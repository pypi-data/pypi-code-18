from bs4 import BeautifulSoup
from lxml import html as ht
import logging


class Parser():
    tags_to_strip = ['span', 'em', 'a', 'b', 'br', 'html', 'body', 'p']

    def parse_results(self, html):
        """
        Parse web search results.
        Ignore universal (news, image etc) results.
        """
        xpaths = [
            "//div[@class='rc']"
        ]

        data = []
        doc = ht.document_fromstring(html)

        for xpath in xpaths:
            results = doc.xpath(xpath)
            if len(results) > 0:
                break

        if not results:
            return data

        # estimated = self.get_estimated(doc)
        # estimated_str = doc.xpath('//div[@id="resultStats"]/text()')

        for result in results:
            link = self.get_link(result)

            if len(link) > 0:
                # Ignore image links that are mixed in with standard results
                if not link.startswith('/images?q='):
                    title = self.get_title(result)
                    snippet = self.get_snippet(result)
                    row = [link, title, snippet]
                    data.append(row)

        return data

    def parse_next_page_link(self, html):
        """
        Parse next page link from html string.
        """
        doc = ht.document_fromstring(html)
        return self.get_next_page_link(doc)

    def get_next_page_link(self, html_tree):
        """
        Return next page link from results paginator.
        """
        try:
            return html_tree.xpath('//a[@id="pnnext"]/@href')[0]
        except KeyError:
            return None

    def get_link(self, html_tree):
        link = ''.join(html_tree.xpath('h3[@class="r"]/a/@href'))
        if link.startswith('/url?q='):
                        q = link.index('?q=')
                        sa = link.index('&sa=')
                        link = link[q + 3:sa]
        return link

    def get_title(self, html_tree):
        title = html_tree.xpath('h3[@class="r"]/a/text()')
        # Get rid of the em tags or we miss the keyword
        # from the title and snippet
        soup = BeautifulSoup("".join(title), 'lxml')
        for tag in self.tags_to_strip:
            for match in soup.findAll(tag):
                match.replaceWithChildren()

        title = soup.renderContents()
        return title

    def get_snippet(self, html_tree):
        xpath = 'div[@class="s"]//span[@class="st"]/text()'
        snippet = html_tree.xpath(xpath)
        soup = BeautifulSoup("".join(snippet), 'lxml')

        # Remove the dates inserted into some snippets by google
        elements_to_remove = soup.findAll("span", {"class": "f"})

        for element in elements_to_remove:
            element.extract()

        for tag in self.tags_to_strip:
            for match in soup.findAll(tag):
                match.replaceWithChildren()

        snippet = soup.renderContents()

        return snippet

    def get_estimated(self, html_tree):
        """
        Return estimated results from Google result page.
        """
        xpath = '//div[@id="resultStats"]/text()'
        try:
            estimated = "".join(html_tree.xpath(xpath))
        except:
            estimated = int(0)
            return estimated

        estimated = estimated.replace(',', '')
        estimated = estimated.replace('.', '')

        # Extract the integer number of estimated results
        # Sometimes page numbers are included, so we always take the
        # last integer from the string
        try:
            ints = [int(s) for s in estimated.split() if s.isdigit()]
            estimated = ints[len(ints) - 1]
        except IndexError:
            estimated = 0

        estimated = int(estimated)
        logging.debug("estimated results - Integer: " + str(estimated))

        return estimated
