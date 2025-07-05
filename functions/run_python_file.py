import os
import subprocess
def run_python_file(working_directory, file_path):
    if file_path.startswith(("../", "/")):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    abspath = os.path.abspath(os.path.join(working_directory, file_path))
    if not os.path.exists(abspath) :
        return f'Error: File "{file_path}" not found.'
    if not file_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'
    try:
        output = subprocess.run(["python", abspath],timeout=30,capture_output=True)
        if output.stdout.decode("utf-8") == "":
            return "No output produced."
        result = f'STDOUT: {output.stdout.decode("utf-8")}\nSTDERR: {output.stderr.decode("utf-8")}'
        if output.returncode != 0:
            result += f'\nProcess exited with code: {output.returncode}'
        return result
    except Exception as e:
        return f"Error: executing Python file: {e}"