from __future__ import annotations

# pyrefly: ignore [missing-import]
from src.models import FunctionDefinition


class _NeedMoreInput(Exception):
    """Raised when the text is a valid prefix but the JSON
      is not yet complete."""


class _GrammarReject(Exception):
    """Raised when the text violates the expected JSON grammar."""


class _Parser:
    """Incremental parser for the JSON structure:

        {"name":"<function_name>","parameters":{<param>:<value>,...}}

    Consumes the accumulated generated text character by character and tracks
    the current parsing mode so the constrained decoder knows which tokens are
    valid at each step.
    """

    def __init__(self, text: str, functions: list[FunctionDefinition]) -> None:
        self.text = text
        self.pos = 0
        self.functions = functions
        self.mode = "literal"

    def parse(self) -> None:
        self._consume_literal('{"name":"')
        function = self._consume_function_name()
        self._consume_literal(',"parameters":{')
        self._consume_args(function)
        self._consume_literal("}}")
        if self.pos != len(self.text):
            raise _GrammarReject()

    # -- literal segments ------------------------------------------------

    def _consume_literal(self, literal: str) -> None:
        self.mode = "literal"
        for expected_char in literal:
            if self.pos >= len(self.text):
                raise _NeedMoreInput()
            if self.text[self.pos] != expected_char:
                raise _GrammarReject()
            self.pos += 1

    # -- function name ---------------------------------------------------

    def _consume_function_name(self) -> FunctionDefinition:
        self.mode = "function_name"
        names = [fn.name for fn in self.functions]
        start = self.pos

        while True:
            current = self.text[start:self.pos]

            # If the next char is a closing quote and the accumulated text
            # is a known function name, we are done.
            if (
                self.pos < len(self.text)
                and self.text[self.pos] == '"'
                and current in names
            ):
                self.pos += 1
                return self._function_by_name(current)

            if self.pos >= len(self.text):
                raise _NeedMoreInput()

            candidate = current + self.text[self.pos]
            if not any(name.startswith(candidate) for name in names):
                raise _GrammarReject()
            self.pos += 1

    def _function_by_name(self, name: str) -> FunctionDefinition:
        for fn in self.functions:
            if fn.name == name:
                return fn
        raise _GrammarReject()

    # -- parameter list --------------------------------------------------

    def _consume_args(self, function: FunctionDefinition) -> None:
        params = list(function.parameters.items())
        for index, (param_name, param_spec) in enumerate(params):
            prefix = ("" if index == 0 else ",") + f'"{param_name}":'
            self._consume_literal(prefix)
            self._consume_value(param_spec.type)

    def _consume_value(self, value_type: str) -> None:
        if value_type == "string":
            self._consume_string_value()
        elif value_type in ("number", "integer"):
            self._consume_number_value()
        elif value_type == "boolean":
            self._consume_boolean_value()
        else:
            # Unknown type: treat as string.
            self._consume_string_value()

    # -- value parsers ---------------------------------------------------

    def _consume_string_value(self) -> None:
        self._consume_literal('"')
        self.mode = "string"
        while True:
            if self.pos >= len(self.text):
                raise _NeedMoreInput()
            char = self.text[self.pos]
            if char == '"':
                self.pos += 1
                return
            if char == "\\":
                self._consume_escape_sequence()
                continue
            if ord(char) < 0x20:
                raise _GrammarReject()
            self.pos += 1

    def _consume_escape_sequence(self) -> None:
        self.pos += 1  # skip the backslash
        if self.pos >= len(self.text):
            raise _NeedMoreInput()

        escape_char = self.text[self.pos]
        if escape_char in '"\\/bfnrt':
            self.pos += 1
            return

        if escape_char == "u":
            self.pos += 1
            for _ in range(4):
                if self.pos >= len(self.text):
                    raise _NeedMoreInput()
                if self.text[self.pos] not in "0123456789abcdefABCDEF":
                    raise _GrammarReject()
                self.pos += 1
            return

        raise _GrammarReject()

    def _consume_number_value(self) -> None:
        if self.pos < len(self.text) and self.text[self.pos] == "-":
            self.pos += 1

        digit_count = 0
        while self.pos < len(self.text) and self.text[self.pos].isdigit():
            self.pos += 1
            digit_count += 1

        if digit_count == 0:
            if self.pos >= len(self.text):
                raise _NeedMoreInput()
            raise _GrammarReject()

        # Optional fractional part.
        if self.pos < len(self.text) and self.text[self.pos] == ".":
            self.pos += 1
            frac_digits = 0
            while self.pos < len(self.text) and self.text[self.pos].isdigit():
                self.pos += 1
                frac_digits += 1
            if frac_digits == 0:
                if self.pos >= len(self.text):
                    raise _NeedMoreInput()
                raise _GrammarReject()

    def _consume_boolean_value(self) -> None:
        if self.pos >= len(self.text):
            raise _NeedMoreInput()
        if self.text[self.pos] == "t":
            self._consume_literal("true")
        elif self.text[self.pos] == "f":
            self._consume_literal("false")
        else:
            raise _GrammarReject()


# ---------------------------------------------------------------------------
# Public API used by the constrained decoder
# ---------------------------------------------------------------------------

def current_mode(text: str, functions: list[FunctionDefinition]) -> str:
    """Return the parser mode at the end of *text*
        (e.g. 'string', 'literal')."""
    parser = _Parser(text, functions)
    try:
        parser.parse()
    except (_NeedMoreInput, _GrammarReject):
        pass
    return parser.mode


def is_valid_prefix(text: str, functions: list[FunctionDefinition]) -> bool:
    """True if *text* is a valid prefix of some accepted JSON string."""
    parser = _Parser(text, functions)
    try:
        parser.parse()
    except _NeedMoreInput:
        return True
    except _GrammarReject:
        return False
    return True


def is_complete(text: str, functions: list[FunctionDefinition]) -> bool:
    """True if *text* is a complete, valid function-call JSON."""
    parser = _Parser(text, functions)
    try:
        parser.parse()
    except (_NeedMoreInput, _GrammarReject):
        return False
    return True
