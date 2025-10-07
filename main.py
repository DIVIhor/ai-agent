import os
import sys

from time import sleep

from dotenv import load_dotenv
from google import genai
from google.genai import types

from functions.call_function import available_functions, call_function

from config import MAX_ITERATIONS, MODEL, ROLE
from prompts import system_prompt


def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    # create a new instance of a Gemini client
    client = genai.Client(api_key=api_key)

    # get prompt from CLI input
    if len(sys.argv) < 2:
        print("No prompt provided. Exiting...")
        exit(1)

    # extract arguments
    args = [arg for arg in sys.argv[1:] if not arg.startswith("--")]
    if not args:
        print("AI Code Assistant")
        print('\nUsage: python main.py "your prompt here" [--verbose]')
        print('Example: python main.py "How do I fix the calculator?"')
        sys.exit(1)

    # populate a prompt string using provided arguments
    user_prompt = " ".join(args)

    # check for verbose info request
    is_verbose = "--verbose" in sys.argv
    if is_verbose:
        # show the user's prompt
        print("User prompt:", user_prompt)

    # conversation history
    messages = [types.Content(role=ROLE, parts=[types.Part(text=user_prompt)])]

    iters = 0
    while iters <= MAX_ITERATIONS:
        iters += 1
        if iters == MAX_ITERATIONS:
            print(f"Maximum iterations ({MAX_ITERATIONS}) reached.")
            sys.exit(1)

        try:
            final_resp = generate_content(client, messages, is_verbose)
            if final_resp:
                print("Final response:")
                print(final_resp)
                break
        except Exception as e:
            print(f"Error generating content: {e}")


def generate_content(client, messages, is_verbose):
    resp = client.models.generate_content(
        model=MODEL,
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions], system_instruction=system_prompt
        ),
    )

    if is_verbose:
        # show the number of prompt tokens
        print("Prompt tokens:", resp.usage_metadata.prompt_token_count)
        # show the number of response tokens
        print("Response tokens:", resp.usage_metadata.candidates_token_count)

    for candidate in resp.candidates:
        messages.append(candidate.content)
    # sleep(3)

    # show the output
    if not resp.function_calls:
        return resp.text

    function_responses = []  # track responses
    # show called functions with their used arguments
    for function_call_part in resp.function_calls:
        function_call_result = call_function(function_call_part, is_verbose)
        if (
            not function_call_result.parts
            or not function_call_result.parts[0].function_response
        ):
            raise Exception(
                f"Empty function call result: {function_call_part.name}({function_call_part.args})"
            )
        # show extended response
        if is_verbose:
            print(
                f"-> {function_call_result.parts[0].function_response.response}"
            )

        function_responses.append(function_call_result.parts[0])

    if not function_responses:
        raise Exception("No function responses generated, exiting.")

    # save results to messages
    messages.append(types.Content(parts=function_call_result.parts, role=ROLE))


if __name__ == "__main__":
    main()
