import os
from functions.config import MAX_CHARS

# os.path.abspath: Get an absolute path from a relative path
# os.path.join: Join two paths together safely (handles slashes)
# .startswith: Check if a string starts with a specific substring
# os.path.isfile: Check if a path is a file

# MAX_CHARS = 10000

# with open(file_path, "r") as f:
#     file_content_string = f.read(MAX_CHARS)

def get_file_content(working_directory, file_path):
    try:
        
        relative_file = os.path.join(working_directory, file_path)


        if not os.path.abspath(relative_file).startswith(
            os.path.abspath(working_directory)
        ):
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

        if not os.path.isfile(relative_file):
            return f'Error: File not found or is not a regular file: "{file_path}"'
        
        with open(relative_file, "r") as f:
            file_content_string = f.read(MAX_CHARS)
            if len(file_content_string)==MAX_CHARS:
                file_content_string += f'[...File "{relative_file}" truncated at 10000 characters]'

            return file_content_string

        

    except Exception as e:
        return f"Error: {e}"