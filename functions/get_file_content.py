import os
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