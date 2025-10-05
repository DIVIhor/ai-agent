import os


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
