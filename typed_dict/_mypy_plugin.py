from __future__ import annotations

from typing import Callable

import mypy.nodes
import mypy.types
from mypy.plugin import (
    DynamicClassDefContext,
    Plugin,
    SemanticAnalyzerPluginInterface,
)

from ._from import from_dataclass

FROM_DATACLASS_FULLNAME = f'{from_dataclass.__module__}.{from_dataclass.__qualname__}'
FALLBACKS = (
    "typing._TypedDict",
    "typing_extensions._TypedDict",
    "mypy_extensions._TypedDict",
)


class TypedDictPlugin(Plugin):
    def get_dynamic_class_hook(
        self,
        fullname: str,
    ) -> Callable[[DynamicClassDefContext], None] | None:
        if fullname == FROM_DATACLASS_FULLNAME:
            return self._from_dataclass_callback
        return None

    def _from_dataclass_callback(
        self,
        ctx: DynamicClassDefContext,
    ) -> None:
        first_arg = ctx.call.args[0]
        assert isinstance(first_arg, mypy.nodes.NameExpr)
        assert isinstance(first_arg.node, mypy.nodes.TypeInfo)
        ctx.api.add_symbol_table_node(
            ctx.name, mypy.nodes.SymbolTableNode(
                kind=mypy.nodes.GDEF,
                node=self._build_typeddict_typeinfo(
                    api=ctx.api,
                    name=first_arg.node.name,
                    names=first_arg.node.names,
                    required_keys=set(),
                    line=ctx.call.line,
                )
            ),
        )

    def _build_typeddict_typeinfo(
        self,
        api: SemanticAnalyzerPluginInterface,
        name: str,
        names: mypy.nodes.SymbolTable,
        required_keys: set[str],
        line: int,
    ) -> mypy.nodes.TypeInfo:
        fallback = self._get_fallback(api)
        info = api.basic_new_typeinfo(name, fallback, line)
        any_type = api.lookup_fully_qualified('typing.Any').type
        assert any_type is not None
        items: dict[str, mypy.types.Type]
        items = {name: node.type or any_type for name, node in names.items()}
        info.update_typeddict_type(
            mypy.types.TypedDictType(
                items=items,
                required_keys=required_keys,
                fallback=fallback,
            ),
        )
        return info

    def _get_fallback(
        self,
        api: SemanticAnalyzerPluginInterface,
    ) -> mypy.types.Instance:
        for name in FALLBACKS:
            fallback = api.named_type_or_none(name, [])
            if fallback is not None:
                return fallback
        raise LookupError('cannot find fallback type for TypedDict')


def plugin(version: str) -> type[Plugin]:
    return TypedDictPlugin
