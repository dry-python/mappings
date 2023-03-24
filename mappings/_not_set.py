from __future__ import annotations

from typing import Literal, TypeAlias
from enum import Enum


class _Sentinel(Enum):
    NOT_SET = object()


NOT_SET = _Sentinel.NOT_SET
NotSet: TypeAlias = Literal[_Sentinel.NOT_SET]
