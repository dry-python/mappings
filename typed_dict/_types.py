from __future__ import annotations

from dataclasses import Field
from typing import Any, ClassVar, Protocol


class TypedDictType(Protocol):
    """A class inherited from `typing_extensions.TypedDict`."""

    __required_keys__: ClassVar[frozenset[str]]
    __optional_keys__: ClassVar[frozenset[str]]
    __total__: ClassVar[bool]


class DataclassType(Protocol):
    """A class decorated with `@dataclasses.dataclass`."""

    __dataclass_fields__: ClassVar[dict[str, Field[Any]]]  # noqa: WPS234
