import os
import sys
from dotenv import load_dotenv
from google import genai


def main():
    load_dotenv()
    args = sys.argv

    if len(args)==1:
        print("Requires argument for PROMPT. usage `uv run main.py PROMPT [--verbose]`")
        sys.exit(1)

    user_prompt = args[1]
    is_verbose = "--verbose" in args
    if is_verbose:
        print(f"User prompt: {user_prompt}")

    messages = [
        genai.types.Content(role="user", parts=[genai.types.Part(text=user_prompt)]),
    ]


    api_key = os.environ.get("GEMINI_API_KEY")

    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(
        model='gemini-2.0-flash-001', contents=messages
    )

    print(response.text)

    if is_verbose:
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
    


if __name__ == "__main__":
    main()
