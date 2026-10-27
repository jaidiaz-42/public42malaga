from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from pydantic import ValidationError

# pyrefly: ignore [missing-import]
from src.models import FunctionCallResult, FunctionDefinition


class InputFileError(Exception):
    """Raised when an input file cannot be read or parsed."""


def _read_json(path: Path) -> Any:
    if not path.is_file():
        raise InputFileError(f"File not found: {path}")
    try:
        with open(path, "r", encoding="utf-8") as handle:
            return json.load(handle)
    except json.JSONDecodeError as exc:
        raise InputFileError(f"Invalid JSON in {path}: {exc}") from exc
    except OSError as exc:
        raise InputFileError(f"Could not read {path}: {exc}") from exc


def load_function_definitions(path: Path) -> list[FunctionDefinition]:
    """Load and validate the function definitions file."""
    raw = _read_json(path)
    if not isinstance(raw, list):
        raise InputFileError(
            f"{path} must contain a JSON array of function definitions"
        )

    definitions: list[FunctionDefinition] = []
    for index, entry in enumerate(raw):
        try:
            definitions.append(FunctionDefinition.model_validate(entry))
        except ValidationError as exc:
            raise InputFileError(
                f"Invalid function definition at \
                    index {index} in {path}: {exc}"
            ) from exc

    if not definitions:
        raise InputFileError(
            f"{path} does not contain any function definitions"
        )
    return definitions


def load_prompts(path: Path) -> list[str]:
    """Load the natural language prompts file.

    Accepts both a plain array of strings and an array of objects with a
    'prompt' key, for compatibility with both formats.
    """
    raw = _read_json(path)
    if not isinstance(raw, list):
        raise InputFileError(f"{path} must contain a JSON array of prompts")

    prompts: list[str] = []
    for index, entry in enumerate(raw):
        if isinstance(entry, str):
            prompts.append(entry)
        elif isinstance(entry, dict) and isinstance(entry.get("prompt"), str):
            prompts.append(entry["prompt"])
        else:
            raise InputFileError(
                f"Invalid prompt entry at index {index} in {path}: {entry!r}"
            )
    return prompts


def write_json_results(path: Path, results: list[FunctionCallResult]) -> None:
    """Serialize a list of FunctionCallResult models to a JSON file."""
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = [item.model_dump() for item in results]
    with open(path, "w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2, ensure_ascii=False)
        handle.write("\n")
