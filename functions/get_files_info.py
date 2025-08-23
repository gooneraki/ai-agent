import os

# Here are some standard library functions you'll find helpful:

# os.path.abspath(): Get an absolute path from a relative path
# os.path.join(): Join two paths together safely (handles slashes)
# .startswith(): Check if a string starts with a substring
# os.path.isdir(): Check if a path is a directory
# os.listdir(): List the contents of a directory
# os.path.getsize(): Get the size of a file
# os.path.isfile(): Check if a path is a file
# .join(): Join a list of strings together with a separator


def get_files_info(working_directory, directory="."):
    try:
        relative_dir = os.path.join(working_directory, directory)

        if not os.path.abspath(relative_dir).startswith(
            os.path.abspath(working_directory)
        ):
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

        if not os.path.isdir(relative_dir):
            return f'Error: "{relative_dir}" is not a directory'

        dir_contents = os.listdir(relative_dir)
        files_ext = "\n".join(
            list(
                map(
                    lambda file: f"- {file}: file_size={os.path.getsize(os.path.join(relative_dir,file))} bytes, is_dir={not os.path.isfile(os.path.join(relative_dir,file))}",
                    dir_contents,
                )
            )
        )
        return files_ext
    except Exception as e:
        return f"Error: {e}"
