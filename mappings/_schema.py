from __future__ import annotations
from dataclasses import dataclass
from typing import Callable, TypeVar, overload


T = TypeVar('T', bound=type)
META_ATTR = '__mappings_meta'


@dataclass(frozen=True)
class Meta:
    total: bool

    @staticmethod
    def get(target: type) -> Meta:
        return getattr(target, META_ATTR)

    def set(self, target: type) -> None:
        return setattr(target, META_ATTR, self)


@overload
def schema(
    model: None = None,
    *,
    total: bool = True,
) -> Callable[[T], T]:
    pass


@overload
def schema(
    model: T,
    *,
    total: bool = True,
) -> T:
    pass


def schema(
    model: T | None = None,
    *,
    total: bool = True,
) -> T | Callable[[T], T]:
    if model is not None:
        meta = Meta(total=total)
        meta.set(model)
        return model

    def wrapper(model: T) -> T:
        meta = Meta(total=total)
        meta.set(model)
        return model

    return wrapper
