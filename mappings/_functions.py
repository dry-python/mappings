from __future__ import annotations
from typing import Any, Mapping, TypedDict
import dataclasses


def cast(schema: type, value: Mapping[str, Any]) -> Mapping[str, Any]:
    return value


def validate(schema: type, value: Mapping[str, Any]) -> Mapping[str, Any]:
    ...
    return value
