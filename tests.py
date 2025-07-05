from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content

def test():
    res = get_file_content("calculator", "main.py")
    print("Result for file: 'main.py ' in calculator:\n", res, "\n")

    res = get_file_content("calculator", "pkg/calculator.py")
    print("Result for file: 'pkg/calculator.py ' in calculator:\n", res, "\n")

    res = get_file_content("calculator", "/bin/cat")
    print("Result for file: '/bin/cat ' in calculator:\n", res, "\n")

if __name__ == "__main__":
    test()