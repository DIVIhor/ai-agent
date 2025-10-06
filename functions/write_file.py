import os

from google.genai import types


def write_file(working_directory, file_path, content):
    # output formatting
    err_prefix = "Error:"

    abs_working_dir = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(os.path.join(abs_working_dir, file_path))

    if not abs_file_path.startswith(abs_working_dir):
        return f'{err_prefix} Cannot write to "{file_path}" as it is outside the permitted working directory'

    if os.path.exists(abs_file_path) and os.path.isdir(abs_file_path):
        return f'Error: "{file_path}" is a directory, not a file'

    # cut filename to check if all the folders exist
    try:
        path_dirs = os.path.dirname(abs_file_path)
        if not os.path.exists(path_dirs):
            os.makedirs(path_dirs)
    except Exception as e:
        return f"{err_prefix} creating directory: {e}"

    try:
        with open(abs_file_path, "w") as f:
            f.write(content)

        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

    except Exception as e:
        return f"{err_prefix} writing to file: {e}"


# Tell the LLM how to use the `write_file` function
# we won't allow the LLM to specify the `working_directory` parameter
schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes contents to a file at the specified path, constrained to the working directory. If the file exists, its contents will be overwritten. Missing directories will be created if necessary.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file to which content will be written, relative to the working directory.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content to be written to the specified file.",
            ),
        },
        required=["file_path"],
    ),
)
