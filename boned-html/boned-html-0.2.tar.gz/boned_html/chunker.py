"""
This module contains a class that does the though work of chunk / unchunking html.

You may look at :py:class:`.boner.HtmlBoner` if you are looking for a more usable class.
"""

import copy
from collections import namedtuple

from lxml import html


#: a sentence, a list of semantic elts to insert inside sentence, the original parent
TextChunk = namedtuple("TextChunk", "text elts parent istail")
#: skip chunk are chunk of html that does not contains sentences
SkipChunk = namedtuple("SkipChunk", "parent")
#: a semantic elt to insert in a sentence at a specific position
Elt = namedtuple("Elt", "elt start end")


def _s(s):
    """return an empty sentence for None
    """
    return "" if s is None else s


class HtmlChunker:
    """This utility chunk an html in text chunk, retaining the tags.
    You can then re-inject the text in html, while eg. adding a specific class.
    """

    #: tags that do not split text. Instead we will retain their position for later construction
    #: (cf. https://developer.mozilla.org/en-US/docs/Web/HTML/Element#Inline_text_semantics)
    #: but we removed br, as it generally means a different sentence.
    TEXT_SEMANTICS = {
        "a", "abbr", "b", "bdi", "bdo", "cite", "code", "data", "dfn", "em", "i", "kbd",
        "mark", "q", "rp", "rt", "rtc", "ruby", "s", "samp", "small", "span", "strong", "sub",
        "sup", "time", "u", "var", "wbr"}

    #: we won't search text inside those tags
    SKIPPED_TAGS = {
        "head", "script", "noscript", "style", "canvas"}

    def is_semantic(self, element):
        """:return bool: true if element is a "semantic element" (does not split text).
        """
        return (
            element.tag in self.TEXT_SEMANTICS and
            # verify children are also semantics
            all(self.is_semantic(e) for e in element))

    def shall_skip(self, element):
        """compute if element shall be skipped
        """
        return (
           element.tag in self.SKIPPED_TAGS or
           isinstance(element, html.HtmlComment) or
           not bool(element.text_content().strip()))

    def _process_semantic_child(self, element, start):
        """process children of elemets which are of type semantic.

        This use recursivity.

        :param element: the parent html element
        :param int start: the actual position in text
        :return tuple: the retrieved text
            and a list of Elt, semantic sub element with their points of insertion
        """
        text = _s(element.text)
        elts = []
        for child in element:
            subtext, subelts = self._process_semantic_child(child, start + len(text))
            text += subtext
            elts.extend(subelts)
        elts = [Elt(element, start, start + len(text))] + elts
        text += _s(element.tail)
        return text, elts

    def chunk_tree(self, tree, tail=None):
        """harvest sentences in html keeping its structure

        use recursivity.

        :param tree: the html element being processed
        :param tail: a list of semantic elements that are part of the tail of this element

        :return list: a list of :py:class:`TextChunk`
        """
        if tail is None:
            tail = []
        chunks = []
        if self.shall_skip(tree):
            chunks.append(SkipChunk(tree))
        else:
            # get text and children with their additional tail
            text = _s(tree.text)
            semantics = []
            children = []
            tails = []
            for child in tree:
                if self.is_semantic(child):
                    if not children:
                        # text before first children, so it's like element text
                        sub_text, sub_elts = self._process_semantic_child(child, len(text))
                        text += sub_text
                        semantics.extend(sub_elts)
                    else:
                        # add to last seen children tail
                        tails[-1].append(child)
                else:
                    # process later
                    children.append(child)
                    tails.append([])
            # make my text
            chunks.append(TextChunk(text, semantics, tree, False))
            # add children sentences
            for child, child_tail in zip(children, tails):
                chunks.extend(self.chunk_tree(child, child_tail))
        # process my tail
        if tree.tail or tail:
            text = _s(tree.tail)
            semantics = []
            for child in tail:
                sub_text, sub_elts = self._process_semantic_child(child, len(text))
                text += sub_text
                semantics.extend(sub_elts)
            chunks.append(TextChunk(text, semantics, tree, True))

        return chunks

    def _crossing_semantics(self, start, end, semantics):
        """from a list of html semantic elements,
        return the one that are included between start and end

        :param int start: start of interval to consider
        :param int end: end of interval
        :param semantics: list of Elt
        :return: list of Elt that are to consider for interval, shifted from start
        """
        for s in semantics:
            elt = None
            if s.start >= start and s.end <= end:
                elt = s  # included
            elif s.start <= start and s.end > start:
                elt = Elt(s.elt, start, min(end, s.end))  # crossing lower
            elif s.end >= end and s.start < end:
                elt = Elt(s.elt, max(start, s.start), end)  # crossing upper
            if elt is not None:
                # shift to have start, end relative to actual start
                yield Elt(elt.elt, elt.start - start, elt.end - start)

    def _introduce_semantics(self, sentence, semantics):
        """utility to unchunk, given a sentence and the list of semantics elements to insert
        return an intro text and etree children to rebuild original sentence.
        """
        if not semantics:
            return sentence, []

        intro = sentence[: semantics[0].start]

        children = []
        while semantics:
            child = semantics.pop(0)
            included = []
            while semantics and semantics[0].end <= child.end:
                s = semantics.pop(0)
                included.append(Elt(s.elt, s.start - child.start, s.end - child.start))
            # recursive
            child_intro, child_children = self._introduce_semantics(
                sentence[child.start:child.end], included)
            html_child = html.Element(
                child.elt.tag, attrib=child.elt.attrib)
            html_child.text = child_intro
            for c in child_children:
                html_child.append(c)
            # tail is text up to next element
            tail_end = semantics[0].start if semantics else None
            html_child.tail = sentence[child.end: tail_end]
            children.append(html_child)

        return intro, children

    def _rebuild_text(self, chunk, parent, sentence_classes,
                      span_id_prefix, no_class_no_span, chunk_num):
        """adding text to parent, sentence by sentence
        """
        # sentence by sentence
        sentence_num = -1
        sentence_start = 0
        last_element = parent
        grand_parent = parent.getparent()
        for sentence, classes in sentence_classes:
            if sentence is None:
                continue
            sentence_num += 1
            sentence_end = sentence_start + len(sentence)

            # reintroduced semantics elts
            crossing = list(
                self._crossing_semantics(sentence_start, sentence_end, chunk.elts))
            text, children = self._introduce_semantics(sentence, crossing)

            if classes or not no_class_no_span:
                if isinstance(classes, str):
                    classes = [classes]
                # we enclose text in a span of right class
                attrib = {}
                if span_id_prefix is not None:
                    attrib["id"] = "%s%d-%d" % (span_id_prefix, chunk_num, sentence_num)
                if classes:
                    attrib["class"] = " ".join(classes)
                span = html.Element("span", attrib=attrib)
                span.text = text
                for child in children:
                    span.append(child)
                if chunk.istail:
                    # by chance we are processing in an ordered manner, so we can append
                    grand_parent.append(span)
                else:
                    parent.append(span)
                last_element = span
            else:
                # we introduce our text
                if last_element != parent or chunk.istail:
                    last_element.tail = _s(last_element.tail) + text
                else:
                    last_element.text = _s(last_element.text) + text
                # and children
                if children:
                    _parent = grand_parent if chunk.istail else parent
                    for child in children:
                        _parent.append(child)
                    last_element = children[-1]
            sentence_start = sentence_end

    def unchunk(self, tree, chunks, chunk_classes, span_id_prefix="chunk-", no_class_no_span=True):
        """given a tree, it's chunks and classifications for sentences in chunks,
        rebuild the html with span and classes inside.

        :param tree: the tree the chunk where generated from
        :param chunks: a list of TextChunk/SkipChunk
        :param chunk_classes: a list of list of classes to apply to each text in each chunk
        :param span_id_prefix: a prefix for span added to html
        :return: a new tree
        """
        old_to_new = {}  # track elements between old and new tree
        for chunk_num, (chunk, sentence_classes) in enumerate(zip(chunks, chunk_classes)):
            if isinstance(chunk, SkipChunk):
                # just clone
                if chunk.parent is not None and chunk.parent.getparent() is not None:
                    new_parent = old_to_new[chunk.parent.getparent()]
                else:
                    # append to root
                    new_parent = tree
                new = copy.deepcopy(chunk.parent)
                # remove tail, as it was processed
                new.tail = ""
                new_parent.append(new)
                old_to_new[chunk.parent] = new
            elif not chunk.istail:
                old_parent = chunk.parent
                # make new parent
                new_parent = html.Element(
                    old_parent.tag, attrib=old_parent.attrib, nsmap=old_parent.nsmap)
                # map new and old
                old_to_new[old_parent] = new_parent
                # add to corresponding node, order is conserved by chunks so it works well
                old_ancestor = old_parent.getparent()
                if old_ancestor is not None:
                    new_ancestor = old_to_new[old_ancestor]
                    new_ancestor.append(new_parent)
            else:
                # this is tail so append text to parent
                if chunk.parent is not None:
                    new_parent = old_to_new[chunk.parent]
                else:
                    # append to root
                    new_parent = tree
            if not isinstance(chunk, SkipChunk):
                self._rebuild_text(
                    chunk, new_parent, sentence_classes,
                    span_id_prefix, no_class_no_span, chunk_num)

        return old_to_new[tree]
