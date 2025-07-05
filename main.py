import sys
import os
from dotenv import load_dotenv
from google import genai
from google.genai import types



def main():
    if len(sys.argv) <= 1:
        sys.stderr.write("error: no prompt provided\n")
        sys.exit(1)
    prompt = sys.argv[1]
    messages = [
        types.Content(role="user", parts = [types.Part(text=prompt)])
    ]
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key) 

    response = client.models.generate_content(
        model='gemini-2.0-flash-001', 
        contents=messages
    )
    print(response.text)
    if len(sys.argv) > 2:
        if sys.argv[2] == "--verbose":
            print("\nUser prompt:", prompt)
            print("Prompt tokens:", response.usage_metadata.prompt_token_count)
            print("Response tokens:", response.usage_metadata.candidates_token_count)


if __name__ == "__main__":
    main()
