import os
from google.genai import types


def write_file(working_directory, file_path, content):
    try:
        relative_file = os.path.join(working_directory, file_path)

        if not os.path.abspath(relative_file).startswith(
            os.path.abspath(working_directory)
        ):
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

        if not os.path.isfile(relative_file):
            # create file here
            open(relative_file, "a").close()

        with open(relative_file, "w") as f:
            f.write(content)

        character_count = 0
        with open(relative_file, "r") as file:
            raw_content = file.read()
            character_count = len(raw_content)

        return f'Successfully wrote to "{file_path}" ({character_count} characters written)'

    except Exception as e:

        return f"Error: {e}"


schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes content to a file within the working directory. Creates the file if it doesn't exist.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the file to write, relative to the working directory.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="Content to write to the file",
            ),
        },
        required=["file_path", "content"],
    ),
)
