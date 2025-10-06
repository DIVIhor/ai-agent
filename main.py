import os
import sys

from dotenv import load_dotenv
from google import genai
from google.genai import types

from functions.get_files_info import schema_get_files_info


def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    # create a new instance of a Gemini client
    client = genai.Client(api_key=api_key)
    # free tier model name
    model = "gemini-2.0-flash-001"

    available_functions = types.Tool(
        function_declarations=[
            schema_get_files_info,
        ]
    )

    system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""

    # get prompt from CLI input
    if len(sys.argv) < 2:
        print("No prompt provided. Exiting...")
        exit(1)
    user_prompt = sys.argv[1]

    # conversation history
    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)])
    ]

    resp = client.models.generate_content(
        model=model,
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions],
            system_instruction=system_prompt,
        ),
    )

    # show called functions with their used arguments
    if resp.function_calls is not None:
        for function_call in resp.function_calls:
            print(f"Calling function: {function_call.name}({function_call.args})")
    # show the output
    else:
        print(resp.text)

    # additional info
    if "--verbose" in sys.argv:
        # show the user's prompt
        print("User prompt:", user_prompt)
        # show the number of prompt tokens
        print("Prompt tokens:", resp.usage_metadata.prompt_token_count)
        # show the number of response tokens
        print("Response tokens:", resp.usage_metadata.candidates_token_count)


if __name__ == "__main__":
    main()
