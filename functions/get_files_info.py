import os
from google.genai import types


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
    

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)
