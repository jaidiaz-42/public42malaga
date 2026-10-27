from __future__ import annotations

import json
from typing import Any

# pyrefly: ignore [missing-import]
from src.generator import GenerationError, generate_function_call

# pyrefly: ignore [missing-import]
from src.models import FunctionCallResult, FunctionDefinition

# pyrefly: ignore [missing-import]
from src.vocabulary import Vocabulary


def _format_function(function: FunctionDefinition) -> str:
    """Format a single FunctionDefinition as a human-readable text block."""
    if function.parameters:
        params_text = ", ".join(
            f"{param_name}: {param_spec.type}"
            for param_name, param_spec in function.parameters.items()
        )
    else:
        params_text = "(no parameters)"

    returns_text = function.returns.type if function.returns else "unknown"

    return (
        f"- {function.name}({params_text}) -> {returns_text}\n"
        f"  Description: {function.description}"
    )


def build_prompt(user_prompt: str, functions: list[FunctionDefinition]) -> str:
    """Build the full prompt sent to the LLM for each user request."""
    functions_text = "\n".join(_format_function(fn) for fn in functions)

    worked_example = (
        "Full format example (invented function just \
            to show the expected shape; "
        "never choose this function for real, always \
            use one from the catalog above):\n"
        'Example request: "Replace every digit with X \
            in \'I have 2 cats and 10 dogs\'"\n'
        'Example response: {"name":"fn_example_replace\
            ","parameters":{"text":"I have 2 cats '
        'and 10 dogs","pattern":"\\\\d+","replacement":"X"}}\n'
        "Note two things: (1) the pattern \\\\d+ (with \
            doubled backslash) represents "
        '"one or more digits"; (2) even though the text \
            contains numbers, the request '
        "asked to REPLACE, not to sum or calculate anything \
            — always choose the function "
        "based on the action requested, not based on the data present."
    )

    return (
        "You are a system that translates natural language requests \
            into function calls. "
        "You have the following functions available:\n\n"
        f"{functions_text}\n\n"
        "Your task is to choose the most suitable function to resolve \
            the user's request "
        "and provide the correct arguments with the correct types.\n\n"
        f"{worked_example}\n\n"
        f"User request: {user_prompt}\n\n"
        'Respond only with a JSON object of the form '
        '{"name": "<function_name>", "parameters": {<arguments>}}.'
    )


class FunctionCallEngine:
    """Orchestrates prompt building, constrained
        decoding and result parsing."""

    def __init__(self, model: object, vocabulary: Vocabulary) -> None:
        self._model = model
        self._vocabulary = vocabulary

    def run(
        self, prompt: str, functions: list[FunctionDefinition]
    ) -> FunctionCallResult:
        """Translate *prompt* into a FunctionCallResult
            using constrained generation."""
        prompt_text = build_prompt(prompt, functions)

        raw_json = generate_function_call(
            self._model, self._vocabulary, functions, prompt_text
        )

        parsed: dict[str, Any] = json.loads(raw_json)
        return FunctionCallResult(
            prompt=prompt,
            name=parsed["name"],
            parameters=parsed["parameters"],
        )


__all__ = ["FunctionCallEngine", "build_prompt", "GenerationError"]
