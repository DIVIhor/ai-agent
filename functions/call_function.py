from google.genai import types

from functions.get_files_info import get_files_info, schema_get_files_info
from functions.get_file_content import (
    get_file_content,
    schema_get_file_content,
)
from functions.run_python_file import run_python_file, schema_run_python_file
from functions.write_file import write_file, schema_write_file

from config import WORKDIR


# function list to describe to LLM
available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_run_python_file,
        schema_write_file,
    ]
)


def call_function(function_call_part: types.FunctionCall, verbose=False):
    func_name = function_call_part.name
    func_args = function_call_part.args

    if verbose:
        # specify function name and args
        print(f" - Calling function: {func_name}({func_args})")
    else:
        # specify name only
        print(f" - Calling function: {func_name}")

    func_map = {
        "get_files_info": get_files_info,
        "get_file_content": get_file_content,
        "run_python_file": run_python_file,
        "write_file": write_file,
    }

    if func_name not in func_map:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=func_name,
                    response={"error": f"Unknown function: {func_name}"},
                )
            ],
        )

    # add workdir to args
    main_args = {"working_directory": WORKDIR}
    func_args = (
        {**main_args, **func_args} if func_args is not None else main_args
    )
    # call function
    result = func_map[func_name](**func_args)
    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=func_name,
                response={"result": result},
            )
        ],
    )
