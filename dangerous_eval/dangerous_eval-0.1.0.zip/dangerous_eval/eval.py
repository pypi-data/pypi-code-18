# coding: utf-8
from node_exec import *


class AT(object):
    unaryop = 1
    boolop = 2
    cmpop = 4
    binop = 8
    subscript = 16
    str = 32
    num = 64
    list = 128
    dict = 256
    set = 512
    tuple = 1024
    name = 2048
    attribute = 4096
    call = 8192


class DangerousEval(object):
    def __init__(self, env=None, allow=AT.call * 2 - 1):
        self.env = env
        self.exec_map = dict()
        for k, v in built_exec.items():
            if allow & k:
                self.exec_map.update(v)

    def eval(self, expr):
        return self._eval_node(ast.parse(expr, mode="eval").body)

    def _eval_node(self, node):
        node_type = type(node)
        if node_type not in self.exec_map:
            raise TypeError(node)
        return self.exec_map[node_type](self.env, node, self._eval_node)


built_exec = {
    AT.unaryop: {ast.UnaryOp: unaryop_},
    AT.boolop: {ast.BoolOp: boolop_},
    AT.cmpop: {ast.Compare: cmpop_},
    AT.binop: {ast.BinOp: binop_},
    AT.subscript: {ast.Subscript: subscript_},
    AT.str: {ast.Str: str_},
    AT.num: {ast.Num: num_},
    AT.list: {ast.List: list_},
    AT.dict: {ast.Dict: dict_},
    AT.set: {ast.Set: set_},
    AT.tuple: {ast.Tuple: tuple_},
    AT.name: {ast.Name: name_},
    AT.attribute: {ast.Attribute: attribute_},
    AT.call: {ast.Call: call_},
}
