import sys
import os
import time

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
    verbose = False
    if len(sys.argv) > 2:
        if sys.argv[2] == "--verbose":
            verbose = True

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
    
    Most likely if the question doesn't provide much context, the problem lies in the code somewhere.
    If it is provided a bug, try to find out where in the file system and in what files the bug is, not just start writing an answer in a file, but find out if the files has any code that the question is relevant for.
    Also try to not overwrite all the code of a file, but edit the file content. For example when fixing a bug you should read the file and then edit it before writing to the file with the solution.
    There is ALWAYS an answer. If you are stuck it might be an idea to use get_files_info.
    Also don't make any temp files or other unnecessary files/directories.
    If you need more information to answer you should still try to find the answer with using the provided functions.
    You should at least try to solve the problem even if the user doesn't precisely provide the path or step by step what you should do.
    All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
    When you are done with using the functions provided and you have solved the problem or question provided by the user, you should return an answer to the original question. Your output should be styled well to easily be read in the console. The answer should also not have long sentences per point, but structured more in key functionalities.
    Then draw a car in the console when you ar done.
    """
    for i in range(20):
        print(i, "\n\n")
        response = client.models.generate_content(
            model='gemini-2.0-flash-001', 
            contents=messages,
            config=types.GenerateContentConfig(
                tools=[available_functions],
                system_instruction=system_prompt
            )
        )
        [messages.append(candidate.content) for candidate in response.candidates]

        function_calls = response.function_calls
        if function_calls and len(response.function_calls) > 0:
            function_call_results = list(map(lambda call: call_function(call, verbose), function_calls))
            try:
                for res in function_call_results:
                    messages.append(res)
                    if verbose:
                        if "result" in res.parts[0].function_response.response:
                            print(f"-> Reslult:\n{res.parts[0].function_response.response["result"]}\n")
                        else:
                            print(f"-> Reslult:\n{res.parts[0].function_response.response}\n")
            except Exception as e:
                raise f'Fatal Error: {e}'
        else:
            print(response.text)
            break
        if i > 9:
            time.sleep(10)
    if verbose:
        print("\nUser prompt:", prompt)
        print("Prompt tokens:", response.usage_metadata.prompt_token_count)
        print("Response tokens:", response.usage_metadata.candidates_token_count)


if __name__ == "__main__":
    main()
