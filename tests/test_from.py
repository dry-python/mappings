from dataclasses import dataclass
import typed_dict
from typing_extensions import NotRequired


def test_from_dataclass():
    @dataclass
    class User:
        name: str

    actual = typed_dict.from_dataclass(User)
    assert actual.__annotations__ == {'name': str}
    assert actual.__required_keys__ == frozenset({'name'})
    assert actual.__optional_keys__ == frozenset()
    assert actual.__total__ is True


def test_from_dataclass__not_total():
    @dataclass
    class User:
        name: str

    actual = typed_dict.from_dataclass(User, total=False)
    assert actual.__annotations__ == {'name': str}
    assert actual.__required_keys__ == frozenset()
    assert actual.__optional_keys__ == frozenset({'name'})
    assert actual.__total__ is False


def test_from_dataclass__default_value():
    """If a dataclass field has a default value, the field is not required.
    """
    @dataclass
    class User:
        name: str = ''

    actual = typed_dict.from_dataclass(User)
    assert actual.__annotations__ == {'name': NotRequired[str]}  # pyright: ignore
    assert actual.__required_keys__ == frozenset({'name'})
    assert actual.__optional_keys__ == frozenset()
    assert actual.__total__ is True
