from __future__ import annotations
import mappings


@mappings.schema
class Post:
    title: str


@mappings.schema(total=True)
class User:
    name: str
    age: int
    is_admin: bool = False
    posts: list[Post] = mappings.field(default_factory=list)
