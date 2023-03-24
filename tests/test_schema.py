from __future__ import annotations

import mappings


def test_cast_is_noop() -> None:
    @mappings.schema
    class User:
        name: str

    assert mappings.cast(User, {'name': 'Mark'}) == {'name': 'Mark'}
