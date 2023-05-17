from __future__ import annotations

from dataclasses import dataclass

import pydantic

import typed_dict


@dataclass
class User:
    name: str
    age: int = 99


UserDict = typed_dict.from_dataclass(User)

res = pydantic.parse_obj_as(UserDict, {'name': 'Aragorn'})
assert res == {'name': 'Aragorn'}
