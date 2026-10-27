from __future__ import annotations

import time
from typing import Optional

# pyrefly: ignore [missing-import]
from src.grammar import current_mode, is_complete, is_valid_prefix

# pyrefly: ignore [missing-import]
from src.models import FunctionDefinition

# pyrefly: ignore [missing-import]
from src.vocabulary import Vocabulary

MAX_GENERATION_STEPS = 200
REPETITION_PENALTY = 1.3


class GenerationError(Exception):
    """Raised when constrained decoding cannot produce a valid JSON output."""


def generate_function_call(
    model: object,
    vocabulary: Vocabulary,
    functions: list[FunctionDefinition],
    prompt_text: str,
    verbose: bool = False,
) -> str:
    """Generate a complete function-call JSON string
        using constrained decoding.

    Tokens are chosen one at a time; only tokens that keep the generated text
    as a valid prefix of the expected JSON schema are allowed.  Stops as soon
    as the generated text is a complete, valid JSON object.

    Returns the raw JSON string (e.g.
    '{"name":"fn_add","parameters":{"a":2,"b":3}}').
    Raises GenerationError if no valid JSON is produced
    within MAX_GENERATION_STEPS.
    """
    encode = getattr(model, "encode")
    input_ids: list[int] = encode(prompt_text)[0].tolist()
    generated_token_ids: list[int] = []
    generated_text = ""

    for step in range(MAX_GENERATION_STEPS):
        if is_complete(generated_text, functions):
            return generated_text

        step_start = time.time()
        next_token_id = _choose_next_token(
            model,
            vocabulary,
            functions,
            input_ids,
            generated_text,
            generated_token_ids
        )
        input_ids.append(next_token_id)
        generated_token_ids.append(next_token_id)
        generated_text += vocabulary.id_to_text[next_token_id] or ""

        if verbose:
            elapsed = time.time() - step_start
            print(f"    step {step}: {elapsed:.2f}s -> {generated_text!r}")

    raise GenerationError(
        f"No valid JSON produced after {MAX_GENERATION_STEPS} steps. "
        f"Generated so far: {generated_text!r}"
    )


def _apply_repetition_penalty(logit: float, already_used: bool) -> float:
    """Divide/multiply logit by REPETITION_PENALTY
        for tokens already generated."""
    if not already_used:
        return logit
    if logit > 0:
        return logit / REPETITION_PENALTY
    return logit * REPETITION_PENALTY


def _choose_next_token(
    model: object,
    vocabulary: Vocabulary,
    functions: list[FunctionDefinition],
    input_ids: list[int],
    generated_text: str,
    generated_token_ids: list[int],
) -> int:
    """Pick the highest-logit token that keeps generated_text a valid prefix.

    Inside a JSON string value (mode == 'string') we use two fast pre-computed
    lists instead of validating the full vocabulary every step:
      - plain_string_token_ids: safe without any prefix check
      - risky_string_token_ids: need per-candidate grammar validation

    Outside a string we filter by first character first, then validate.
    """
    get_logits = getattr(model, "get_logits_from_input_ids")
    logits: list[float] = get_logits(input_ids)
    already_used = set(generated_token_ids)

    best_token_id: Optional[int] = None
    best_adjusted_logit = float("-inf")

    mode = current_mode(generated_text, functions)

    if mode == "string":
        # Fast path: plain tokens are always valid inside a string.
        for token_id in vocabulary.plain_string_token_ids:
            adjusted = _apply_repetition_penalty(
                logits[token_id],
                token_id in already_used
            )
            if adjusted > best_adjusted_logit:
                best_adjusted_logit = adjusted
                best_token_id = token_id

        # Risky tokens (quotes, backslashes, control chars)
        # need full validation.
        for token_id in vocabulary.risky_string_token_ids:
            candidate_text = vocabulary.id_to_text[token_id]
            if not is_valid_prefix(
                generated_text + (candidate_text or ""),
                functions
            ):
                continue
            adjusted = _apply_repetition_penalty(
                logits[token_id],
                token_id in already_used
            )
            if adjusted > best_adjusted_logit:
                best_adjusted_logit = adjusted
                best_token_id = token_id
    else:
        # Outside a string: filter by 1st character, then validate full token.
        valid_first_chars = [
            char
            for char in vocabulary.first_char_to_ids
            if is_valid_prefix(generated_text + char, functions)
        ]
        for first_char in valid_first_chars:
            for token_id in vocabulary.first_char_to_ids[first_char]:
                candidate_text = vocabulary.id_to_text[token_id]
                if not is_valid_prefix(
                    generated_text + (candidate_text or ""),
                    functions
                ):
                    continue
                adjusted = _apply_repetition_penalty(
                    logits[token_id], token_id in already_used
                )
                if adjusted > best_adjusted_logit:
                    best_adjusted_logit = adjusted
                    best_token_id = token_id

    if best_token_id is None:
        raise GenerationError(
            f"No vocabulary token is valid after: {generated_text!r}"
        )

    return best_token_id
