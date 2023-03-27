from __future__ import annotations
import dataclasses
import inspect
from types import FunctionType
from typing import Any, TypedDict
from typed_dict._types import DataclassType, TypedDictType

from typing_extensions import NotRequired


def from_function(
    func: FunctionType,
    *,
    total: bool = True,
    skip_self: bool = False,
) -> type[TypedDictType]:
    """Generate TypedDict from a function signature.
    """
    sig = inspect.Signature.from_callable(func)
    fields: dict[str, object] = {}
    for name, param in sig.parameters.items():
        if skip_self and name in ('self', 'cls'):
            continue
        skip_self = False  # self may come only on the first position
        field_type: object = param.annotation
        if field_type is param.empty:
            field_type = Any
        if param.default is not param.empty:
            field_type = NotRequired[field_type]  # pyright: ignore
        fields[name] = field_type
    return TypedDict(
        func.__name__,  # type: ignore[operator]
        fields,
        total=total,
    )


# TODO: `recursive` flag.
def from_dataclass(
    schema: type[DataclassType],
    *,
    total: bool = True,
    init: bool = False,
) -> type[TypedDictType]:
    """Generate TypedDict from a dataclass.

    Args:
        schema: the dataclass to convert.
        total: set to False to make all fields optional.
        init: only include fields present in ``__init__``.

    """
    fields: dict[str, object] = {}
    for field in dataclasses.fields(schema):
        if init and not field.init:
            continue
        field_type: object = field.type
        if total and _dataclass_field_has_default(field):
            field_type = NotRequired[field_type]  # pyright: ignore
        fields[field.name] = field_type
    return TypedDict(
        schema.__name__,  # type: ignore[operator]
        fields,
        total=total,
    )


def _dataclass_field_has_default(field: dataclasses.Field[object]) -> bool:
    if field.default is not dataclasses.MISSING:
        return True
    return field.default_factory is not dataclasses.MISSING
