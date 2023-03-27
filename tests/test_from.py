from dataclasses import dataclass

from typing_extensions import NotRequired, TypedDict

import typed_dict


def compare_typed_dicts(actual: object, expected: object) -> None:
    attrs = (
        '__annotations__',
        '__required_keys__',
        '__optional_keys__',
        '__total__',
    )
    for attr in attrs:
        assert getattr(actual, attr) == getattr(expected, attr)


def test_from_dataclass():
    @dataclass
    class User:
        name: str

    class UserDict(TypedDict):
        name: str

    actual = typed_dict.from_dataclass(User)
    compare_typed_dicts(actual, UserDict)


def test_from_dataclass__not_total():
    @dataclass
    class User:
        name: str

    class UserDict(TypedDict, total=False):
        name: str

    actual = typed_dict.from_dataclass(User, total=False)
    compare_typed_dicts(actual, UserDict)


def test_from_dataclass__default_value():
    """If a dataclass field has a default value, the field is not required.
    """
    @dataclass
    class User:
        name: str = ''

    class UserDict(TypedDict):
        name: NotRequired[str]

    actual = typed_dict.from_dataclass(User)
    compare_typed_dicts(actual, UserDict)
