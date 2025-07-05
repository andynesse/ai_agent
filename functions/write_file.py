import os
from google.genai import types

def write_file(working_directory, file_path, content):
    if file_path.startswith(("../", "/")):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    abspath = os.path.abspath(os.path.join(working_directory, file_path))
    try:
        if not os.path.exists(os.path.split(abspath)[0]):
            print("Making dirs")
            os.makedirs(os.path.split(abspath)[0])
        
        with open(abspath, "w") as f:
            f.write(content)
        return  f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f'Error: Failed to write to "{file_path}" (0 characters written): {e}'
    

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes specified content to the specified file relative to the working directory, constrained to the working directory. If the path to the file doesn't exist it will generate the branch and create the file before writing the content to it. Returns a string either starting with 'Successfully' or 'Error'",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path to write content to, relative to the working directory. Must be provided.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content to be written to the file. Must be provided."
            )
        },
    ),
)