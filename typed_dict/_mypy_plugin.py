from __future__ import annotations

from typing import Callable

from mypy import nodes, types
from mypy.plugin import (
    DynamicClassDefContext,
    Plugin,
    SemanticAnalyzerPluginInterface,
)

from ._from import from_dataclass

FROM_DATACLASS_FULLNAME = f'{from_dataclass.__module__}.{from_dataclass.__qualname__}'
FALLBACKS = (
    'typing._TypedDict',
    'typing_extensions._TypedDict',
    'mypy_extensions._TypedDict',
)


class TypedDictPlugin(Plugin):
    """Mypy plugin to generate TypedDict.

    https://mypy.readthedocs.io/en/stable/extending_mypy.html
    """

    def get_dynamic_class_hook(
        self,
        fullname: str,
    ) -> Callable[[DynamicClassDefContext], None] | None:
        """Implements mypy callback."""
        if fullname == FROM_DATACLASS_FULLNAME:
            return self._from_dataclass_callback
        return None

    def _from_dataclass_callback(
        self,
        ctx: DynamicClassDefContext,
    ) -> None:
        first_arg = ctx.call.args[0]
        if not isinstance(first_arg, nodes.NameExpr):
            return
        if not isinstance(first_arg.node, nodes.TypeInfo):
            return
        ctx.api.add_symbol_table_node(
            ctx.name, nodes.SymbolTableNode(
                kind=nodes.GDEF,
                node=self._build_typeddict_typeinfo(
                    api=ctx.api,
                    name=first_arg.node.name,
                    names=first_arg.node.names,
                    required_keys=set(),
                    line=ctx.call.line,
                ),
            ),
        )

    def _build_typeddict_typeinfo(  # noqa: WPS211
        self,
        api: SemanticAnalyzerPluginInterface,
        name: str,
        names: nodes.SymbolTable,
        required_keys: set[str],
        line: int,
    ) -> nodes.TypeInfo:
        fallback = self._get_fallback(api)
        type_info = api.basic_new_typeinfo(name, fallback, line)
        any_type = api.lookup_fully_qualified('typing.Any').type
        assert any_type is not None
        type_info.update_typeddict_type(
            types.TypedDictType(
                items={name: node.type or any_type for name, node in names.items()},
                required_keys=required_keys,
                fallback=fallback,
            ),
        )
        return type_info

    def _get_fallback(
        self,
        api: SemanticAnalyzerPluginInterface,
    ) -> types.Instance:
        for name in FALLBACKS:
            fallback = api.named_type_or_none(name, [])
            if fallback is not None:
                return fallback
        raise LookupError('cannot find fallback type for TypedDict')


def plugin(version: str) -> type[Plugin]:
    """Mypy plugin entry point."""
    return TypedDictPlugin
