import os
import sys
from dotenv import load_dotenv
from google.genai import types, Client
from functions.get_files_info import schema_get_files_info


def main():
    load_dotenv()
    args = sys.argv

    if len(args) == 1:
        print("Requires argument for PROMPT. usage `uv run main.py PROMPT [--verbose]`")
        sys.exit(1)

    user_prompt = args[1]
    system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""
    is_verbose = "--verbose" in args
    model_name = "gemini-2.0-flash-001"
    available_functions = types.Tool(
        function_declarations=[
            schema_get_files_info,
        ]
    )
    config = types.GenerateContentConfig(
        tools=[available_functions], system_instruction=system_prompt
    )

    if is_verbose:
        print(f"User prompt: {user_prompt}")

    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]

    api_key = os.environ.get("GEMINI_API_KEY")

    client = Client(api_key=api_key)
    response = client.models.generate_content(
        model=model_name,
        contents=messages,
        config=config,
    )

    function_calls = response.function_calls
    if function_calls:
        for function_call_part in function_calls:
            print(
                f"Calling function: {function_call_part.name}({function_call_part.args})"
            )
    else:
        print(response.text)

    if is_verbose:
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")


if __name__ == "__main__":
    main()
