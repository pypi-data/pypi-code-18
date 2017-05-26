# coding: utf-8
import ast


class SafeEval(object):
    def __init__(self, env=None):
        self.env = env
        self._allowed_operators = {
            ast.Num: self._eval_num,
            ast.Str: self._eval_str,
            ast.Call: self._eval_call,
            ast.Name: self._eval_name,
        }

    def _eval_name(self, node):
        return self.env[node.id]

    def _eval_num(self, node):
        return node.n

    def _eval_str(self, node):
        return node.s

    def _eval_call(self, node):
        if node.func.id in self.env:
            args = [self._eval_node(arg_node) for arg_node in node.args]
            kwargs = {item.arg: self._eval_node(item.value) for item in node.keywords}
            return self.env[node.func.id](*args, **kwargs)
        raise AttributeError(node.func.id)

    def eval(self, expr):
        return self._eval_node(ast.parse(expr, mode="eval").body)

    def _eval_node(self, node):
        node_type = type(node)
        if node_type not in self._allowed_operators:
            raise TypeError(node)
        return self._allowed_operators[node_type](node)
