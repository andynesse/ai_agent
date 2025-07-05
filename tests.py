from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.write_file import write_file
from functions.run_python_file import run_python_file

def test():
    res = run_python_file("calculator", "main.py")
    print("Result for file: 'main.py' in calculator:\n", res, "\n")

    res = run_python_file("calculator", "tests.py")
    print("Result for file: 'tests.py' in calculator:\n", res, "\n")

    res = run_python_file("calculator", "../main.py")
    print("Result for file: '../main.py' in calculator:\n", res, "\n")

    res = run_python_file("calculator", "nonexistent.py")
    print("Result for file: 'nonexistent.py' in calculator:\n", res, "\n")

if __name__ == "__main__":
    test()