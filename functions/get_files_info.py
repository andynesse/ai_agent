import os
from google.genai import types

def get_files_info(working_directory, directory=None):
    if directory.startswith(("../", "/")):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    abspath = os.path.abspath(os.path.join(working_directory, directory))
    if not os.path.isdir(abspath) :
        return f'Error: "{directory}" is not a directory'
    return "\n".join(map(lambda inode: f"- {inode}: file_size={os.path.getsize(os.path.join(abspath, inode))}, is_dir={os.path.isdir(os.path.join(abspath, inode))}",os.listdir(abspath)))

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)