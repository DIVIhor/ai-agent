import os
import sys

from dotenv import load_dotenv
from google import genai
from google.genai import types


def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    # create a new instance of a Gemini client
    client = genai.Client(api_key=api_key)
    # free tier model name
    model = "gemini-2.0-flash-001"

    # get prompt from CLI input
    if len(sys.argv) < 2:
        print("No prompt provided. Exiting...")
        exit(1)
    user_prompt = sys.argv[1]

    # conversation history
    messages = [types.Content(role="user", parts=[types.Part(text=user_prompt)])]

    resp = client.models.generate_content(model=model, contents=messages)
    print(resp.text)

    if "--verbose" in sys.argv:
        # show the user's prompt
        print("User prompt:", user_prompt)
        # show the number of prompt tokens
        print("Prompt tokens:", resp.usage_metadata.prompt_token_count)
        # show the number of response tokens
        print("Response tokens:", resp.usage_metadata.candidates_token_count)


if __name__ == "__main__":
    main()
