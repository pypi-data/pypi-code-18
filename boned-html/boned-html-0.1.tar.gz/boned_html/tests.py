import unittest
from lxml import html

from .chunker import Elt, TextChunk, SkipChunk, HtmlChunker


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
                <span class="X" id="chunk-1">A test</span>
                <h1><span class="Y" id="chunk-2">With foo</span></h1>
                <span class="Y" id="chunk-3">but <b>also</b></span>
                <p><span class="X" id="chunk-4">there are some <em>difficulties.</em></span>
                <span class="Y" id="chunk-5"><em> <b>And</b> </em>sentences</span></p>
                <span class="Y" id="chunk-6">and tails.</span>
              </body>
            </html>"""
        expected = "".join(e.strip() for e in expected.split("\n"))

        def reformat(x):
            return "\n<".join(">\n".join(x.split(">")).split("<")).split("\n")

        result = self.chunker.unchunk(tree, chunks, classifications)
        self.assertEqual(
            reformat(html.tostring(result, encoding="utf-8").decode("utf-8")),
            reformat(expected))
