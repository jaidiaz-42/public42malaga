import sys
import os
import site
import sysconfig


def is_virtual_env() -> bool:
    return hasattr(sys, 'real_prefix') or (
        hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix
    )


def main() -> None:
    in_venv = is_virtual_env()
    current_python = sys.executable

    if not in_venv:
        print("Outside the Matrix")
        print("MATRIX STATUS: You're still plugged in\n")
        print(f"Current Python: {current_python}")
        print("Virtual Environment: None detected\n")
        print("WARNING: You're in the global environment!")
        print("The machines can see everything you install.\n")
        print("To enter the construct, run:")
        print("python -m venv matrix_env")
        print("source matrix_env/bin/activate # On Unix")
        print("matrix_env\\Scripts\\activate # On Windows\n")
        print("Then run this program again.")
    else:
        env_path = sys.prefix
        env_name = os.path.basename(env_path)
        try:
            site_packages = site.getsitepackages()[0]
        except AttributeError:
            site_packages = sysconfig.get_path('purelib')

        print("Inside the Construct\n")
        print("MATRIX STATUS: Welcome to the construct\n")
        print(f"Current Python: {current_python}")
        print(f"Virtual Environment: {env_name}")
        print(f"Environment Path: {env_path}\n")
        print("SUCCESS: You're in an isolated environment!")
        print("Safe to install packages without affecting")
        print("the global system.\n")
        print("Package installation path:")
        print(site_packages)


if __name__ == "__main__":
    main()
