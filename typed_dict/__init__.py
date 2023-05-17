"""A library to generate TypedDict from different types, with mypy support."""
from ._from import from_dataclass
from ._mypy_plugin import plugin

__all__ = [  # noqa: WPS410
    'from_dataclass',
    'plugin',
]
