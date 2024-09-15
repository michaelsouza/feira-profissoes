import sys
import json
from openai import OpenAI
from dotenv import load_dotenv
from code_interpreter import CodeInterpreter
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.syntax import Syntax
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
I have a local code interpreter available to you, so you should call it for any calculations. 
You can break down the problem into smaller parts and use the code interpreter to solve them.
In order to get the solution from the code interpreter, you can use the `call_coder` function. 
The `call_coder` function takes a single argument, `code`, which is a string containing the Python code you want to run.    
Make sure to provide the code interpreter with the necessary code to solve the problem.
Use the same language and style of the user's question when providing the solution.
"""

math_tutor_final = """
This is the final solution that will be presented to the user, so make sure it is correct and easy to understand.
You cannot use the `call_coder` function anymore.
Do not comment about the solution, just provide the solution itself but in a clear and detailed way.
Revise the solution and make it as clear as possible.
====================
%s
"""


def call_coder(code: str) -> str:
    output = coder.execute(code)
    sys.stdout = sys.__stdout__
    syntax = Syntax(code, "python", theme="github-dark", line_numbers=True)
    console.print("")  # add a new line
    console.print(
        Panel(
            syntax,
            title="Execução de Código",
            expand=True,
        )
    )
    console.print(
        Panel(
            f"[bold blue]Output:[/bold blue] {output}", title="Resultado", expand=True
        )
    )
    return output


def solve_math_problem(user_question: str, max_steps=10):
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
            f"[bold yellow]Resolvendo:[/bold yellow]\n{user_question}",
            title="Problema Matemático",
            expand=True,
        )
    )

    while len(messages) < max_steps:
        chat_message, finish_reason = call_chat(messages)

        if finish_reason == "stop":
            display_solution(messages)
            break
        elif finish_reason == "tool_calls":
            handle_tool_calls(chat_message, messages)
        else:
            raise Exception(f"Unexpected finish reason: {finish_reason}")


def call_chat(messages: List[dict]):
    # call the OpenAI API to get a response
    console.print(f"🚀 Calling OpenAI API ...")
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
        if func_name == "call_coder":
            execute_call_coder(func_args, tool_call.id, messages)
        else:
            raise Exception(f"Unknown function: {func_name}")


def execute_call_coder(func_args, tool_call_id, messages):
    code = func_args["code"]
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
        if m["role"] == "tool":
            continue
        solution += f"{m['content']}\n"
    message = {"role": "user", "content": math_tutor_final % solution}
    messages.append(message)
    chat_message, finish_reason = call_chat(messages)
    content = chat_message.content
    console.print("\n")
    console.print(
        Panel(
            f"[bold green]Solução Completa:[/bold green]\n{content}",
            title="Resultado Final",
            expand=True,
        )
    )


def welcome_banner():
    console.print(
        Panel(
            r'''
[bold yellow] 
 __  __       _   _       _____      _                                         .="=.
|  \/  | __ _| |_| |__   |_   _|   _| |_ ___  _ __                           _/.-.-.\_     _
| |\/| |/ _` | __| '_ \    | || | | | __/ _ \| '__|                         ( ( o o ) )    ))
| |  | | (_| | |_| | | |   | || |_| | || (_) | |                             |/  "  \|    //
|_|  |_|\__,_|\__|_| |_|   |_| \__,_|\__\___/|_|             .-------.        \'---'/    //
                                                            _|~~ ~~  |_       /`"""`\\  ((
   _   _ _____ ____     ____   ___ ____  _  _             =(_|_______|_)=    / /_,_\ \\  \\
  | | | |  ___/ ___|   |___ \ / _ \___ \| || |              |:::::::::|      \_\\_'__/ \  ))
  | | | | |_ | |         __) | | | |__) | || |_             |:::::::[]|       /`  /`~\  |//
  | |_| |  _|| |___     / __/| |_| / __/|__   _|            |o=======.|      /   /    \  /
   \___/|_|   \____|   |_____|\___/_____|  |_|              `"""""""""`  ,--`,--'\/\    /
                                                                     '-- "--'
[/bold yellow]
''',
            title="Feira das Profissões",
            expand=True,
        )
    )


def main():
    welcome_banner()
    while True:
        user_question = Prompt.ask(
            "[bold yellow]Insira um problema matemático (or digite 'exit' para sair)[/bold yellow]\n"
        )

        if user_question.lower() == "exit":
            console.print(
                Panel("[bold red]Finalizando...[/bold red]", title="Exit", expand=False)
            )
            break

        solve_math_problem(user_question)


def test_main():
    welcome_banner()
    user_question = "Determine:\n(a) $\\int_{0}^{3.75} (x^2 + sin(x))dx$;\n(b) o oitavo elemento da série de Fibonacci;\n(c) Um triângulo de lados 1, 3 e 7 pode ser retângulo?"
    solve_math_problem(user_question)


if __name__ == "__main__":
    # test_main()
    main()
