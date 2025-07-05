import os
def write_file(working_directory, file_path, content):
    if file_path.startswith(("../", "/")):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    abspath = os.path.abspath(os.path.join(working_directory, file_path))
    try:
        if not os.path.exists(abspath):
            print("Making dirs")
            os.makedirs(os.path.split(abspath)[0])
        
        with open(abspath, "w") as f:
            f.write(content)
        return  f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception:
        return f'Error: Failed to write to "{file_path}" (0 characters written)'