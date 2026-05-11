import sys


def main() -> None:
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <file>")
        print()
        return

    filename: str = sys.argv[1]
    print("=== Cyber Archives Recovery & Preservation ===")
    print(f"Accessing file '{filename}'")

    try:
        file = open(filename, "r")
        lines: list[str] = file.readlines()
        print("---\n")
        for line in lines:
            print(line, end="")
        print("\n---")
        file.close()
        print(f"File '{filename}' closed.")

        print("\nTransform data:")
        print("---\n")
        transformed_content: str = ""
        for line in lines:
            new_line: str = line.rstrip("\n") + "#\n"
            transformed_content += new_line
            print(new_line, end="")
        print("\n---")

        dest_filename: str = input("Enter new file name (or empty): ")

        if dest_filename:
            print(f"Saving data to '{dest_filename}'")
            out_file = open(dest_filename, "w")
            out_file.write(transformed_content)
            out_file.close()
            print(f"Data saved in file '{dest_filename}'.")
            print()
        else:
            print("Not saving data.")

    except Exception as e:
        print(f"Error opening file '{filename}': {e}")


if __name__ == "__main__":
    main()
