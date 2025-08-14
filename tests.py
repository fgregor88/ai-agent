# tests.py
from functions.write_file import write_file

def run_tests():
    # Test cases
    test_cases = [
        ("calculator", "lorem.txt", "wait, this isn't lorem ipsum"),
        ("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet"),
        ("calculator", "/tmp/temp.txt", "this should not be allowed")
    ]
    
    for working_dir, file_path, content in test_cases:
        print(f"write_file('{working_dir}', '{file_path}', '{content[:20]}...'):")
        result = write_file(working_dir, file_path, content)
        print(f"Result: {result}")
        print()

if __name__ == "__main__":
    run_tests()