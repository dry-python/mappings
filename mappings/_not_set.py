from __future__ import annotations

from typing import TYPE_CHECKING, Literal
from enum import Enum

if TYPE_CHECKING:
    from typing import TypeAlias


class _Sentinel(Enum):
    NOT_SET = object()


NOT_SET = _Sentinel.NOT_SET
NotSet: TypeAlias = Literal[_Sentinel.NOT_SET]
