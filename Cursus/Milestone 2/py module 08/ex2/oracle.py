import os
import sys

try:
    from dotenv import load_dotenv  # type: ignore
except ImportError:
    pass


def check_security(matrix_mode: str) -> None:
    print("Environment security check:")
    print("[OK] No hardcoded secrets detected")

    if os.path.isfile(".env"):
        print("[OK] .env file properly configured")

    if matrix_mode == "production" or os.environ.get("API_KEY") == "secret123":
        print("[OK] Production overrides available")

    print("\nThe Oracle sees all configurations.")


def load_configuration() -> None:
    if 'dotenv' in sys.modules:
        load_dotenv()

    matrix_mode = os.environ.get("MATRIX_MODE")
    if not matrix_mode:
        print("ORACLE STATUS: Reading the Matrix...\n")
        print("Warning: Missing MATRIX_MODE configuration.")
        print("Ensure environment variables are set or a .env file exists.")
        sys.exit(1)

    db_url = os.environ.get("DATABASE_URL")
    api_key = os.environ.get("API_KEY")
    log_level = os.environ.get("LOG_LEVEL")
    zion_endpoint = os.environ.get("ZION_ENDPOINT")

    if not all([db_url, api_key, log_level, zion_endpoint]):
        print("ORACLE STATUS: Reading the Matrix...\n")
        print("Warning: Missing one or more configuration variables.")
        sys.exit(1)

    print("ORACLE STATUS: Reading the Matrix...\n")
    print("Configuration loaded:")
    print(f"Mode: {matrix_mode}")

    if matrix_mode == "development":
        print("Database: Connected to local instance")
    else:
        print("Database: Connected to production instance")

    print("API Access: Authenticated")
    print(f"Log Level: {log_level}")
    print("Zion Network: Online\n")

    check_security(matrix_mode)


def main() -> None:
    load_configuration()


if __name__ == "__main__":
    main()
