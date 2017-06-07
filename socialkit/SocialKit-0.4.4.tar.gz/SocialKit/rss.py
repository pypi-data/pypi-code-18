import base64
from qlib.data.sql import SqlObjectEngine, Table, SqlEngine
from .parser import XmlParser

class RssResource(Table):
    resfrom = str
    geo = str
    about = str
    url = str

    def __repr__(self):
        return self.geo + "|" + self.url


class Rss(Table):
    title = str
    pubDate = str
    lang = str
    descr = str

    def __repr__(self):
        return self.title + "|" + self.pubDate


class RssContent(Table):
    content = 'None'
    title = str
    link = str
    pubDate = str
    descr = str
    belongto = Rss

    def __repr__(self):
        return self.title + "|" + self.pubDate


class RssTag(Table):
    name = str
    belongto = RssContent

    def __repr__(self):
        return self.name + " | " + str(self.belongto)

class ItemDoc:

    def __init__(self, item, category=None):
        self.category = set()
        if isinstance(item, RssContent):
            for i in item._columns():
                setattr(self, i, getattr(item, i))
            if category:
                self.category = category
        else:
            for i in item.iter():
                if ':'  in i.tag:
                    continue
                if i.tag == 'category':
                    self.category.add( next(i.itertext()) )
                    continue

                setattr(self, i.tag, next(i.itertext()))

    def __getitem__(self, k):
        for t in self.category:
            if k in t:
                return True
        if len(self.description.split(k)) > 2:
            return True

        return False

    def save(self, rss_handler, rssbelong):
        rss_handler.save('C', title = self.title, pubDate= self.pubDate, link=self.link, descr = self.description, belongto = rssbelong)
        this = rss_handler._db.last(RssContent, pubDate= self.pubDate, link=self.link)
        for t in self.category:
            rss_handler.save('T',name=t, belongto=this)

    def __repr__(self):
        return self.title + " | " + self.pubDate

class RssDoc:

    def __init__(self, rss_handler, xml_content):
        self.title = xml_content("channel > title").text()
        self.descr = xml_content("channel > description").text()
        self.lang = xml_content("channel > language").text()
        self.pubDate = xml_content("channel > pubDate").text()
        self.items = [ItemDoc(i) for i in xml_content("channel > item")]
        self.rss_handler = rss_handler

    def __getitem__(self, k):
        for i in self.items:
            if i[k]:
                yield i

    def save(self):
        self.rss_handler.save('D' ,title=self.title, pubDate = self.pubDate, lang=self.lang, descr=self.descr)
        belongtoRss = self.rss_handler._db.last(Rss, title=self.title)
        if belongtoRss:
            [i.save(self.rss_handler, belongtoRss) for i in self.items ]


    def __repr__(self):
        return self.title + " | " + self.pubDate

class RssHandler:

    def __init__(self, database=None):
        self.database = database
        self._db = SqlObjectEngine(database=database)
        try:
            self._db.create(Rss)
            self._db.create(RssResource)
            self._db.create(RssContent)
            self._db.create(RssTag)
            
        except Exception as e:
            pass

    def load(self, type, **condition):
        if type == 'C':
            c = RssContent
        elif type == 'D':
            c = Rss
        elif type == 'R':
            c = RssResource
        elif type == 'T':
            c = RssTag
        else:
            raise Exception("not support this type , only C/T/R .")
        
        res = self._db.find(c, **condition)
        return res

    def save(self, type, **kargs):
        if type == 'C':
            c = RssContent
        elif type == 'D':
            c = Rss
        elif type == 'R':
            c = RssResource
        elif type == 'T':
            c = RssTag
        else:
            raise Exception("not support this type , only C/T/R .")
        for i in kargs:
            if 'desc' in i:
                kargs[i] = base64.b64encode(kargs[i].encode()).decode("utf8")
        r = c(**kargs)
        if not self._db.find_one(c, **kargs):
            self._db.add(r)
            return True
        else:
            return False

    def parse(self, xml_content):
        if not isinstance(xml_content, bytes):
            return RssDoc(self, XmlParser(xml_content.encode()))
        return RssDoc(self, XmlParser(xml_content))

    def list(self):
        return [i for i in self.load('R')]


    def list_cate(self):
        return [i for i in self.load("T")]

    def __getitem__(self,k):
        res = {}

        for tag in self._db.sql.search("RssTag",'belongto',name=k):
            i = ItemDoc(self._db.find_one(RssContent, ID=tag[0]))
            if i.__repr__() not in res:
                res[i.__repr__()] = i
        return list(res.values())


    def __del__(self):
        self._db.close()

