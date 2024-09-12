import sys
import json
from openai import OpenAI
from dotenv import load_dotenv
from code_interpreter import CodeInterpreter
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.progress import Progress
from typing import List

console = Console()

load_dotenv()

client = OpenAI()
coder = CodeInterpreter()

# MODEL = "gpt-4o" # expensive, larger model
MODEL = "gpt-4o-mini"  # affordable, smaller model


tools = [
    {
        "type": "function",
        "function": {
            "name": "call_coder",
            "description": "Call a python code interpreter to run code.",
            "parameters": {
                "type": "object",
                "properties": {
                    "code": {
                        "type": "string",
                        "description": "The python code to run.",
                    }
                },
                "required": ["code"],
            },
        },
    }
]

math_tutor_prompt = """
    You are a helpful math tutor. You will be provided with a math problem, and your goal will be to output a step by step solution, along with a final answer.
    For each step, just provide the output as an equation use the explanation field to detail the reasoning.
    I have a local code interpreter available to you, so you can ask for help with any complex calculations.
    In order to get the solution from the code interpreter, you can use the `call_coder` function. The `call_coder` function takes a single argument, `code`, which is a string containing the Python code you want to run.    
    Make sure to provide the code interpreter with the necessary code to solve the problem.
    Use the same language and style of the user's question when providing the solution.
"""


def call_coder(code: str) -> str:
    output = coder.execute(code)
    sys.stdout = sys.__stdout__
    console.print(
        Panel(
            f"[bold green]Executed Code:\n[/bold green]{code}",
            title="Code Execution",
            expand=False,
        )
    )
    console.print(
        Panel(f"[bold blue]Output:[/bold blue] {output}", title="Result", expand=False)
    )
    return output


def solve_math_problem(user_question):
    messages = [
        {
            "role": "assistant",
            "content": math_tutor_prompt,
        },
        {
            "role": "user",
            "content": user_question,
        },
    ]

    console.print(
        Panel(
            f"[bold yellow]Solving Math Problem:[/bold yellow]\n{user_question}",
            title="Math Problem",
            expand=False,
        )
    )

    with Progress() as progress:
        task = progress.add_task("[cyan]Solving Math Problem...", total=100)
        while True:
            progress.update(task, advance=10)
            chat_message, finish_reason = call_chat(messages)

            if finish_reason == "stop":
                progress.update(task, advance=100)
                display_solution(messages)
                break
            elif finish_reason == "tool_calls":
                handle_tool_calls(chat_message, messages)
            else:
                raise Exception(f"Unexpected finish reason: {finish_reason}")


def call_chat(messages: List[dict]):
    # call the OpenAI API to get a response
    chat_response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        tools=tools,
    )
    chat_message = chat_response.choices[0].message
    finish_reason = chat_response.choices[0].finish_reason
    messages.append(chat_message.to_dict())
    return chat_message, finish_reason


def handle_tool_calls(chat_message, messages):
    tool_calls = chat_message.tool_calls
    for tool_call in tool_calls:
        # get the function name and arguments
        func = tool_call.to_dict()["function"]
        func_name = func["name"]
        func_args = json.loads(func["arguments"])
        console.print(
            f"\n:gear: [bold magenta] Function Call:[/bold magenta] {func_name}"
        )
        if func_name == "call_coder":
            execute_call_coder(func_args, tool_call.id, messages)
        else:
            raise Exception(f"Unknown function: {func_name}")


def execute_call_coder(func_args, tool_call_id, messages):
    code = func_args["code"]
    console.print(":rocket: [bold green]Calling Code Interpreter...[/bold green]")
    func_output = call_coder(code)
    coder_output_message = {
        "role": "tool",
        "content": json.dumps({"code": code, "output": func_output}),
        "tool_call_id": tool_call_id,
    }
    messages.append(coder_output_message)


def display_solution(messages: list):
    messages = [m for m in messages if isinstance(m, dict)]
    # drop the first two messages (prompt and user question)
    messages = messages[2:]
    solution = ""
    for m in messages:
        # skip tool messages. it's already displayed in the code interpreter output
        if m['role'] == 'tool':
            continue
        solution += f"{m['content']}\n"

    console.print("\n")
    console.print(
        Panel(
            f"[bold green]Solution Completed:[/bold green]\n{solution}",
            title="Completion",
            expand=False,
        )
    )


def main():
    while True:
        user_question = Prompt.ask(
            "[bold yellow]Insira um problema matemático (or digite 'exit' to sair)[/bold yellow]\n"
        )

        if user_question.lower() == "exit":
            console.print(
                Panel("[bold red]Finalizando...[/bold red]", title="Exit", expand=False)
            )
            break

        solve_math_problem(user_question)


def test_main():
    user_question = "Qual é o resultado de $\\int_{0}^{3.75} x^2 dx$?"
    solve_math_problem(user_question)


if __name__ == "__main__":
    # test_main()
    main()
