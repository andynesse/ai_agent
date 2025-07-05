import os
from google.genai import types
def get_file_content(working_directory, file_path):
    if file_path.startswith(("../", "/")):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    abspath = os.path.abspath(os.path.join(working_directory, file_path))
    if not os.path.isfile(abspath) :
        return f'Error: File not found or is not a regular file: "{file_path}"'
    
    MAX_CHARS = 10000

    with open(abspath, "r") as f:
        file_content_string = f.read(MAX_CHARS)
        if f.tell() >= MAX_CHARS + 38:
            file_content_string += f'\n[...File "{abspath}" truncated at 10000 characters]'
    return file_content_string

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Returns the content of a file relative to the working directory passed as an argument, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file to get content from, relative to the working directory. Must be provided.",
            ),
        },
    ),
)