import json
import pyperclip
from typing import List
from textwrap import dedent

def create_prompt(files:List[str], user_request:str) -> str:
    prompt = {}
    prompt["files"] = []
    for file in files:
        with open(file, "r") as f:
            prompt["files"].append(
                {
                    "name": file,
                    "content": f.read()
                }
            )
    prompt["user_request"] = dedent(user_request)
    prompt["system"] = """
    1. When updating code, please show only the code that needs to be updated and cite the file(s) name(s).
    """
    return json.dumps(prompt)

if __name__ == "__main__":
    files = ["agent-openai.py"]
    user_request = """Now, let's make the code more responsive by allowing a sequence of questions to be asked."""

    prompt = create_prompt(files, user_request.strip())
    pyperclip.copy(prompt)