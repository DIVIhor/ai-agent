import os

from google.genai import types


MAX_CHARS = 10000


def get_file_content(working_directory, file_path):
    # output formatting
    err_prefix = "Error:"
    truncate_msg = '[...File "{file_path}" truncated at 10000 characters]'

    abs_working_dir = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(os.path.join(abs_working_dir, file_path))
    if not abs_file_path.startswith(abs_working_dir):
        return f'{err_prefix} Cannot read "{file_path}" as it is outside the permitted working directory'

    if not os.path.isfile(abs_file_path):
        return f'{err_prefix} "{file_path}" is not a file'

    # file reading and processing
    try:
        with open(abs_file_path, "r") as f:
            file_contents = f.read()
        if len(file_contents) > MAX_CHARS:
            file_contents = file_contents[:MAX_CHARS] + truncate_msg
        return file_contents
    except Exception as e:
        return f"{err_prefix} {e}"


# Tell the LLM how to use the `get_file_content` function
# we won't allow the LLM to specify the `working_directory` parameter
schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Reads contents of a file from the specified directory, constrained to the working directory. The contents are truncated after 10,000 characters, and a predefined message is appended.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file from which to read contents, relative to the working directory.",
            ),
        },
        required=["file_path"],
    ),
)
