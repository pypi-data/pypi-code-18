import re


class Text:
    def __init__(self, content, hashtags=list(), links=list()):
        self.content = content
        self.tweet_links = []
        self.external_links = []
        self.links = links
        self.hashtags = hashtags
        self._separate_links(links)

    def __add__(self, other):
        res_hashs = self.hashtags
        for oh in other.hashtags:
            if oh not in res_hashs:
                res_hashs.append(oh)
        return Text(self.content + other.content,
                    res_hashs,
                    self.links + other.links)

    def __repr__(self):
        res = 'content:\n'
        res += '\t\"' + self.content + '\"\n'
        if self.hashtags:
            res += 'hashtags:\n'
            for h in self.hashtags:
                res += '\t' + h + '\n'
        if self.external_links:
            res += 'external links:\n'
            for l in self.external_links:
                res += '\t' + l + '\n'
        if self.tweet_links:
            res += 'tweet links:\n'
            for l in self.tweet_links:
                res += '\t' + l + '\n'
        return res

    def _separate_links(self, links):
        for l in links:
            if re.match("^http[s]?://(www\.)?twitter.com(.*)", l):
                self.tweet_links.append(l)
            else:
                self.external_links.append(l)

    def get_external_links(self):
        return self.external_links

    def get_content(self):
        return self.content
