"""The API class to use html boner

This module provide a class that helps you split an html in small text chunks,
at the level of one or more sentence.
You can then latter recompose the html adding a specific class to each text.

This is helpfull eg. to colorize html text after you have assigned a category to each sentence
(maybe using machine learning or whatever heuristic).
"""
from lxml import html

from .chunker import TextChunk, SkipChunk, HtmlChunker
from .exceptions import MismatchingText, UnasignableChunk


class HtmlBoner:
    """
    This class giving a simple API to chunk / unchunk an html.
    """

    chunker = HtmlChunker()

    def __init__(self, tree, span_id_prefix="chunk-", no_class_no_span=True):
        """
        :param tree: an etree compatible tree
        :param str span_id_prefix: a prefix to `id` property
          that will be added to span elements when rendering
        :paran bool no_class_no_span: tells the renderer that chunks without assigned classes
          should not be nested in a span.
        """
        self.orig_tree = tree
        self.chunks = self.chunker.chunk_tree(tree)
        self.span_id_prefix = span_id_prefix
        self.no_class_no_span = no_class_no_span
        # default classes
        self.classes = [[[text, None]] for text in list(self)]

    def __len__(self):
        """number of chunks
        """
        return len(self.chunks)

    def __iter__(self):
        """iter text in chunks
        """
        for chunk in self.chunks:
            yield chunk.text if isinstance(chunk, TextChunk) else None

    def __getitem__(self, n):
        """return text in chunk n
        """
        chunk = self.chunks[n]
        return chunk.text if isinstance(chunk, TextChunk) else None

    def set_classes(self, n, text_classes):
        """assign classes to a particular chunk

        :param text_classes: a list of list associating part of the text to a class.
          for comodity you may also just give a class to whole text.
        """
        chunk = self.chunks[n]
        if isinstance(chunk, SkipChunk):
            if (text_classes is not None and
                    text_classes and
                    len(text_classes[0]) > 1 and
                    text_classes[0][1] is not None):
                raise UnasignableChunk("Chunk %d can't receive a class" % n)
        else:
            orig_text = chunk.text
            if isinstance(text_classes, str):
                text_classes = [[orig_text, text_classes]]
            texts = [text for text, cls in text_classes]
            if "".join(texts) != orig_text:
                raise MismatchingText(
                    "provided text does not match original text at chunk %d: %s != %r" %
                    (n, texts, orig_text))
            self.classes[n] = text_classes

    def bulk_set_classes(self, text_classes):
        """assign classes to each text

        :param text_classes: a list of list of list associating part of the text to a class
        """
        for n, chunk_classes in enumerate(text_classes):
            self.set_classes(n, chunk_classes)

    @property
    def tree(self):
        """return a tree representing the html, eventually adding provided classes
        to chunk of texts
        """
        return self.chunker.unchunk(
            self.orig_tree, self.chunks, self.classes,
            span_id_prefix=self.span_id_prefix, no_class_no_span=True)

    def __str__(self):
        """render a representaton of the tree
        """
        return html.tostring(self.tree, encoding="utf-8").decode("utf-8")
