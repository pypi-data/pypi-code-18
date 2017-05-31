import sys
_PY3 = sys.version_info[0] >= 3
if _PY3:
    from html.entities import codepoint2name, name2codepoint
    unichr = chr
    unicode = str
else:
    from htmlentitydefs import codepoint2name, name2codepoint
import re
import codecs


class UnknownEntities(KeyError):
    pass

NAMED_ENT   = unicode('&{0};')
NUMERIC_ENT = unicode('&#{0};')

def unescape(text):
    """
    Convert from HTML entities (named or numeric) to Unicode characters.
    """
    def fixup(m):
        """
        Given an HTML entity (named or numeric), return its Unicode
        equivalent. Does not, however, unescape &amp; &lt; and &gt;
        (decimal 38, 60, and 62). Those are 'special' in that they are
        often escaped for very important, specific reasons (e.g. to describe
        HTML within HTML). Any messing with them is likely to break things
        badly.
        """
        text = m.group(0)
        if text[:2] == "&#":            # numeric entity
            try:
                codepoint = int(text[3:-1], 16) if text[:3] == "&#x" \
                    else int(text[2:-1])
                if codepoint != 38 and codepoint != 60 and codepoint != 62:
                    return unichr(codepoint)
                else:
                    return text
            except ValueError:
                return text
        else:                           # named entity
            try:
                codepoint = name2codepoint[text[1:-1]]
                if codepoint != 38 and codepoint != 60 and codepoint != 62:
                    return unichr(codepoint)
                else:
                    return text
            except KeyError:
                return text
        return text                     # pragma: no cover
                                        # should never execute - but leave as is

    return re.sub(r"&#?\w+;", fixup, text)


def named_entities_codec(text):
    """
    Encode codec that converts Unicode characters into named entities (where
    the names are known), or failing that, numerical entities.
    """
    if isinstance(text, (UnicodeEncodeError, UnicodeTranslateError)):
        s = []
        for c in text.object[text.start:text.end]:
            if ord(c) in codepoint2name:
                s.append(NAMED_ENT.format(codepoint2name[ord(c)]))
            else:
                s.append(NUMERIC_ENT.format(ord(c)))
        return ''.join(s), text.end
    else:
        raise TypeError("Can't handle {0!r}".format(text))


def numeric_entities_codec(text):
    """
    Encode codec that converts Unicode characters into numeric entities.
    """
    if isinstance(text, (UnicodeEncodeError, UnicodeTranslateError)):
        s = []
        for c in text.object[text.start:text.end]:
            s.append(NUMERIC_ENT.format(ord(c)))
        return ''.join(s), text.end
    else:
        raise TypeError("Can't handle {0!r}".format(text))


def hex_entities_codec(text):
    """
    Encode codec that converts Unicode characters into numeric entities
    in hexadecimal form.
    """
    if isinstance(text, (UnicodeEncodeError, UnicodeTranslateError)):
        s = []
        for c in text.object[text.start:text.end]:
            s.append(NUMERIC_ENT.format(hex(ord(c))[1:]))
        return ''.join(s), text.end
    else:
        raise TypeError("Can't handle {0!r}".format(text))


codecs.register_error('named_entities',   named_entities_codec)
codecs.register_error('numeric_entities', numeric_entities_codec)
codecs.register_error('hex_entities',     hex_entities_codec)



def perform_escape(s, escape):
    if not escape:
        return s
    escaper = escape if hasattr(escape, '__call__') else html_escape
    return escaper(s)


def transform(text, escape, codec_name):
    """
    Generic text transformer that converts a string into hatever
    form of entities are required.
    """
    unescaped_text = unescape(text)
    mixed_text = perform_escape(unescaped_text, escape)
    entities_text = mixed_text.encode('ascii', codec_name)
    if _PY3:
        # we don't want type bytes back, we want str; therefore...
        return entities_text.decode("ascii", "strict")
    else:
        return entities_text


def named_entities(text, escape=False):
    """
    Given a string, convert its Unicode characters and numerical HTML entities
    to named HTML entities. Works by converting the entire string to Unicode
    characters, then re-encoding Unicode characters into named entities.
    Where names are not known, numerical entities are used instead.
    """
    return transform(text, escape, 'named_entities')


def numeric_entities(text, escape=False):
    """
    Given a string, convert its Unicode characters and named HTML entities
    to numeric HTML entities. Works by converting the entire string to Unicode
    characters, then re-encoding Unicode characters into numeric entities.
    """
    return transform(text, escape, 'numeric_entities')


decimal_entities = numeric_entities


def numeric_entities_builtin(text, escape=False):
    """
    Given a string, convert its Unicode characters and named HTML entities
    to numeric HTML entities. Works by converting the entire string to Unicode
    characters, then re-encoding Unicode characters into numeric entities.

    This one uses the xmlcharrefreplace builtin.
    """
    return transform(text, escape, 'xmlcharrefreplace')


def hex_entities(text, escape=False):
    """
    Given a string, convert its Unicode characters and named HTML entities to
    numeric HTML entities written in hexadecimal form. Works by converting the
    entire string to Unicode characters, then re-encoding Unicode characters
    into numeric entities.
    """
    return transform(text, escape, 'hex_entities')


def unicode_entities(text, escape=False):
    """
    Given a string, convert its Unicode characters and named/numeric HTML entities
    to Unicode characters, then re-encoding Unicode characters
    into numeric entities.
    """
    unescaped_text = unescape(text)
    mixed_text = perform_escape(unescaped_text, escape)
    return mixed_text


def none_entities(text, escape=False):
    """
    Given a string, do nothing to convert it in any way, but optionally
    escape its HTML. This is essentially a null / identity function,
    present for compatibility and parallelism.
    """
    mixed_text = perform_escape(text, escape)
    return mixed_text

    # This potentially has a rather different behavior than the other
    # entity mappers, in that legitimate entities are never nativized before
    # possible escaping. Do we really need a none transform?


CONVERTER = { 'named':   named_entities,
              'numeric': numeric_entities,
              'decimal': numeric_entities,
              'hex':     hex_entities,
              'unicode': unicode_entities,
              'none':    none_entities,
              None:      none_entities }


def entities(text, kind='named', escape=False):
    """
    Convert Unicode characters and existing entities into the desired
    kind: named, numeric, hex, unicode, or none (a no-op)
    """
    try:
        conv = CONVERTER[kind.lower() if kind is not None else None]
    except KeyError:
        raise UnknownEntities("Don't know about {0!r} entities".format(kind))
    return conv(text, escape=escape)


def html_escape(s, quote=True):
    """
    Replace special characters "&", "<" and ">" to HTML-safe sequences.
    If the optional flag quote is true (the default), the quotation mark
    characters, both double quote (") and single quote (') characters are also
    translated.

    This code was taken verbatim from the Python 3.5.2 standard library, module
    `html`, function `escape`, and is only renamed `html_escape` here.
    """
    s = s.replace("&", "&amp;") # Must be done first!
    s = s.replace("<", "&lt;")
    s = s.replace(">", "&gt;")
    if quote:
        s = s.replace('"', "&quot;")
        s = s.replace('\'', "&#x27;")
    return s


def encode_ampersands(text):
    """
    Encode ampersands into &amp;
    """
    text = re.sub('&(?!([a-zA-Z0-9]+|#[0-9]+|#x[0-9a-fA-F]+);)', '&amp;', text)
    return text
