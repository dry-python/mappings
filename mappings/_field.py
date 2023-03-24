from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Generic, TypeVar
from ._not_set import NOT_SET, NotSet


T = TypeVar('T')


@dataclass
class Field(Generic[T]):
    default: T | NotSet
    default_factory: Callable[[], T] | NotSet
    required: bool | None
    name: str | None = None

    def __set_name__(self, owner: object, name: str) -> None:
        self.name = name

    def get_default(self) -> T | NotSet:
        if self.default_factory is not NOT_SET:
            return self.default_factory()
        return self.default


def field(
    *,
    default: T | NotSet = NOT_SET,
    default_factory: Callable[[], T] | NotSet = NOT_SET,
    required: bool | None = None,
) -> T:
    return Field(  # type: ignore[return-value]
        default=default,
        default_factory=default_factory,
        required=required,
    )
