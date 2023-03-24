from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Callable, Generic, Mapping, TypeVar, overload


T = TypeVar('T', bound=type)


@dataclass
class Schema(Generic[T]):
    model: T
    total: bool

    @classmethod
    def cast(cls, data: Mapping[str, Any]) -> Mapping[str, Any]:
        return data


@overload
def schema(
    model: None = None,
    *,
    total: bool = True,
) -> Callable[[T], Schema[T]]:
    pass


@overload
def schema(
    model: T,
    *,
    total: bool = True,
) -> Schema[T]:
    pass


def schema(
    model: T | None = None,
    *,
    total: bool = True,
) -> Schema[T] | Callable[[T], Schema[T]]:
    if model is not None:
        return Schema(model=model, total=total)

    def wrapper(model: T) -> Schema[T]:
        return Schema(model=model, total=total)
    return wrapper
