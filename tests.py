from functions.get_files_info import get_files_info

def test():
    res = get_files_info("calculator", ".")
    print("Result for current directory:\n", res, "\n")

    res = get_files_info("calculator", "pkg")
    print("Result for 'pkg' directory:\n", res, "\n")

    res = get_files_info("calculator", "/bin")
    print("Result for '/bin' directory:\n", res, "\n")

    res = get_files_info("calculator", "../")
    print("Result for '../' directory:\n", res, "\n")

if __name__ == "__main__":
    test()