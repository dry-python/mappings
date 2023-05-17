from __future__ import annotations

from typing import Callable

from mypy import nodes
from mypy.plugin import DynamicClassDefContext, Plugin

from ._from import from_dataclass
from ._mypy_ast import Model

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
        if not isinstance(first_arg, (nodes.NameExpr, nodes.MemberExpr)):
            return
        if not isinstance(first_arg.node, nodes.TypeInfo):
            return
        model = Model.from_dataclass(first_arg.node)
        type_info = model.as_type_info(api=ctx.api, line=ctx.call.line)
        stnode = nodes.SymbolTableNode(kind=nodes.GDEF, node=type_info)
        ctx.api.add_symbol_table_node(ctx.name, stnode)


def plugin(version: str) -> type[Plugin]:
    """Mypy plugin entry point."""
    return TypedDictPlugin
