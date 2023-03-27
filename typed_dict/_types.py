from __future__ import annotations

from dataclasses import Field
from typing import Any, ClassVar, Protocol


class TypedDictType(Protocol):
    __required_keys__: ClassVar[frozenset[str]]
    __optional_keys__: ClassVar[frozenset[str]]
    __total__: ClassVar[bool]


class DataclassType(Protocol):
    __dataclass_fields__: ClassVar[dict[str, Field[Any]]]
