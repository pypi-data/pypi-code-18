# coding: utf-8


class Node(object):
    """ 一个简单的结构表示文本中的一行 """
    __slots__ = ('name', 'expr', 'children', 'output')

    def __init__(self, name, expr=None, children=None, output=None):
        self.name = name
        self.expr = expr
        self.children = children
        self.output = output

    def __repr__(self):
        return "<Node name={} expr={} output={}>{}</Node>"\
            .format(self.name, self.expr, self.output, self.children or '')


def parse(script):
    """ 将代码解释成 Node 列表 """
    return map(_process_node, _parse_indented_text(script))


def _process_node(item_arr):
    line, children = (item_arr[0], item_arr[1:] if len(item_arr) > 1 else None)
    left, expr = line.split(None, 1)
    name, output = left.split("@") if "@" in left else (left, None)
    children = map(_process_node, children) if children else None
    item = Node(name=name, expr=expr, output=output, children=children)
    return item


def _parse_indented_text(text):
    """ 处理脚本文本 """
    lines = text.splitlines()
    result = []
    indent_stack = [0]
    for line in lines:
        indent = len(line) - len(line.strip())
        if not line.strip():
            continue
        try:
            pos = indent_stack.index(indent)
            indent_stack = indent_stack[:pos + 1]
        except ValueError:
            if indent < indent_stack[-1]:
                raise IndentationError("unexpected indent")
            pos = len(indent_stack)
            indent_stack.append(indent)

        p = result
        for x in range(pos):
            p = p[-1]
        p.append([line.strip()])
    return result
