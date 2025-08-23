from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.write_file import write_file

run_cases_info = [
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

run_cases_content = [
    (
        ["calculator", "main.py"],
        """import sys
from pkg.calculator import Calculator
from pkg.render import render


def main():
    calculator = Calculator()
    if len(sys.argv) <= 1:
        print("Calculator App")
        print('Usage: python main.py "<expression>"')
        print('Example: python main.py "3 + 5"')
        return

    expression = " ".join(sys.argv[1:])
    try:
        result = calculator.evaluate(expression)
        to_print = render(expression, result)
        print(to_print)
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()"""
    ),
    (
        ["calculator", "pkg/calculator.py"],
        """class Calculator:
    def __init__(self):
        self.operators = {
            "+": lambda a, b: a + b,
            "-": lambda a, b: a - b,
            "*": lambda a, b: a * b,
            "/": lambda a, b: a / b,
        }
        self.precedence = {
            "+": 1,
            "-": 1,
            "*": 2,
            "/": 2,
        }

    def evaluate(self, expression):
        if not expression or expression.isspace():
            return None
        tokens = expression.strip().split()
        return self._evaluate_infix(tokens)

    def _evaluate_infix(self, tokens):
        values = []
        operators = []

        for token in tokens:
            if token in self.operators:
                while (
                    operators
                    and operators[-1] in self.operators
                    and self.precedence[operators[-1]] >= self.precedence[token]
                ):
                    self._apply_operator(operators, values)
                operators.append(token)
            else:
                try:
                    values.append(float(token))
                except ValueError:
                    raise ValueError(f"invalid token: {token}")

        while operators:
            self._apply_operator(operators, values)

        if len(values) != 1:
            raise ValueError("invalid expression")

        return values[0]

    def _apply_operator(self, operators, values):
        if not operators:
            return

        operator = operators.pop()
        if len(values) < 2:
            raise ValueError(f"not enough operands for operator {operator}")

        b = values.pop()
        a = values.pop()
        values.append(self.operators[operator](a, b))"""
    ),
    (
        ["calculator", "/bin/cat"],
        'Error: Cannot read "/bin/cat" as it is outside the permitted working directory'
    ),
    (
        ["calculator", "pkg/does_not_exist.py"],
        'Error: File not found or is not a regular file: "pkg/does_not_exist.py"'
    ),
]

run_cases_write = [
    (
        ["calculator", "lorem.txt", "wait, this isn't lorem ipsum"],
        f'Successfully wrote to "lorem.txt" (28 characters written)'
    ),
    (
        ["calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet"],
        f'Successfully wrote to "pkg/morelorem.txt" (26 characters written)'
    ),
    (
        ["calculator", "/tmp/temp.txt", "this should not be allowed"],
        'Error: Cannot write to "/tmp/temp.txt" as it is outside the permitted working directory'
    )
]



def test_info(input1, expected_output):
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


def test_content(input, expected_output):

    print(f"/n===============")
    print(f"input {input}")
    print(f"EXPECTED\n{expected_output}")

    result = get_file_content(*input)
    print(f"ACTUAL\n{result}")
    if (result != expected_output):
        print("FAILED TEST")
    else:
        print("SUCCESS TEST")
    return result == expected_output

def test_write(input, expected_output):
    print(f"/n===============")
    print(f"input {input}")
    print(f"EXPECTED\n{expected_output}")

    result = write_file(*input)
    print(f"ACTUAL\n{result}")
    if (result != expected_output):
        print("FAILED TEST")
    else:
        print("SUCCESS TEST")
    return result == expected_output

def main():
    passed = 0
    failed = 0

    for case in run_cases_write:
        success = test_write(case[0],case[1])
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