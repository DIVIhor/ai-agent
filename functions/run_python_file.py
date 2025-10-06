import os
import subprocess

from google.genai import types


def run_python_file(working_directory, file_path, args=[]):
    # output formatting
    err_prefix = "Error:"

    abs_working_dir = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(os.path.join(abs_working_dir, file_path))

    if not abs_file_path.startswith(abs_working_dir):
        return f'{err_prefix} Cannot execute "{file_path}" as it is outside the permitted working directory'

    if not os.path.exists(abs_file_path):
        return f'{err_prefix} File "{file_path}" not found.'

    if not file_path.endswith(".py"):
        return f'{err_prefix} File "{file_path}" is not a Python file.'

    try:
        result = subprocess.run(
            ["python", abs_file_path, *args],
            timeout=30,
            stderr=subprocess.PIPE,
            stdout=subprocess.PIPE,
            text=True,
            cwd=abs_working_dir,
        )

        output_delimiter = "\n"
        results = []
        if result.stdout:
            results.append(f"STDOUT: {result.stdout}")
        if result.stdout:
            results.append(f"STDERR: {result.stderr}")

        if result.returncode != 0:
            results.append(f"Process exited with code {result.returncode}")

        return (
            output_delimiter.join(results)
            if results
            else "No output produced."
        )

    except Exception as e:
        return f"{err_prefix} executing Python file: {e}"


# Tell the LLM how to use the `run_python_file` function
# we won't allow the LLM to specify the `working_directory` parameter
schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes a Python file from the specified path, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the Python file to be executed, relative to the working directory.",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                description="A list of additional arguments to pass when running the file. If not provided, the file will be executed without any arguments.",
                items=types.Schema(
                    type=types.Type.STRING,
                    description="Optional arguments to pass to the Python file.",
                ),
            ),
        },
        required=["file_path"],
    ),
)
