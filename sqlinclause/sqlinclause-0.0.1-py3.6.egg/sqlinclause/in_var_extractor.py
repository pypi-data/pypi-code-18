import re
import sqlparse
from typing import List, Tuple, Iterator, Iterable, Union, Any, Dict, Set

Token = sqlparse.tokens.Token


def parse_named_placeholder(text: str):
    if text[0] == ':':
        return text[1:], False
    else:
        return text[2:-2], True


class InVar:
    """
    SQL文中に含まれるIN句を構成する名前付きプレースホルダ情報。
    IN :x
    という記述があったら、「:x」部分の開始位置・長さと認識結果を格納しています。
    :property pos: 開始位置
    :property length: 長さ
    :property name: プレースホルダ名
    :property is_pyformat: %(x)s 形式であったらTrue、:x 形式ならFalse
    :property is_in_paren: IN (:x) の形なら True, IN :x の形ならFalse
    """

    def __init__(self,
                 pos: int,
                 text: str,
                 is_in_paren: bool  # IN :x ならFalse、IN (:x) ならTrue
                 ):
        self.pos = pos
        self.length = len(text)
        self.name, self.is_pyformat = parse_named_placeholder(text)
        self.is_in_paren = is_in_paren

    def matches(self, obj):
        """
        指定された名前、またはInVarに一致するプレースホルダであるかを判定します。
        not is_pyformat の場合にはcx_oracleの動作に合わせるため
        大小文字無視して一致判定するようになっています。
        """
        if isinstance(obj, str):
            if self.is_pyformat:
                return self.name == obj
            else:
                return self.name.lower() == obj.lower()
        else:
            if self.is_pyformat:
                return obj.is_pyformat and self.name == obj.name
            else:
                return not obj.is_pyformat and\
                       self.name.lower() == obj.name.lower()

    def find_in_dict(self, d: Dict[str, Any]):
        """
        辞書中に、自分の名前に一致するキーがあればそのキーと値を出力します。
        """
        if self.is_pyformat:
            if self.name in d:
                return self.name, d[self.name]
        else:
            for key in d:
                if self.matches(key):
                    return key, d[key]
        return None

    def generate_replace_string(self, new_names: Iterable[str]):
        """
        このプレースホルダを、指定された名前のプレースホルダの列に変換します。
        この結果をSQLの文字列置換に使用します。
        :param new_names: 名前の列
        :return: 必要に応じて括弧を補ったカンマ区切りプレースホルダ列
        """
        if self.is_pyformat:
            result = '%(' + ')s,%('.join(new_names) + ')s'
        else:
            result = ':' + ',:'.join(new_names)

        return result if self.is_in_paren else '(%s)' % result

    def __str__(self):
        return '<%s (%d-%d) %s%s>' % (
            self.name,
            self.pos,
            self.pos + self.length,
            'pyformat' if self.is_pyformat else 'named',
            ' in_paren' if self.is_in_paren else ''
        )


def extract_in_var(
        statement: str
) -> Tuple[List[InVar], Set[str]]:

    return parse_expression(
        iter(sqlparse.parse(statement)[0].flatten()))


def parse_expression(
        token_iterator: Iterator
) -> Tuple[List[InVar], Set[str]]:
    """
    括弧に入っていない地の文。
    """
    pos = 0
    in_vars = []  # type: List[InVar]
    names = set()  # type: Set[str]
    while True:
        try:
            token = next(token_iterator)
        except StopIteration:
            return in_vars, names
        pos += len(str(token))

        if is_left_paren(token):
            pos, found_in_vars, found_names =\
                parse_paren(pos, token_iterator)
            in_vars += found_in_vars
            names += found_names

        elif is_keyword_in(token):

            pos, found_in_vars, found_names =\
                parse_in_clause(pos, token_iterator)
            in_vars += found_in_vars
            names += found_names

        elif is_named_placeholder(token):
            name, _ = parse_named_placeholder(str(token))
            names.append(name)


def parse_in_clause_paren(
        pos: int,
        token_iterator: Iterator
) -> Tuple[int, List[InVar], Set[str]]:
    """
    INに続く括弧の中。
    """
    print('parse_in_clause_paren')
    in_vars = []  # type: List[InVar]
    names = set()  # type: Set[str]
    while True:
        try:
            token = next(token_iterator)
        except StopIteration:
            return pos, in_vars, names
        cur_pos = pos
        pos += len(str(token))

        if is_right_paren(token):
            return pos, in_vars, names

        if is_left_paren(token):
            pos, found_in_vars, found_names = \
                parse_paren(pos, token_iterator)
            in_vars += found_in_vars
            names += found_names

        elif is_named_placeholder(token):

            in_var = InVar(cur_pos, str(token), is_in_paren=True)
            in_vars.append(in_var)
            names.append(in_var.name)


def parse_paren(
        pos: int,
        token_iterator: Iterator
) -> Tuple[int, List[InVar], List[str]]:
    """
    括弧の中。
    """
    print('parse_paren')
    found = []  # type: List[InVar]
    names = []  # type: Set[str]
    while True:
        try:
            token = next(token_iterator)
        except StopIteration:
            return pos, found, names
        pos += len(str(token))

        if is_right_paren(token):
            return pos, found, names

        if is_left_paren(token):
            pos, found_in_vars, found_names =\
                parse_paren(pos, token_iterator)
            found += found_in_vars
            names += found_names

        elif is_keyword_in(token):

            pos, found_in_vars, found_names =\
                parse_in_clause(pos, token_iterator)
            found += found_in_vars
            names += found_names

        elif is_named_placeholder(token):
            name, _ = parse_named_placeholder(str(token))
            names.append(name)


def parse_in_clause(
        pos: int,
        token_iterator: Iterator
) -> Tuple[int, List[InVar], Set[str]]:
    """
    "IN"を呼んだ直後の状態。
    """
    print('parse_in_clause')
    while True:
        try:
            token = next(token_iterator)
        except StopIteration:
            return pos, [], set()
        cur_pos = pos
        pos += len(str(token))

        if is_left_paren(token):

            return parse_in_clause_paren(pos, token_iterator)

        elif is_named_placeholder(token):

            in_var = InVar(cur_pos, str(token), is_in_paren=False)
            return pos, [in_var], {in_var.name}

        elif not is_ignorable(token):
            return pos, [], set()


def is_keyword_in(token):
    return token.ttype == Token.Keyword and str(token).lower() == 'in'


def is_ignorable(token):
    return token.ttype in (Token.Comment.Multiline,
                           Token.Comment.Single,
                           Token.Text.Whitespace)


def is_named_placeholder(token):
    s = str(token)
    return token.ttype == Token.Name.Placeholder and \
        ((s[0] == ':' and not re.match(':[0-9]+$', s))
         or s.startswith('%('))


def is_left_paren(token):
    return token.ttype == Token.Punctuation and str(token) == '('


def is_right_paren(token):
    return token.ttype == Token.Punctuation and str(token) == ')'
