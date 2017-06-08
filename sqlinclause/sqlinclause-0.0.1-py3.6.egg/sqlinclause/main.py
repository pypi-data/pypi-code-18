from inspect import currentframe
from typing import Set, List, Any, Dict, Tuple, Union, Iterable, Sized

from in_var_extractor import extract_in_var, InVar


def expand_in_clause(
        statement: str,
        args: Union[dict, list, tuple, None]
) -> Tuple[str, Union[dict, list, tuple]]:
    if args is None:
        args = {}

    # 辞書型実引数以外には手を触れない
    if not isinstance(args, dict):
        return statement, args

    seq = Sequence()
    in_vars, names = extract_in_var(statement)

    replacements = []  # type: List[Tuple[InVar, str]]
    result_args = {}

    for in_var in in_vars:

        for replacement in replacements:
            # すでに同じ名前のプレースホルダを置換済みだった場合には、その置換にのっかる
            *_, found_in_var, found_replacestr = replacement
            if found_in_var.matches(in_var):
                replacements.append((in_var, found_replacestr))
                break
        else:
            match = in_var.find_in_dict(args)
            if match is None:
                continue

            key, value = match
            if not isinstance(value, str) and\
                    isinstance(value, Iterable):

                if not isinstance(value, Sized):
                    value = list(value)
                new_names = _new_names(names, len(value), seq)
                statement_replace = in_var.generate_replace_string(new_names)
                result_args.update(zip(new_names, value))
            else:
                statement_replace = in_var.generate_replace_string([key])

            replacements.append((in_var, statement_replace))

    result_statement = []
    pos = 0
    for in_var, text in replacements:
        start = in_var.pos
        end = in_var.pos + in_var.length

        result_statement.append(statement[pos:start])
        result_statement.append(text)
        pos = end

    result_statement.append(statement[pos:])
    result = ''.join(result_statement)

    for arg_key, arg_value in args.items():
        for in_var, text in replacements:
            if in_var.matches(arg_key):
                break
        else:
            result_args[arg_key] = arg_value

    return result, result_args


def _caller_locals(depth: int = 1) -> dict:
    """
    呼び出し元コードの名前空間を辞書として取得します。
    :param depth: _caller_namespace() を呼んでいるコードを0とし、増えるごとに\
    呼び出し元を1つずつ遡っていきます。
    :return:
    """
    f = currentframe().f_back
    for i in range(depth):
        f = f.f_back
    return f.f_locals


class Sequence:
    def __init__(self):
        self.count = 0

    def generate(self):
        self.count += 1
        return self.count


def _new_names(existing: Set[str], how_many: int, seq: Sequence):
    for i in range(how_many):
        while True:
            name = 'e#%d' % seq.generate()
            if name not in existing:
                break
        yield name
