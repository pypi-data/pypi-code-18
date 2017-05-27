import ast


def unaryop_(env, node, ev):
    if isinstance(node.op, ast.UAdd):
        return +ev(node.operand)
    elif isinstance(node.op, ast.USub):
        return -ev(node.operand)
    elif isinstance(node.op, ast.Not):
        return not ev(node.operand)
    elif isinstance(node.op, ast.Invert):
        return ~ev(node.operand)
    else:
        raise TypeError(node)


def boolop_(env, node, ev):
    if isinstance(node.op, ast.And):
        for n in node.values:
            if not ev(n):
                return False
        return True
    elif isinstance(node.op, ast.Or):
        for n in node.values:
            if ev(n):
                return True
        return False
    else:
        raise TypeError(node)


def cmpop_(env, node, ev):
    l = ev(node.left)
    for idx, op in enumerate(node.ops):
        r = ev(node.comparators[idx])
        if isinstance(op, ast.NotEq):
            if l == r:
                return False
        elif isinstance(op, ast.Eq):
            if l != r:
                return False
        elif isinstance(op, ast.NotIn):
            if l in r:
                return False
        elif isinstance(op, ast.IsNot):
            if not (l is not r):
                return False
        elif isinstance(op, ast.Gt):
            if l <= r:
                return False
        elif isinstance(op, ast.LtE):
            if l > r:
                return False
        elif isinstance(op, ast.Lt):
            if l >= r:
                return False
        elif isinstance(op, ast.GtE):
            if l < r:
                return False
        elif isinstance(op, ast.In):
            if l not in r:
                return False
        elif isinstance(op, ast.Is):
            if not (l is r):
                return False
        else:
            raise AttributeError(node)
        l = r
    return True


def binop_(env, node, ev):
    l, r = ev(node.left), ev(node.right)
    if isinstance(node.op, ast.RShift):
        return l >> r
    elif isinstance(node.op, ast.BitXor):
        return l ^ r
    elif isinstance(node.op, ast.Div):
        return l / r
    elif isinstance(node.op, ast.Sub):
        return l - r
    elif isinstance(node.op, ast.Pow):
        return l ** r
    elif isinstance(node.op, ast.BitAnd):
        return l & r
    elif isinstance(node.op, ast.Mod):
        return l % r
    elif isinstance(node.op, ast.Mult):
        return l * r
    elif isinstance(node.op, ast.FloorDiv):
        return l // r
    elif isinstance(node.op, ast.LShift):
        return l << r
    elif isinstance(node.op, ast.And):
        return l and r
    elif isinstance(node.op, ast.BitOr):
        return l | r
    else:
        raise AttributeError(node)


def subscript_(env, node, ev):
    import operator

    if isinstance(node.slice, ast.Index):
        iv = ev(node.slice.value)
        if isinstance(iv, basestring) and iv[:2] == "__":
            raise AttributeError(node)
        return ev(node.value)[iv]
    elif isinstance(node.slice, ast.Slice):

        valid = (node.slice.lower is None or isinstance(node.slice.lower, ast.Num)) and \
                (node.slice.upper is None or isinstance(node.slice.upper, ast.Num)) and \
                (node.slice.step is None or isinstance(node.slice.upper, ast.Num))
        if not valid:
            raise AttributeError(node)
        arr = ev(node.value)
        length = len(arr)
        lower = node.slice.lower.n if node.slice.lower else 0
        if lower < 0:
            lower = length + lower
        upper = node.slice.upper.n if node.slice.upper else len(arr)
        if upper < 0:
            upper = length + upper
        step = node.slice.step.n if node.slice.step else 1
        return arr[lower:upper:step]
    else:
        raise AttributeError(node)


def str_(env, node, ev):
    return node.s


def num_(env, node, ev):
    return node.n


def list_(env, node, ev):
    return [ev(n) for n in node.elts]


def dict_(env, node, ev):
    return {ev(n): ev(node.values[idx]) for idx, n in enumerate(node.keys)}


def set_(env, node, ev):
    return set(list_(env, node, ev))


def name_(env, node, ev):
    return env[node.id]


def tuple_(env, node, ev):
    return tuple(list_(env, node, ev))


def attribute_(env, node, ev):
    if node.attr[:2] == "__":
        raise AttributeError(node)
    return getattr(ev(node.value), node.attr)


def call_(env, node, ev):
    fn = ev(node.func)
    args = [ev(n) for n in node.args]
    kwargs = {kw.arg: ev(kw.value) for kw in node.keywords}
    return fn(*args, **kwargs)
