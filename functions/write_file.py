import os


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
