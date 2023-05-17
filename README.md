# typed_dict

[![Build Status](https://travis-ci.com/dry-python/mappings.svg?branch=master)](https://travis-ci.com/dry-python/mappings)
[![Coverage](https://coveralls.io/repos/github/dry-python/mappings/badge.svg?branch=master)](https://coveralls.io/github/dry-python/mappings?branch=master)
[![Python Version](https://img.shields.io/pypi/pyversions/typed-dict.svg)](https://pypi.org/project/typed-dict/)
[![wemake-python-styleguide](https://img.shields.io/badge/style-wemake-000000.svg)](https://github.com/wemake-services/wemake-python-styleguide)

Like attrs, but for dicts

What it can do:

+ Generate [TypedDict](https://docs.python.org/3/library/typing.html#typing.TypedDict) from pydantic models, attrs schemas, and dataclasses.
+ Validate dicts using TypedDict at runtime.

Why it's cool:

+ Supports multiple schema formats.
+ 100% type safe.

## Installation

Install:

```bash
python3 -m pip install typed-dict
```

And then add in `plugins` section of the [mypy config](https://mypy.readthedocs.io/en/stable/config_file.html) (`pyproject.toml`):

```toml
[tool.mypy]
plugins = ["typed_dict"]
```

## Usage

Generate a TypedDict from a [dataclass](https://docs.python.org/3/library/dataclasses.html):

```python
from dataclasses import dataclass
import typed_dict

@dataclass
class User:
    name: str
    age: int = 99

UserDict = typed_dict.from_dataclass(User)
```

Now, you can use it in type annotations (and [mypy](https://mypy-lang.org/) will understand it):

```python
user: UserDict = {'name': 'aragorn'}
```

Or with runtime type checkers, like [pydantic](https://github.com/pydantic/pydantic):

```python
import pydantic

user = pydantic.parse_obj_as(UserDict, {'name': 'Aragorn'})
assert user == {'name': 'Aragorn'}
```

See [examples](./examples/) directory for more code.
