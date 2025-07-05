import sys
import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.write_file import schema_write_file
from functions.run_python_file import schema_run_python_file
from functions.call_function import call_function

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

    available_functions = types.Tool(
        function_declarations=[
            schema_get_files_info,
            schema_get_file_content,
            schema_write_file,
            schema_run_python_file
        ]
    )

    system_prompt = """
    You are a helpful AI coding agent.

    When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

    - List files and directories
    - Read file contents
    - Execute Python files with optional arguments
    - Write or overwrite files
    
    All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
    """

    response = client.models.generate_content(
        model='gemini-2.0-flash-001', 
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions],
            system_instruction=system_prompt
        )
    )
    verbose = False
    if len(sys.argv) > 2:
        if sys.argv[2] == "--verbose":
            verbose = True
    function_calls = response.function_calls
    if function_calls and len(response.function_calls) > 0:
        function_call_results = list(map(lambda call: call_function(call, verbose), function_calls))
        try:
            for res in function_call_results:
                if verbose:
                    print(f"-> Reslult:\n{res.parts[0].function_response.response["result"]}")
        except Exception as e:
            raise f'Fatal Error: {e}'
    if verbose:
        print("\nUser prompt:", prompt)
        print("Prompt tokens:", response.usage_metadata.prompt_token_count)
        print("Response tokens:", response.usage_metadata.candidates_token_count)


if __name__ == "__main__":
    main()
