"""Type-safe `dataclass.replace`.

This example shows how you can make a type-safe version of `dataclass.replace`
that will report if you try passing an argument that isn't a valid dataclass field
or has invalid type.
"""
from __future__ import annotations

import dataclasses

from typing_extensions import Unpack

import typed_dict


@dataclasses.dataclass
class _User:
    name: str
    age: int = 99


UserDict = typed_dict.from_dataclass(_User)


class User(_User):
    # The `Unpack` support in mypy is experimental, so you need to run mypy with
    # `--enable-incomplete-feature=Unpack` for it to work.
    def evolve(self, **kwargs: Unpack[UserDict]) -> User:
        """Create a copy of User with the given fields replaced."""
        return dataclasses.replace(self, **kwargs)


user = User(name='Aragorn')
user = user.evolve(age=88)  # noqa: WPS432
