from __future__ import annotations

import argparse
import sys
from pathlib import Path

from src.engine import FunctionCallEngine

from src.io_utils import (
    InputFileError,
    load_function_definitions,
    load_prompts,
    write_json_results)

from src.models import FunctionCallResult

from src.vocabulary import load_vocabulary

DEFAULT_INPUT_DIR = Path("data/input")
DEFAULT_OUTPUT_PATH = Path("data/output/function_calling_results.json")
TESTS_FILENAME = "function_calling_tests.json"

DEFINITIONS_FILENAME_CANDIDATES = [
    "function_definitions.json",
    "functions_definition.json",
    "functions_definitions.json",
]
DEFAULT_MODEL_NAME = "Qwen/Qwen3-0.6B"


def _resolve_definitions_path(input_dir: Path) -> Path:
    for filename in DEFINITIONS_FILENAME_CANDIDATES:
        candidate = input_dir / filename
        if candidate.is_file():
            return candidate
    return input_dir / DEFINITIONS_FILENAME_CANDIDATES[0]


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="call-me-maybe",
        description="Translate natural language \
         prompts into structured function calls "
        "using an LLM constrained to always \
         emit valid, schema-compliant JSON.",
    )
    parser.add_argument(
        "--input",
        type=Path,
        default=DEFAULT_INPUT_DIR,
        help=f"Directory containing the input JSON files \
          (default: {DEFAULT_INPUT_DIR})",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT_PATH,
        help=f"Path where the JSON results will be written \
         (default: {DEFAULT_OUTPUT_PATH})",
    )
    parser.add_argument(
        "--model",
        default=DEFAULT_MODEL_NAME,
        help=f"Hugging Face model identifier to load \
             (default: {DEFAULT_MODEL_NAME})",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    tests_path: Path = args.input / TESTS_FILENAME
    definitions_path: Path = _resolve_definitions_path(args.input)

    try:
        functions = load_function_definitions(definitions_path)
        prompts = load_prompts(tests_path)
    except InputFileError as exc:
        print(f"[error] {exc}", file=sys.stderr)
        return 1

    if not prompts:
        print("[warning] No prompts to process,  \
            writing an empty output file.", file=sys.stderr)
        write_json_results(args.output, [])
        return 0

    try:
        from llm_sdk import Small_LLM_Model

        print(f"[info] Loading model '{args.model}'... this can take a while. \
               ", file=sys.stderr)
        model = Small_LLM_Model(model_name=args.model)
        vocabulary = load_vocabulary(model)
    except Exception as exc:  # noqa: BLE001 - we must never crash the CLI
        print(f"[error] Could not load the model \
              or its vocabulary: {exc}", file=sys.stderr)
        return 1

    engine = FunctionCallEngine(model, vocabulary)

    results: list[FunctionCallResult] = []
    for index, prompt in enumerate(prompts, start=1):
        print(f"[{index}/{len(prompts)}] {prompt}", file=sys.stderr)
        try:
            result = engine.run(prompt, functions)
            results.append(result)
            print(f"  -> {result.name} {result.parameters}", file=sys.stderr)
        except Exception as exc:  # noqa: BLE001 - keep proc remaining prompts
            print(f"[warning] Skipping prompt {prompt!r}: {exc} \
                  ", file=sys.stderr)

    write_json_results(args.output, results)
    print(
        f"[info] Wrote {len(results)}/{len(prompts)} results to {args.output}",
        file=sys.stderr,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
