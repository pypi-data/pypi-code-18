
import six
from namedentities import *
from namedentities.core import (named_entities_codec, hex_entities_codec,
                                numeric_entities_codec,
                                numeric_entities_builtin,
                                none_entities, html_escape)
import sys
import pytest


def _print(*args, **kwargs):
    """
    Python 2 and 3 compatible print function, similar to Python 3 arg handling.
    """
    sep = kwargs.get('sep', ' ')
    end = kwargs.get('end', '\n')
    f   = kwargs.get('file', sys.stdout)
    parts.append(end)
    f.write(sep.join(parts))


def test_unicode():
    u = six.u('both em\u2014and&')
    assert named_entities(u) == six.u("both em&mdash;and&")


def test_numeric_entity():
    u = six.u('and&#x2013;dashes')
    assert named_entities(u) == six.u("and&ndash;dashes")
    assert hex_entities(u) == entities(u, 'hex')


def test_broken_entity():
    # if the entity is broken, it doesn't encode anything properly
    # so do-not-translate is the right approach
    u = six.u('and&#broke;it')
    assert named_entities(u) == u
    assert hex_entities(u) == u
    assert numeric_entities(u) == u
    assert unicode_entities(u) == u

    # similarly, if there really is no named entity, leave it be

    u = 'also &broken; too'
    assert hex_entities(u) == u


def test_broken_codecs():
    # ensure some trivial exception paths as not legitimate issues
    with pytest.raises(TypeError):
        numeric_entities_codec(4)
    with pytest.raises(TypeError):
        hex_entities_codec(4)
    with pytest.raises(TypeError):
        named_entities_codec(4)


def test_hex():

    u = six.u('both em\u2014and&#x2013;dashes&hellip;')
    assert hex_entities(u) == six.u("both em&#x2014;and&#x2013;dashes&#x2026;")


def test_entities():
    u = six.u('both em\u2014and&#x2013;dashes&hellip;')
    assert hex_entities(u) == entities(u, 'hex')
    assert named_entities(u) == entities(u, 'named')
    assert numeric_entities(u) == entities(u, 'numeric')
    assert unicode_entities(u) == entities(u, 'unicode')
    assert u == entities(u, 'none')
    with pytest.raises(UnknownEntities):
        entities(u, 'bozo')


def test_unicode_and_numeric():
    u = six.u('both em\u2014and&#x2013;dashes&hellip;')
    assert named_entities(u) == six.u("both em&mdash;and&ndash;dashes&hellip;")


def test_numeric_entities_builtin():
    # not exported, but let's test it anyway
    assert numeric_entities_builtin('this &mdash;') == 'this &#8212;'


def test_missing_named_entities():
    """
    Some great Unicode symbols don't have HTML entity names. What
    happens when they're encountered?
    """
    sm = six.u("\u2120")
    assert numeric_entities(sm) == '&#8480;'
    assert named_entities(sm) == '&#8480;'  # can't name-encode


def test_six_print_example(capsys):
    u = six.u('both em\u2014and&#x2013;dashes&hellip;')
    six.print_(named_entities(u))
    out, err = capsys.readouterr()
    assert out.startswith("both em&mdash;and&ndash;dashes&hellip;")


def test_docs_example():
    u = six.u('both em\u2014and&#x2013;dashes&hellip;')
    assert named_entities(u)   == 'both em&mdash;and&ndash;dashes&hellip;'
    assert numeric_entities(u) == 'both em&#8212;and&#8211;dashes&#8230;'
    assert unescape(u)   == six.u('both em\u2014and\u2013dashes\u2026')


def test_encode_ampersands():
    assert encode_ampersands("this & that") == "this &amp; that"

    assert encode_ampersands("this &amp; that") == "this &amp; that"
    # ha! not fooled!


def test_escape_function():
    esc = lambda s: s.replace('"', 'QUOTE')
    assert named_entities('and "this" is', escape=esc) == \
       'and QUOTEthisQUOTE is'


def test_escape():
    """
    Ensure that inline markup escaping works
    """
    s = '>that&this&#x2014;that<'
    # no encoding vs encoding, named entities
    assert named_entities(s) == six.u(">that&this&mdash;that<")
    assert named_entities(s, escape=True) == six.u("&gt;that&amp;this&mdash;that&lt;")

    # more complicated ampersand interleaving
    assert named_entities('&&#x2014;') == six.u("&&mdash;")
    assert named_entities('&&#x2014;', escape=True) == six.u("&amp;&mdash;")

    # decimal numeric entities, with escape
    assert numeric_entities(s) == six.u(">that&this&#8212;that<")
    assert numeric_entities(s, escape=True) == six.u("&gt;that&amp;this&#8212;that&lt;")

    # hexadecimal numeric entities, with escape
    assert hex_entities(s) == six.u(">that&this&#x2014;that<")
    assert hex_entities(s, escape=True) == six.u("&gt;that&amp;this&#x2014;that&lt;")

    # unicode entities, with escape
    assert unicode_entities(s) == six.u(">that&this\u2014that<")
    assert unicode_entities(s, escape=True) == six.u("&gt;that&amp;this\u2014that&lt;")

    # none entities, with escape
    assert none_entities(s) == six.u('>that&this&#x2014;that<')
    assert none_entities(s, escape=True) == six.u('&gt;that&amp;this&amp;#x2014;that&lt;')

    # entities API, with escape
    assert entities(s, 'named') == six.u(">that&this&mdash;that<")
    assert entities(s, 'named', escape=True) == six.u("&gt;that&amp;this&mdash;that&lt;")
    assert entities(s, 'numeric') == six.u(">that&this&#8212;that<")
    assert entities(s, 'numeric', escape=True) == six.u("&gt;that&amp;this&#8212;that&lt;")
    assert entities(s, 'decimal') == six.u(">that&this&#8212;that<")
    assert entities(s, 'decimal', escape=True) == six.u("&gt;that&amp;this&#8212;that&lt;")
    assert entities(s, 'hex') == six.u(">that&this&#x2014;that<")
    assert entities(s, 'hex', escape=True) == six.u("&gt;that&amp;this&#x2014;that&lt;")
    assert entities(s, 'none') == six.u(">that&this&#x2014;that<")
    assert entities(s, 'none', escape=True) == six.u('&gt;that&amp;this&amp;#x2014;that&lt;')
    assert entities(s, None) == six.u(">that&this&#x2014;that<")
    assert entities(s, None, escape=True) == six.u('&gt;that&amp;this&amp;#x2014;that&lt;')


def test_html_escape():
    t1 = 'this & that < other but > some'
    t1a = 'this &amp; that &lt; other but &gt; some'
    assert html_escape(t1) == t1a
    assert html_escape(t1, False) == t1a
    assert html_escape(t1, quote=False) == t1a

    t2 = """and 'some' more "stuff" """
    t2a = """and &#x27;some&#x27; more &quot;stuff&quot; """

    assert html_escape(t2) == t2a
    assert html_escape(t2, False) == t2
    assert html_escape(t2, quote=False) == t2


def test_unescape():
    t0 = 'needs no escape'
    u0 = unescape(t0)
    assert u0 == t0

    t1 = 'this&mdash;that &lt;p&gt; &amp; more'
    t1a = six.u('this\u2014that &lt;p&gt; &amp; more')
    u1 = unescape(t1)
    assert u1 == t1a

    t2 = 'this&mdash;that &#60;p&#62; &#38; more'
    t2a = six.u('this\u2014that &#60;p&#62; &#38; more')
    u2 = unescape(t2)
    assert u2 == t2a

    t3 = 'this&mdash;that &#x3c;p&#x3e; &#x26; more'
    t3a = six.u('this\u2014that &#x3c;p&#x3e; &#x26; more')
    u3 = unescape(t3)
    assert u3 == t3a
