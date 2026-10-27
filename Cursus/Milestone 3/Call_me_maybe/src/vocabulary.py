from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path
from typing import Optional


EOS_TOKEN_CONTENT = "<|endoftext|>"


@lru_cache(maxsize=1)
def _byte_to_unicode_map() -> dict[int, str]:
    """GPT-2 / Qwen byte-level BPE mapping: byte -> unicode character."""
    printable_ranges = (
        list(range(ord("!"), ord("~") + 1))
        + list(range(ord("¡"), ord("¬") + 1))
        + list(range(ord("®"), ord("ÿ") + 1))
    )
    byte_values = printable_ranges[:]
    unicode_points = printable_ranges[:]

    extra_index = 0
    for byte_value in range(256):
        if byte_value not in byte_values:
            byte_values.append(byte_value)
            unicode_points.append(256 + extra_index)
            extra_index += 1

    return {byte: chr(point) for byte, point in zip(
        byte_values,
        unicode_points
        )}


@lru_cache(maxsize=1)
def _unicode_to_byte_map() -> dict[str, int]:
    return {char: byte for byte, char in _byte_to_unicode_map().items()}


def token_to_text(token: str) -> Optional[str]:
    """Decode a raw BPE token string into the UTF-8 text it represents.

    Returns None if the token maps to an invalid UTF-8 byte sequence.
    Returns the token unchanged if it is a special token (e.g. <|endoftext|>).
    """
    unicode_to_byte = _unicode_to_byte_map()

    try:
        raw_bytes = bytes(unicode_to_byte[char] for char in token)
    except KeyError:
        # Special token: not part of the byte-level alphabet.
        return token

    try:
        return raw_bytes.decode("utf-8")
    except UnicodeDecodeError:
        return None


def _is_safe_inside_string(text: str) -> bool:
    """True if the token contains no characters
        that need escaping in a JSON string."""
    return all(char not in '"\\' and ord(char) >= 0x20 for char in text)


class Vocabulary:
    """Full id <-> text mapping with precomputed lookup
        structures for fast decoding."""

    def __init__(
        self,
        id_to_token: dict[int, str],
        id_to_text: dict[int, Optional[str]],
        eos_token_id: int,
    ) -> None:
        self.id_to_token = id_to_token
        self.id_to_text = id_to_text
        self.eos_token_id = eos_token_id
        self.size = len(id_to_token)

        # Precomputed lookup structures used by the constrained decoder.
        self.first_char_to_ids: dict[str, list[int]] = {}
        self.plain_string_token_ids: list[int] = []   # safe inside a JSON
        self.risky_string_token_ids: list[int] = []   # need per validation

        for token_id, text in id_to_text.items():
            if not text or token_id == eos_token_id:
                continue
            first_char = text[0]
            self.first_char_to_ids.setdefault(first_char, []).append(token_id)

            if _is_safe_inside_string(text):
                self.plain_string_token_ids.append(token_id)
            else:
                self.risky_string_token_ids.append(token_id)


def load_vocabulary(model: object) -> Vocabulary:
    """Build a Vocabulary from the model's tokenizer.json file."""
    get_path = getattr(model, "get_path_to_tokenizer_file")
    path = Path(get_path())
    with open(path, "r", encoding="utf-8") as file:
        data: dict[str, object] = json.load(file)

    model_section = data["model"]
    assert isinstance(model_section, dict)
    raw_vocab: dict[str, int] = model_section[
        "vocab"
        ]

    id_to_token: dict[int, str] = {
        token_id: token for token, token_id in raw_vocab.items()
    }

    eos_token_id: Optional[int] = None
    added_tokens = data.get("added_tokens", [])
    assert isinstance(added_tokens, list)
    for added_token in added_tokens:
        assert isinstance(added_token, dict)
        id_to_token[added_token["id"]] = added_token["content"]
        if added_token["content"] == EOS_TOKEN_CONTENT:
            eos_token_id = added_token["id"]

    if eos_token_id is None:
        raise ValueError(
            f"EOS token {EOS_TOKEN_CONTENT!r} not \
                found in tokenizer file at {path}"
        )

    id_to_text: dict[int, Optional[str]] = {
        token_id: token_to_text(token) for (
            token_id,
            token
            ) in id_to_token.items()
    }

    return Vocabulary(
        id_to_token=id_to_token,
        id_to_text=id_to_text,
        eos_token_id=eos_token_id,
    )
