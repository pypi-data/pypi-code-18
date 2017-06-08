import re
import sqlparse
from typing import List, Tuple, Iterator, Iterable, Any, Dict

Token = sqlparse.tokens.Token


def _parse_named_placeholder(text: str):
    if text[0] == ':':
        return text[1:], False
    else:
        return text[2:-2], True


class PlaceHolder:
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
                 is_for_in_clause: bool,  # IN句内のプレースホルダであるか
                 is_in_paren: bool  # IN :x ならFalse、IN (:x) ならTrue
                 ):
        self.pos = pos
        self.length = len(text)
        self.name, self.is_pyformat = _parse_named_placeholder(text)
        self.is_for_in_clause = is_for_in_clause
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
                return not obj.is_pyformat and \
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
        """
        if self.is_pyformat:
            return '%(' + ')s,%('.join(new_names) + ')s'
        else:
            return ':' + ',:'.join(new_names)

    def __str__(self):
        return '<%s (%d-%d) %s%s>' % (
            self.name,
            self.pos,
            self.pos + self.length,
            'pyformat' if self.is_pyformat else 'named',
            '' if not self.is_for_in_clause else ' IN()'
            if self.is_in_paren else ' IN'
        )


def extract_placeholders(
        statement: str
) -> List[PlaceHolder]:
    return _parse_expression(
        iter(sqlparse.parse(statement)[0].flatten()))


def _parse_expression(
        token_iterator: Iterator
) -> List[PlaceHolder]:
    """
    括弧に入っていない地の文。
    """
    pos = 0
    placeholders = []  # type: List[PlaceHolder]
    while True:
        try:
            token = next(token_iterator)
        except StopIteration:
            return placeholders
        pos += len(str(token))

        if _is_left_paren(token):
            pos, found_placeholders = \
                _parse_paren(pos, token_iterator)
            placeholders += found_placeholders

        elif _is_keyword_in(token):

            pos, found_placeholders = \
                _parse_in_clause(pos, token_iterator)
            placeholders += found_placeholders

        elif _is_named_placeholder(token):
            placeholders.append(PlaceHolder(pos, str(token),
                                            is_for_in_clause=False,
                                            is_in_paren=False))


def _parse_in_clause_paren(
        pos: int,
        token_iterator: Iterator
) -> Tuple[int, List[PlaceHolder]]:
    """
    INに続く括弧の中。
    """
    placeholders = []  # type: List[PlaceHolder]
    while True:
        try:
            token = next(token_iterator)
        except StopIteration:
            return pos, placeholders
        cur_pos = pos
        pos += len(str(token))

        if _is_right_paren(token):
            return pos, placeholders

        if _is_left_paren(token):
            pos, found_placeholders = \
                _parse_paren(pos, token_iterator)
            placeholders += found_placeholders

        elif _is_named_placeholder(token):

            placeholder = PlaceHolder(cur_pos, str(token),
                                      is_for_in_clause=True,
                                      is_in_paren=True)
            placeholders.append(placeholder)


def _parse_paren(
        pos: int,
        token_iterator: Iterator
) -> Tuple[int, List[PlaceHolder]]:
    """
    括弧の中。
    """
    found = []  # type: List[PlaceHolder]
    while True:
        try:
            token = next(token_iterator)
        except StopIteration:
            return pos, found
        pos += len(str(token))

        if _is_right_paren(token):
            return pos, found

        if _is_left_paren(token):
            pos, found_placeholders = \
                _parse_paren(pos, token_iterator)
            found += found_placeholders

        elif _is_keyword_in(token):

            pos, found_placeholders = \
                _parse_in_clause(pos, token_iterator)
            found += found_placeholders

        elif _is_named_placeholder(token):
            found.append(PlaceHolder(pos, str(token),
                                     is_for_in_clause=False,
                                     is_in_paren=False))


def _parse_in_clause(
        pos: int,
        token_iterator: Iterator
) -> Tuple[int, List[PlaceHolder]]:
    """
    "IN"を呼んだ直後の状態。
    """
    while True:
        try:
            token = next(token_iterator)
        except StopIteration:
            return pos, []
        cur_pos = pos
        pos += len(str(token))

        if _is_left_paren(token):

            return _parse_in_clause_paren(pos, token_iterator)

        elif _is_named_placeholder(token):

            placeholder = PlaceHolder(cur_pos,
                                      str(token),
                                      is_for_in_clause=True,
                                      is_in_paren=False)
            return pos, [placeholder]

        elif not _is_ignorable(token):
            return pos, []


def _is_keyword_in(token):
    return token.ttype == Token.Keyword and str(token).lower() == 'in'


def _is_ignorable(token):
    return token.ttype in (Token.Comment.Multiline,
                           Token.Comment.Single,
                           Token.Text.Whitespace)


def _is_named_placeholder(token):
    s = str(token)
    return token.ttype == Token.Name.Placeholder and \
        ((s[0] == ':' and not re.match(':[0-9]+$', s))
         or s.startswith('%('))


def _is_left_paren(token):
    return token.ttype == Token.Punctuation and str(token) == '('


def _is_right_paren(token):
    return token.ttype == Token.Punctuation and str(token) == ')'
