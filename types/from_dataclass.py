from __future__ import annotations

from dataclasses import dataclass

import typed_dict


@dataclass
class User:
    name: str
    age: int = 99


UDict = typed_dict.from_dataclass(User)

_1: UDict = {'name': 'aragorn', 'age': 88}
_2: UDict = {'name': 'aragorn', 'age': 88}
# E: Incompatible types (expression has type "int", TypedDict item "name" has type "str")
_3: UDict = {'name': 88}
# E: Incompatible types (expression has type "str", TypedDict item "age" has type "int")
_4: UDict = {'name': 'aragorn', 'age': 'idk'}
