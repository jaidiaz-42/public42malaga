from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class ParameterSpec(BaseModel):
    """Describes a single parameter of a callable function."""

    type: str


class FunctionDefinition(BaseModel):
    """A single entry of ``function_definitions.json``."""

    name: str
    description: str
    parameters: dict[str, ParameterSpec] = Field(default_factory=dict)
    returns: ParameterSpec | None = None


class FunctionCallResult(BaseModel):
    """A single entry of the output file."""

    prompt: str
    name: str
    parameters: dict[str, Any] = Field(default_factory=dict)
