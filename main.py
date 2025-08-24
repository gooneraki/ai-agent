import os
import sys
from dotenv import load_dotenv
from google.genai import types, Client
from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.write_file import schema_write_file
from functions.run_python_file import schema_run_python_file
from functions.call_function import call_function


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
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""
    is_verbose = "--verbose" in args
    model_name = "gemini-2.0-flash-001"
    available_functions = types.Tool(
        function_declarations=[
            schema_get_files_info,
            schema_get_file_content,
            schema_write_file,
            schema_run_python_file,
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

    for _ in range(20):
        try:
            response = client.models.generate_content(
                model=model_name,
                contents=messages,
                config=config,
            )

            candidates = response.candidates
            if candidates:
                for candidate in candidates:
                    messages.append(candidate.content)

            function_calls = response.function_calls
            if function_calls:
                for function_call_part in function_calls:

                    function_call_result = call_function(function_call_part, is_verbose)

                    if not function_call_result.parts[0].function_response.response:
                        raise Exception("Fatal exception of some sort")

                    new_message = types.Content(
                        role="user",
                        parts=[
                            types.Part(
                                text=function_call_result.parts[
                                    0
                                ].function_response.response["result"]
                            )
                        ],
                        # parts=[
                        #     types.Part.from_function_response(
                        #         name="call_function",
                        #         text=function_call_result.parts[
                        #             0
                        #         ].function_response.response,
                        #     )
                        # ],
                    )

                    messages.append(new_message)

                    if is_verbose:
                        print(
                            f"-> {function_call_result.parts[0].function_response.response}"
                        )

            else:
                print(response.text)
                break

            if is_verbose:
                print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
                print(
                    f"Response tokens: {response.usage_metadata.candidates_token_count}"
                )
        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    main()
