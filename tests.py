# tests.py
from functions.run_python import run_python_file

def run_tests():
    test_cases = [
        ("calculator", "main.py"),
        ("calculator", "main.py", ["3 + 5"]),
        ("calculator", "tests.py"),
        ("calculator", "../main.py"),
        ("calculator", "nonexistent.py")
    ]
    
    for case in test_cases:
        print(f"run_python_file{case}:")
        result = run_python_file(*case)
        print(result)
        print("\n" + "="*50 + "\n")

if __name__ == "__main__":
    run_tests()