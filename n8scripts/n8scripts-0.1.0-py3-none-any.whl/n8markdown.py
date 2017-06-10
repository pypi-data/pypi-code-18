"""n8markdown.py

Customizations for publishing to n8henrie.com
"""

import re
from urllib.parse import urlparse

from markdown.treeprocessors import Treeprocessor
from markdown.postprocessors import Postprocessor
from markdown.extensions import Extension


class SetBlankTarget(Treeprocessor):
    def set_link_target(self, element):
        for child in element:
            if child.tag == "a" and child.get('href'):
                link = child.get('href')
                if not urlparse(link).netloc.endswith('n8henrie.com'):
                    child.set("target", "_blank")

            # run recursively on children
            self.set_link_target(child)

    def run(self, root):
        return self.set_link_target(root)


class FixCodeblocks(Postprocessor):
    def run(self, text):
        return re.sub(r"\n(</code></pre>)", "\g<1>", text)


class N8Markdown(Extension):
    def extendMarkdown(self, md, md_globals):
        md.treeprocessors.add('set_blank_target', SetBlankTarget(md), '_end')
        md.postprocessors.add('codeblock_newline', FixCodeblocks(md), '_end')


def makeExtension(configs=None):
    if configs is None:
        configs = {}
    return N8Markdown(configs=configs)
