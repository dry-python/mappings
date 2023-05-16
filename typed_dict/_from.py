from __future__ import annotations

import dataclasses
import inspect
from types import FunctionType
from typing import Any

from typing_extensions import NotRequired, TypedDict

from ._types import DataclassType, TypedDictType


def from_function(
    func: FunctionType,
    *,
    total: bool = True,
    skip_self: bool = False,
) -> type[TypedDictType]:
    """Generate TypedDict from a function signature.

    Parameters
    ----------
    func
        the function to convert.
    total
        set to False to make all fields optional.
    skip_self
        don't include the first function argument
        (if called ``self`` or ``cls``).

    Returns
    -------
    TypedDictType
        The generated TypedDict subclass.
    """
    sig = inspect.Signature.from_callable(func)
    fields: dict[str, object] = {}
    for name, func_param in sig.parameters.items():
        if skip_self and name in {'self', 'cls'}:
            continue
        skip_self = False  # self may come only on the first position
        fields[name] = _get_func_field_type(func_param)
    return TypedDict(
        func.__name__,  # type: ignore[operator]
        fields,
        total=total,
    )


def _get_func_field_type(func_param: inspect.Parameter) -> object:
    field_type: object = func_param.annotation
    if field_type is func_param.empty:
        field_type = Any
    if func_param.default is not func_param.empty:
        field_type = NotRequired[field_type]  # pyright: ignore
    return field_type


# TODO: `recursive` flag.
def from_dataclass(
    schema: type[DataclassType],
    *,
    total: bool = True,
    init: bool = False,
) -> type[TypedDictType]:
    """Generate TypedDict from a dataclass.

    Parameters
    ----------
    schema
        the dataclass to convert.
    total
        set to False to make all fields optional.
    init
        only include fields present in ``__init__``.

    Returns
    -------
    TypedDictType
        The generated TypedDict subclass.
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
