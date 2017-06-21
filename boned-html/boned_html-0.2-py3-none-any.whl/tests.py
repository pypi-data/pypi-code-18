import unittest
from lxml import html

from .boner import HtmlBoner
from .chunker import Elt, TextChunk, SkipChunk, HtmlChunker
from .exceptions import MismatchingText, UnasignableChunk


class IntroduceSemanticsTestCase(unittest.TestCase):

    def setUp(self):
        self.chunker = HtmlChunker()

    def deconstruct_and_rebuild(self, original, element):
        chunks = self.chunker.chunk_tree(html.fromstring(original))
        sentence_chunk = chunks[0]

        intro, children = self.chunker._introduce_semantics(
            sentence_chunk.text, sentence_chunk.elts)

        body = html.Element(element)
        body.text = intro
        for c in children:
            body.append(c)

        return body

    def test_attribs(self):
        original = (
            """<div>""" +
            """<b class="test">Some <em border="solid" style="width:3em;">text</em></b>""" +
            """</div>""")
        body = self.deconstruct_and_rebuild(original, "div")
        self.assertEqual(
            original,
            html.tostring(body, encoding="utf-8").decode("utf-8"))

    def test_multi_level(self):
        original = ("<div>" +
                    "<b>We <em>have some</em> <a>silly <code><small>sentence</small>" +
                    " </code><sub>with a lot</sub> of</a> </b>" +
                    "complicated<sup><strong></strong> semantics</sup>" +
                    "</div>")
        body = self.deconstruct_and_rebuild(original, "div")
        self.assertEqual(
            original,
            html.tostring(body, encoding="utf-8").decode("utf-8"))


class ChunkTreeTestCase(unittest.TestCase):

    # TODO: add skipchunk tests

    def setUp(self):
        self.chunker = HtmlChunker()

    def simple_example(self):
        text = """<html>
          <head></head>
          <body>
            A test
            <h1>With foo</h1>
            but <b>also</b>
            <p>there are some <em>difficulties. <b>And</b> </em>sentences</p>
            and tails.
          </body>
        <html>"""
        # remove spaces for simplicity
        text = "".join(l.strip() for l in text.split("\n"))
        tree = html.fromstring(text)
        head, body = list(tree)
        h1, b, p = list(body)
        em, = list(p)
        em_b, = list(em)
        chunks = [
            TextChunk('',  [],  tree,  False),
            SkipChunk(head),
            TextChunk('A test',  [],  body,  False),
            TextChunk('With foo',  [],  h1,  False),
            TextChunk('but also',  [Elt(b, 4, 8)],  h1,  True),
            TextChunk('there are some difficulties. And sentences',
                      [Elt(em, 15, 33), Elt(em_b, 29, 32)],  p,  False),
            TextChunk('and tails.',  [],  p,  True)]
        return text, tree, chunks

    def test_chunk(self):
        text, tree, expected = self.simple_example()
        chunks = self.chunker.chunk_tree(tree)
        self.assertEqual(chunks, expected)
        # verify positions
        text, elt = chunks[4].text, chunks[4].elts[0]
        self.assertEqual(text[elt.start: elt.end], "also")
        text, elt = chunks[5].text, chunks[5].elts[0]
        self.assertEqual(text[elt.start: elt.end], "difficulties. And ")
        text, elt = chunks[5].text, chunks[5].elts[1]
        self.assertEqual(text[elt.start: elt.end], "And")

    def test_unchunk(self):
        text, tree, chunks = self.simple_example()
        classifications = [
            [[None, 'X']],
            [[None, 'Y']],
            [['A test', 'X']],
            [['With foo', 'Y']],
            [['but also', 'Y']],
            [['there are some difficulties.', 'X'], [' And sentences', 'Y']],
            [['and tails.', 'Y']]]
        expected = """<html>
              <head></head>
              <body>
                <span class="X" id="chunk-2-0">A test</span>
                <h1><span class="Y" id="chunk-3-0">With foo</span></h1>
                <span class="Y" id="chunk-4-0">but <b>also</b></span>
                <p><span class="X" id="chunk-5-0">there are some <em>difficulties.</em></span>
                <span class="Y" id="chunk-5-1"><em> <b>And</b> </em>sentences</span></p>
                <span class="Y" id="chunk-6-0">and tails.</span>
              </body>
            </html>"""
        expected = "".join(e.strip() for e in expected.split("\n"))

        def reformat(x):
            return "\n<".join(">\n".join(x.split(">")).split("<")).split("\n")

        result = self.chunker.unchunk(tree, chunks, classifications)
        self.assertEqual(
            reformat(html.tostring(result, encoding="utf-8").decode("utf-8")),
            reformat(expected))


def _striped(l):
    return [s.strip() for s in l]


class BonerTestCase(unittest.TestCase):

    HTML = """
        <html>
          <head></head>
          <body>
            A test
            <h1>With foo</h1>
            And <em>bar</em>.
          </body>
        </html>""".strip()

    def test_base_read_api(self):
        tree = html.fromstring(self.HTML)
        boner = HtmlBoner(tree)
        texts = ["", None, "", "A test", "With foo", "And bar.", ""]
        self.assertEqual(
            list(s.strip() if s is not None else None for s in boner),
            texts)
        self.assertEqual(len(boner), len(texts))
        self.assertEqual(boner[0].strip(), "")
        self.assertEqual(boner[3].strip(), "A test")
        self.assertEqual(boner[-2].strip(), "And bar.")
        self.assertEqual(str(boner), self.HTML)  # no change

    def test_index_error(self):
        tree = html.fromstring(self.HTML)
        boner = HtmlBoner(tree)
        with self.assertRaises(IndexError):
            boner[1000]

    def test_assign_class_str(self):
        tree = html.fromstring(self.HTML)
        boner = HtmlBoner(tree)
        boner.set_classes(4, "foo")
        # retrieve element
        self.assertEqual(boner.tree.xpath("//span[@class = 'foo']/text()"), ["With foo"])
        self.assertEqual(boner.tree.xpath("//span[@id = 'chunk-4-0']/text()"), ["With foo"])
        boner.set_classes(-2, "foo")
        # retrieve elements
        self.assertEqual(
            _striped(boner.tree.xpath("//span[@class = 'foo']//text()")),
            ["With foo", "And", "bar", "."])
        self.assertEqual(
            _striped(boner.tree.xpath("//span[@id = 'chunk-5-0']//text()")),
            ["And", "bar", "."])

    def test_assign_class_list(self):
        tree = html.fromstring(self.HTML)
        boner = HtmlBoner(tree)
        boner.set_classes(4, [["With ", None], ["foo", "foo"]])
        self.assertEqual(boner.tree.xpath("//span[@class = 'foo']/text()"), ["foo"])

    def test_assign_class_skip(self):
        tree = html.fromstring(self.HTML)
        boner = HtmlBoner(tree)
        boner.set_classes(1, [["", None]])
        boner.set_classes(1, [])
        boner.set_classes(1, None)
        with self.assertRaises(UnasignableChunk):
            boner.set_classes(1, [["foo", "bar"]])

    def test_bulk_set_classes(self):
        # stripping for convenience
        stripped_html = "\n".join(_striped(self.HTML.split("\n")))
        tree = html.fromstring(stripped_html)
        boned = HtmlBoner(tree)
        boned.bulk_set_classes([
            [["\n", None]],
            None,
            [["\n", None]],
            [["\nA test\n", "foo"]],
            [["With ", None], ["foo", "foo"]],
            [["\nAnd bar", "bar"], [".\n", None]],
            [["\n", "empty"]],
        ])
        btree = boned.tree
        self.assertEqual(btree.xpath("//span[@class='foo']/text()"), ["\nA test\n", "foo"])
        self.assertEqual(btree.xpath("//span[@class='bar']//text()"), ["\nAnd ", "bar", ""])
        self.assertEqual(btree.xpath("//span[@class='empty']/text()"), ["\n"])

    def test_bad_set_class(self):
        tree = html.fromstring(self.HTML)
        boner = HtmlBoner(tree)
        with self.assertRaises(MismatchingText):
            boner.set_classes(0, [["foo", "bar"]])
        with self.assertRaises(MismatchingText):
            boner.set_classes(4, [["foo", "bar"]])
        with self.assertRaises(MismatchingText):
            boner.set_classes(4, [["", "bar"]])

    def test_complex_tails(self):
        original = ("<html><body>a <i>simple</i> paragraph <p>and</p> " +
                    "a <em>big <strong>complicated</strong></em> " +
                    "wizzy <i>long</i> tail</body></html>")
        tree = html.fromstring(original)
        boned = HtmlBoner(tree)
        new = str(boned)
        self.assertEqual(
            original,
            new)

        # add classes to complexify
        boned.set_classes(1, [["a simple", None], [" ", "x"], ["paragraph", None], [" ", None]])
        boned.set_classes(
            3, [[" a big", "x"], [" complicated ", None], ["wizzy long", None], [" tail", "y"]])
        new = str(boned)
        self.assertEqual(
            new,
            '<html><body>a <i>simple</i><span class="x" id="chunk-1-1"> </span>paragraph ' +
            '<p>and</p><span class="x" id="chunk-3-0"> a <em>big</em></span><em> ' +
            '<strong>complicated</strong></em> wizzy <i>long</i>' +
            '<span class="y" id="chunk-3-3"> tail</span></body></html>')

    def test_attr_kept(self):
        orig_html = (
            '<html style="color:black;"><body>' +
            'some <p class="foo"> <a href="#">text</a> </p>' +
            '</body></html>')
        tree = html.fromstring(orig_html)
        boner = HtmlBoner(tree, span_id_prefix="foo")
        self.assertEqual(str(boner), orig_html)
        boner.set_classes(1, "bar")
        boner.set_classes(2, "baz")
        btree = boner.tree
        self.assertEqual(btree.xpath('//html/@style'), ["color:black;"])
        self.assertEqual(btree.xpath('//p/@class'), ["foo"])
        self.assertEqual(btree.xpath('//a/@href'), ["#"])

    def test_span_id_prefix(self):
        tree = html.fromstring(self.HTML)
        boner = HtmlBoner(tree, span_id_prefix="foo-")
        boner.set_classes(3, "bar")
        boner.set_classes(4, "baz")
        btree = boner.tree
        self.assertTrue(
            btree.xpath("//span[@id='foo-3-0']//text()"))
        self.assertTrue(
            btree.xpath("//span[@id='foo-4-0']//text()"))

    def test_span_everywhere(self):
        tree = html.fromstring("<html><body> a <p>simple</p> <b>test</b>. </body></html>")
        boner = HtmlBoner(tree, no_class_no_span=False)
        self.assertEqual(
            str(boner),
            "<html><body> a <p>simple</p> <b>test</b>. </body></html>")
