import sys


def main() -> None:
    if len(sys.argv) != 2:
        sys.stdout.write(f"Usage: {sys.argv[0]} <file>\n")
        return

    filename: str = sys.argv[1]
    sys.stdout.write("=== Cyber Archives Recovery & Preservation ===\n")
    sys.stdout.write(f"Accessing file '{filename}'\n")

    try:
        file = open(filename, "r")
        lines: list[str] = file.readlines()
        for line in lines:
            sys.stdout.write(line)
        file.close()
        sys.stdout.write(f"File '{filename}' closed.\n")

        sys.stdout.write("\nTransform data:\n")
        transformed_content: str = ""
        for line in lines:
            new_line: str = line.rstrip("\n") + "#\n"
            transformed_content += new_line
            sys.stdout.write(new_line)

        sys.stdout.write("Enter new file name (or empty): ")
        sys.stdout.flush()
        dest_filename: str = sys.stdin.readline().strip()

        if dest_filename:
            sys.stdout.write(f"Saving data to '{dest_filename}'\n")
            try:
                out_file = open(dest_filename, "w")
                out_file.write(transformed_content)
                out_file.close()
                sys.stdout.write(f"Data saved in file '{dest_filename}'.\n")
            except Exception as e:
                sys.stderr.write(f"[STDERR] Error opening file "
                                 f"'{dest_filename}': {e}\n")
                sys.stdout.write("Data not saved.\n")
        else:
            sys.stdout.write("Not saving data.\n")

    except Exception as e:
        sys.stderr.write(f"[STDERR] Error opening file '{filename}': {e}\n")


if __name__ == "__main__":
    main()
