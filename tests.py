from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.write_file import write_file

def test():
    res = write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum")
    print("Result for file: 'lorem.txt ' in calculator:\n", res, "\n")

    res = write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet")
    print("Result for file: 'pkg/morelorem.txt ' in calculator:\n", res, "\n")

    res = write_file("calculator", "/tmp/temp.txt", "this should not be allowed")
    print("Result for file: '/bin/cat ' in calculator:\n", res, "\n")

if __name__ == "__main__":
    test()