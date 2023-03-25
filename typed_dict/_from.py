from __future__ import annotations
import dataclasses
from typing import TypedDict
from ._types import DataclassType, TypedDictType

from typing_extensions import NotRequired


def from_dataclass(
    schema: type[DataclassType],
    total: bool = True,
) -> type[TypedDictType]:
    fields: dict[str, object] = {}
    for field in dataclasses.fields(schema):
        field_type: object = field.type
        if total and _dataclass_field_has_default(field):
            field_type = NotRequired[field_type]  # pyright: ignore
        fields[field.name] = field_type
    return TypedDict(schema.__name__, fields, total=total)  # type: ignore[operator]


def _dataclass_field_has_default(field: dataclasses.Field[object]) -> bool:
    if field.default is not dataclasses.MISSING:
        return True
    return field.default_factory is not dataclasses.MISSING
