import os
import sys

from dotenv import load_dotenv
from google import genai
from google.genai import types

from functions.call_function import available_functions, call_function


def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    # create a new instance of a Gemini client
    client = genai.Client(api_key=api_key)
    # free tier model name
    model = "gemini-2.0-flash-001"

    system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""

    # get prompt from CLI input
    if len(sys.argv) < 2:
        print("No prompt provided. Exiting...")
        exit(1)
    user_prompt = sys.argv[1]
    is_verbose = "--verbose" in sys.argv

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

    # show the output
    if not resp.function_calls:
        return resp.text

    function_responses = []  # track responses
    # show called functions with their used arguments
    if resp.function_calls is not None:
        for function_call_part in resp.function_calls:
            function_call_result = call_function(
                function_call_part, is_verbose
            )
            if (
                not function_call_result.parts
                or not function_call_result.parts[0].function_response
            ):
                raise Exception(
                    f"No function responses generated for: {function_call_part.name}({function_call_part.args})"
                )
            if is_verbose:
                print(
                    f"-> {function_call_result.parts[0].function_response.response}"
                )
            function_responses.append(function_call_result.parts[0])

    if not function_responses:
        raise Exception("no function responses generated, exiting.")

    # additional info
    if is_verbose:
        # show the user's prompt
        print("User prompt:", user_prompt)
        # show the number of prompt tokens
        print("Prompt tokens:", resp.usage_metadata.prompt_token_count)
        # show the number of response tokens
        print("Response tokens:", resp.usage_metadata.candidates_token_count)


if __name__ == "__main__":
    main()
