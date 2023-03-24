import mappings


def test_cast_is_noop():
    @mappings.schema
    class User:
        name: str

    assert User.cast({'name': 'Mark'}) == {'name': 'Mark'}
