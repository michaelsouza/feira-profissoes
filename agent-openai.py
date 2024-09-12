import sys
import json
import time
from openai import OpenAI
from textwrap import dedent
from dotenv import load_dotenv
from sympy import sympify, pretty
from code_interpreter import CodeInterpreter
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.prompt import Prompt
from rich.table import Table
from rich.progress import Progress

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
    messages = initialize_messages(user_question)
    console.print(
        Panel(
            f"[bold yellow]Solving Math Problem:[/bold yellow] {user_question}",
            title="Math Problem",
            expand=False,
        )
    )

    with Progress() as progress:
        task = progress.add_task("[cyan]Solving Math Problem...", total=100)
        run_math_solver_loop(messages, task, progress)


def initialize_messages(user_question):
    return [
        {
            "role": "assistant",
            "content": math_tutor_prompt,
        },
        {
            "role": "user",
            "content": user_question,
        },
    ]


def run_math_solver_loop(messages, task, progress):
    while True:
        progress.update(task, advance=10)
        chat_response, finish_reason = get_chat_response(messages)

        if finish_reason == "stop":
            progress.update(task, advance=100)
            display_solution(chat_response.choices[0].message.content)
            break

        if finish_reason == "tool_calls":
            handle_tool_calls(chat_response.choices[0].message, messages)


def get_chat_response(messages):
    chat_response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        tools=tools,
    )
    return chat_response, chat_response.choices[0].finish_reason


def handle_tool_calls(chat_message, messages):
    messages.append(chat_message)
    tool_calls = chat_message.tool_calls

    for tool_call in tool_calls:
        func_name, func_args = parse_tool_call(tool_call)
        display_tool_call_info(func_name)

        if func_name == "call_coder":
            execute_call_coder(func_args, tool_call.id, messages)


def parse_tool_call(tool_call):
    func = tool_call.to_dict()["function"]
    func_name = func["name"]
    func_args = json.loads(func["arguments"])
    return func_name, func_args


def display_tool_call_info(func_name):
    console.print(f":gear: [bold magenta] Function Call:[/bold magenta] {func_name}")


def execute_call_coder(func_args, tool_call_id, messages):
    code = func_args["code"]
    console.print(":rocket: [bold green]Calling Code Interpreter...[/bold green]")
    func_output = call_coder(code)
    tool_message = {
        "role": "tool",
        "content": json.dumps({"code": code, "output": func_output}),
        "tool_call_id": tool_call_id,
    }
    messages.append(tool_message)


def display_solution(solution_content):
    console.print("\n")
    console.print(
        Panel(
            f"[bold green]Solution Completed:[/bold green]\n{solution_content}",
            title="Completion",
            expand=False,
        )
    )


def main():
    while True:
        user_question = Prompt.ask("[bold yellow]Insira um problema matemático (or digite 'exit' to sair)[/bold yellow]\n")
        
        if user_question.lower() == 'exit':
            console.print(Panel("[bold red]Finalizando...[/bold red]", title="Exit", expand=False))
            break
        
        solve_math_problem(user_question)


if __name__ == "__main__":
    main()
