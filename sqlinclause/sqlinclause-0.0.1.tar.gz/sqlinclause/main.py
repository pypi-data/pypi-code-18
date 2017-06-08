from inspect import currentframe, signature
from typing import List, Tuple, Union, Iterable, Sized, Callable

from sqlinclause.placeholder_extractor import extract_placeholders, PlaceHolder


def expand_sql(
        statement: str,
        params: Union[dict, list, tuple]=None,
        call_depth=1
) -> Tuple[str, Union[dict, list, tuple]]:
    """
    SQL文中でIN句内に名前付きプレースホルダが入っていた場合、実引数リストの数に
    応じて名前付きプレースホルダのカンマ区切り列に展開します。
    
    例： expand_sql_in_clause('select * from some_table where id in :x',
                             {'x': [1,2,3]})
    ⇒
    ('select * from some_table where id in (:e_1,:e_2,:e_3)',
     {'e_1': 1, 'e_2: 2, 'e_3: 3})
    
    :param call_depth: ユーザーコードからの呼び出し深度。直接呼び出す場合は1を指定。
    :param statement: SQL文
    :param params: 実引数辞書。リストやタプルを渡した場合には何も処理せず返します。
    :return: 展開済みのSQL文とそれに適用するための実引数辞書
    """
    if params is None:
        params = {}

    # 辞書型実引数以外には手を触れない
    if not isinstance(params, dict):
        return statement, params

    local_vars = _caller_locals(call_depth)
    placeholders = extract_placeholders(statement)

    supplied_args = dict(params)
    for placeholder in placeholders:
        key_value = placeholder.find_in_dict(params)
        if key_value is None:  # 実引数辞書に必要なキーがなかった！
            local_key_value = placeholder.find_in_dict(local_vars)
            if local_key_value is not None:  # ローカル変数にならあった！
                key, value = local_key_value
                supplied_args[key] = value

    return _expand_sql_in_clause(statement, placeholders, supplied_args)


def expand_sql_in_clause(
        statement: str,
        params: dict
) -> Tuple[str, dict]:
    """
    SQL文中でIN句内に名前付きプレースホルダが入っていた場合、実引数リストの数に
    応じて名前付きプレースホルダのカンマ区切り列に展開します。
    
    例： expand_sql_in_clause('select * from some_table where id in :x',
                             {'x': [1,2,3]})
    ⇒
    ('select * from some_table where id in (:e_1,:e_2,:e_3)',
     {'e_1': 1, 'e_2: 2, 'e_3: 3})
    
    :param statement: SQL文
    :param params: 実引数辞書。
    :return: 展開済みのSQL文とそれに適用するための実引数辞書
    """

    placeholders = extract_placeholders(statement)
    return _expand_sql_in_clause(statement, placeholders, params)


def _expand_sql_in_clause(
        statement: str,
        placeholders: List[PlaceHolder],
        params: dict
) -> Tuple[str, dict]:

    seq = Sequence()
    replacements = []  # type: List[Tuple[PlaceHolder, str]]
    result_args = {}

    for placeholder in placeholders:

        if not placeholder.is_for_in_clause:
            continue

        for replacement in replacements:
            # すでに同じ名前のプレースホルダを置換済みだった場合には、その置換にのっかる
            *_, existing_placeholder, replace_str = replacement
            if existing_placeholder.matches(placeholder):
                replacements.append((placeholder, replace_str))
                break
        else:
            match = placeholder.find_in_dict(params)
            if match is None:
                continue

            key, value = match
            if not isinstance(value, str) and\
                    isinstance(value, Iterable):

                if not isinstance(value, Sized):
                    value = list(value)
                new_names = list(_new_names(placeholders, len(value), seq))
                statement_replace = placeholder.generate_replace_string(new_names)
                result_args.update(zip(new_names, value))
            else:
                statement_replace = placeholder.generate_replace_string([key])

            replacements.append((placeholder, statement_replace))

    result_statement = []
    pos = 0
    for placeholder, text in replacements:
        start = placeholder.pos
        end = placeholder.pos + placeholder.length

        result_statement.append(statement[pos:start])
        if placeholder.is_in_paren:
            result_statement.append(text)
        else:
            result_statement.append('(')
            result_statement.append(text)
            result_statement.append(')')
        pos = end

    result_statement.append(statement[pos:])
    result = ''.join(result_statement)

    for arg_key, arg_value in params.items():
        for placeholder, text in replacements:
            if placeholder.matches(arg_key):
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


def _new_names(existing: List[PlaceHolder], how_many: int, seq: Sequence):
    for i in range(how_many):
        while True:
            name = 'e_%d' % seq.generate()
            if not any(var.matches(name) for var in existing):
                break
        yield name
