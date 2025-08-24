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
    description=f"Reads and returns the first {MAX_CHARS} characters of the content from a specified file within the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file whose content should be read, relative to the working directory.",
            ),
        },
        required=["file_path"],
    ),
)
