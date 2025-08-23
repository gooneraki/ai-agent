import os
from google.genai import types
from functions.config import MAX_CHARS


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
            if len(file_content_string) == MAX_CHARS:
                file_content_string += (
                    f'[...File "{relative_file}" truncated at 10000 characters]'
                )

            return file_content_string

    except Exception as e:
        return f"Error: {e}"


schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description=f"Reads the content of a file up to {MAX_CHARS} characters, constrained to files in working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The file to read content from, relative to the working directory.",
            ),
        },
    ),
)
