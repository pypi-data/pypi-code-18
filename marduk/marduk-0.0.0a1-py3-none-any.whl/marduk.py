# Marduk, transpile your Python 3.6 to Python 3.5
# Copyright (C) 2017 Thomas Grainger
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


import warnings
import functools

from typed_ast import ast3
import typed_astunparse

def unparse(ast):
    return typed_astunparse.unparse(ast).strip()


TYPING_MODULE = '__ast36_35_typing__'

def if_typing(body):
    return ast3.If(
        body=body,
        test=ast3.Attribute(
            attr='TYPE_CHECKING',
            value=ast3.Name(
                id=TYPING_MODULE,
                ctx=ast3.Load(),
            ),
            ctx=ast3.Load()
        ),
        orelse=[],
    )


def splice(fn, vars):
    for i, v in enumerate(vars):
        nv = fn(v)
        if nv is None:
            yield v
        else:
            yield nv
            yield from vars[i:]
            return

def format_str(n):
    c, f = n.conversion, n.format_spec

    def conversion_str():
        try:
            return f'!{chr(c)}'
        except ValueError:
            return ''

    def format_str():
        if isinstance(f, ast3.Str):
            return f':{f.s}'
        return ''


    return f'{{{conversion_str()}{format_str()}}}'


class _AST36To35(ast3.NodeTransformer):
    def visit_Module(self, n):
        new = self.generic_visit(n)

        def dosplice(v):
            if not (isinstance(v, ast3.ImportFrom) and v.module == '__future__'):
                return ast3.Import(names=[ast3.alias('typing', TYPING_MODULE)])

        new.body = list(splice(dosplice, new.body))
        return new


    def visit_FormattedValue(self, n):
        new = self.generic_visit(n)

        return ast3.Call(
            func=ast3.Attribute(
                value=ast3.Str(format_str(new)),
                attr='format',
                ctx=ast3.Load(),
            ),
            args=[new.value],
            keywords=[],
        )


    def visit_JoinedStr(self, n):
        new = self.generic_visit(n)
        NONE = ast3.Str(s='');

        init = ast3.BinOp(left=NONE, right=NONE, op=ast3.Add())

        def to_binop(acc, next):
            left, right, op = acc.left, acc.right, acc.op
            if right is NONE:
                return ast3.BinOp(left=next, right=left, op=op)
            return ast3.BinOp(left=next, right=acc, op=op)

        value = functools.reduce(to_binop, reversed(new.values), init)

        return ast3.Expr(value=value)


    def visit_AnnAssign(self, n):
        new = self.generic_visit(n)
        type_comment=unparse(new.annotation)
        val = new.value if new.value is not None else ast3.NameConstant(value=None)
        assign = ast3.Assign(
            targets=[new.target],
            value=val,
            type_comment=type_comment,
            lineno=new.lineno,
            col_offset=new.col_offset,
        )

        if n.value and isinstance(n.target, ast3.Name):
            return assign

        if not n.simple:
            warnings.warn(f"declaration {unparse(n)} is not valid in mypy", SyntaxWarning)

        return if_typing(assign)


def py36_to_35(ast):
    return _AST36To35().visit(ast)


def py36_to_35_src(src, check=True):
    ast = ast3.parse(src)
    transformed = py36_to_35(ast)


    res = typed_astunparse.unparse(transformed)
    if check:
        ast3.parse(res, feature_version=5)

    return res
