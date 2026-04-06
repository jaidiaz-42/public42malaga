def garden_operations() -> None:
    print("=== Garden Error Types Demo ===\n")
    try:
        print("Testing ValueError...")
        int("abc")
    except ValueError:
        print("Caught ValueError: invalid literal for int()\n")
    try:
        print("Testing ZeroDivisionError...")
        10 / 0
    except ZeroDivisionError:
        print("Caught ZeroDivisionError: division by zero\n")
    try:
        print("Testing FileNotFoundError...")
        open("missing.txt")
    except FileNotFoundError as e:
        print(f"Caught FileNotFoundError: {e}\n")
    try:
        print("Testing KeyError...")
        data: dict = {}
        data["missing_plant"]
    except KeyError as e:
        print(f"Caught KeyError: '{e}'\n")
    try:
        print("Testing multiple errors together...")
        int("abc")
        10/0
        open("missing_text.txt")
    except (ValueError, ZeroDivisionError, FileNotFoundError):
        print("Caught an error, but the program continues!\n")
    print("All error types tested succesfully")


if __name__ == "__main__":
    garden_operations()
