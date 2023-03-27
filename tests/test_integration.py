from __future__ import annotations

from dataclasses import dataclass

import pydantic
import pytest

import typed_dict


@dataclass
class User:
    name: str
    age: int = 99


ok = True


@pytest.mark.parametrize('given, expected_ok', [
    ({'name': 'Aragorn'}, ok),
    ({'name': 'Aragorn', 'age': 88}, ok),

    ({}, not ok),
    ({'age': 88}, not ok),
    ({'name': 'Aragorn', 'age': 'idk'}, not ok),
])
def test_pydantic_validation(given: object, expected_ok: bool) -> None:
    UserDict = typed_dict.from_dataclass(User)
    try:
        pydantic.parse_obj_as(UserDict, given)
    except pydantic.ValidationError as exc:
        print(exc)
        assert not expected_ok, 'expected to pass but failed'
    else:
        assert expected_ok, 'expected to fail but passed'
