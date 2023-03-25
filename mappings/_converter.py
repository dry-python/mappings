from __future__ import annotations
from typing import TypedDict
import dataclasses


def is_typed_dict(schema: type) -> bool:
    return hasattr(schema, '__required_keys__')


def as_typed_dict(schema: type, total: bool = True) -> type:
    if is_typed_dict(schema):
        return schema

    if dataclasses.is_dataclass(schema):
        fields: dict[str, type] = {}
        for field in dataclasses.fields(schema):
            fields[field.name] = field.type
        return TypedDict(schema.__name__, fields, total=total)  # type: ignore

    raise TypeError('unsupported schema')
