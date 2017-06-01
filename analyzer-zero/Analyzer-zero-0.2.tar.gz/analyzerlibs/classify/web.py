import jieba
import jieba.analyse
from bs4 import BeautifulSoup
from analyzerlibs.wordslib import stat

def init(parallel=1):
    jieba.initialize()

class WebSta:
    def __init__(self, ana_instance, num=100, pro=1):
        self.processer_num = pro
        self.keys_num = num
        self._res = ana_instance
        self.text = ana_instance.text()
        self.css = len(ana_instance.css)
        self.script = len(ana_instance.script)
        self.links = ana_instance.links
        self.keys = jieba.analyse.extract_tags(self.text, num)
        self.words = list(jieba.cut(self.text))

    @property
    def words_sta(self):
        return stat.w_stat(self.words, self.processer_num, words=self.keys)

    @property
    def title(self):
        return { 'h' + str(i):len(self._res("h" + str(i))) for i in range(1,7)}

    @property
    def img(self):
        return {'img': len(self._res("img"))}

    @property
    def content(self):
        return {
            i: len(self._res(i))
            for i in ['ol', 'ul', 'li', 'div', 'span', 'p', 'i', 'b', 'br', 'img']
            
        }

    @property
    def meta(self):
        return {
            'meta': len(self._res("meta"))
        }

    @property
    def statistic(self):
        d = dict()
        d.update(self.title)
        d.update(self.content)
        d.update(self.img)
        d.update(self.meta)
        d.update({'css': self.css, 'script': self.script})
        return d

