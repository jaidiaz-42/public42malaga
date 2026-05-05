def secure_archive(filename: str, action: str = "read",
                   content: str = "") -> tuple[bool, str]:
    try:
        if action == "read":
            with open(filename, "r") as file:
                return (True, file.read())
        elif action == "write":
            with open(filename, "w") as file:
                file.write(content)
                return (True, "Content successfully written to file")
        return (False, "Invalid action")
    except Exception as e:
        return (False, f"[{e.args[0] if e.args else ''}] "
                f"{e.strerror if hasattr(e, 'strerror') else str(e)}: "
                f"'{filename}'")


def main() -> None:
    print("=== Cyber Archives Security ===\n")

    print("Using 'secure_archive' to read from a nonexistent file:")
    print(secure_archive("/not/existing/file", "read"))

    print("\nUsing 'secure_archive' to read from an inaccessible file:")
    print(secure_archive("/etc/shadow", "read"))

    print("\nUsing 'secure_archive' to read from a regular file:")
    print(secure_archive("ancient_fragment.txt", "read"))

    print("\nUsing 'secure_archive' to write previous content to a new file:")
    print(secure_archive("security_protocols.txt", "write",
                         "New security protocols archived"))


if __name__ == "__main__":
    main()
