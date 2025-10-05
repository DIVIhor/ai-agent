import os


def get_files_info(working_directory, directory="."):
    # output formatting
    err_prefix = "Error:"
    row_delimiter = "\n"
    
    abs_working_dir = os.path.abspath(working_directory)
    abs_dir_path = os.path.abspath(os.path.join(working_directory, directory))

    if not abs_dir_path.startswith(abs_working_dir):
        return f'{err_prefix} Cannot list "{directory}" as it is outside the permitted working directory'

    if not os.path.isdir(abs_dir_path):
        return f'{err_prefix} "{directory}" is not a directory'

    file_info = []
    try:
        for entry in os.listdir(abs_dir_path):
            entry_path = os.path.join(abs_dir_path, entry)
            size = os.path.getsize(entry_path)
            is_dir = os.path.isdir(entry_path)

            file_info.append(f" - {entry}: file_size={size} bytes, is_dir={is_dir}")

        return row_delimiter.join(file_info)

    except Exception as e:
        return f"{err_prefix} {e}"
