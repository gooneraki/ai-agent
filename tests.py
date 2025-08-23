from functions.get_files_info import get_files_info

run_cases = [
    (
        ["calculator", "."],
        """- main.py: file_size=576 bytes, is_dir=False\n- tests.py: file_size=1343 bytes, is_dir=False\n- pkg: file_size=92 bytes, is_dir=True"""
    ),
    (
        ["calculator", "pkg"],
        """- calculator.py: file_size=1739 bytes, is_dir=False\n- render.py: file_size=768 bytes, is_dir=False"""
    ),
    (
        ["calculator", "/bin"],
        """Error: Cannot list "/bin" as it is outside the permitted working directory"""
    ),
    (
        ["calculator", "../"],
        """Error: Cannot list "../" as it is outside the permitted working directory"""
    )
]

def test(input1, expected_output):
    print(f"/n===============")
    print(f"input {input1}")
    print(f"EXPECTED\n{expected_output}")

    result = get_files_info(*input1)
    print(f"ACTUAL\n{result}")
    if (result != expected_output):
        print("FAILED TEST")
    else:
        print("SUCCESS TEST")
    return result == expected_output

def main():
    passed = 0
    failed = 0

    for case in run_cases:
        success = test(case[0],case[1])
        if success:
            passed += 1
        else:
            failed += 1

    if failed == 0:
        print("\n============= PASS ==============")
    else:
        print("\n============= FAIL ==============")
        print(f"{passed} passed, {failed} failed")
    

main()