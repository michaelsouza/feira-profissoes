# code_interpreter.py

import io
import sys
import ast
from typing import List


class CodeInterpreter:
    def __init__(self):
        # A dictionary to hold the global variables across multiple executions
        self.global_context = {}
        self.execute('\n'.join([
            "import numpy as np",
            "import sympy as sp",
            "import scipy as sc",
            "import pandas as pd",
            "import matplotlib.pyplot as plt",
            "import seaborn"
        ]))

    def extract_code_chunks(self, code: str) -> List[str]:
        """Splits the code into multiple lines without breaking important structures."""
        try:
            parsed_code = ast.parse(code)
            code_chunks = []
            processed_line_idx = []
            for node in ast.walk(parsed_code):
                node_code = ast.get_source_segment(code, node)
                if isinstance(
                    node, (ast.FunctionDef, ast.For, ast.While, ast.If, ast.With, ast.ClassDef, ast.Expr, ast.Assign, ast.ImportFrom, ast.Import)
                ):
                    node_idx_bgn = node.lineno - 1
                    node_idx_end = node.end_lineno
                    
                    # Check if the chunk has already been processed
                    already_processed = False
                    for i, j in processed_line_idx:
                        if node_idx_bgn >= i and node_idx_end <= j:
                            already_processed = True
                            break
                    if already_processed:
                        continue

                    processed_line_idx.append((node_idx_bgn, node_idx_end))                
                    code_chunks.append(node_code)

            return code_chunks

        except Exception as e:
            return f"Error: {str(e)}"

    def execute(self, code: str) -> str:
        """
        Execute the given Python code line by line if it is multiline.
        It returns the combined output for all lines.
        """
        # Split the code into multiple lines
        code_lines = self.extract_code_chunks(code)

        # Capture the combined output of all lines
        combined_output = []

        # Execute each line individually
        for line in code_lines:
            if line.strip() == "":
                continue
            output = self._execute_line(line)
            combined_output.append(output)

        non_empty_output = [output for output in combined_output if output.strip() != ""]
        return "\n".join(non_empty_output)

    def _execute_line(self, code: str) -> str:
        """
        Execute the given Python code and return the output.
        """

        # Capture standard output
        output_capture = io.StringIO()
        sys.stdout = output_capture

        try:
            # Parse the code to check if it is an expression or statement
            parsed_code = ast.parse(code, mode="exec")

            # Check if the parsed code contains only an expression
            if isinstance(parsed_code.body[0], ast.Expr):
                # If it is an expression, evaluate it
                result = str(eval(code, self.global_context))
                result = result if result != "None" else output_capture.getvalue()
                return str(result)

            # Otherwise, execute the statement
            exec(code, self.global_context, self.global_context)
        except Exception as e:
            return f"Error: {str(e)}"
        finally:
            # Restore stdout to its original state
            sys.stdout = sys.__stdout__

        # Get the captured output
        output = output_capture.getvalue()
        return output if output else ""


def test_code_interpreter():
    interpreter = CodeInterpreter()
    ok_code = ""

    # Test simple expressions
    assert interpreter.execute("2 + 3") == "5"
    assert interpreter.execute("2 ** 3") == "8"
    assert interpreter.execute("2 * 3") == "6"
    assert interpreter.execute("2 / 3") == "0.6666666666666666"

    # Test simple statements
    assert interpreter.execute("a = 10") == ok_code
    assert interpreter.execute("b = 20") == ok_code
    assert interpreter.execute("a + b") == "30"

    # Test error handling
    assert interpreter.execute("10 / 0") == "Error: division by zero"
    assert interpreter.execute("print('Hello, World!')") == "Hello, World!\n"

    # Test multi-line code
    assert (
        interpreter.execute(
            """
def dummy(a, b):
    while a < b:
        a += 1       
    return a + b

y = dummy(2, 3)
"""
        )
        == ok_code
    )
    assert interpreter.execute("y") == "6"

    # Test multi-line using sympy
    assert (
        interpreter.execute(
            """
x = sp.symbols('x')
y = sp.symbols('y')
eq = sp.Eq(x + y, 10)
sol = sp.solve(eq, x)
"""
        )
        == ok_code
    )
    assert interpreter.execute("sol") == "[10 - y]"

    # Test multi-line using numpy
    assert (
        interpreter.execute(
            """
x = np.arange(0, 5, 1) 
y = x + 1
y
"""
        )
        == "[1 2 3 4 5]"
    )
    
    print("All tests passed successfully!")


# Example usage
if __name__ == "__main__":
    test_code_interpreter()
