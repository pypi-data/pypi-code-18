import pytest
import feedparser
from datetime import datetime
from utilofies.bslib import intelligent_decode
from ..fetchers.feed import FeedFetcher


class MockFeedFetcher(FeedFetcher):

    def __init__(self, url, encoding, *args, **kwargs):
        super().__init__(url, 60, *args, **kwargs)
        self.encoding = encoding
        self.update()

    def update(self):
        with open('resyndicator/tests/samples/' + self.url, 'rb') as feedfile:
            content = feedfile.read()
        dammit = intelligent_decode(
            markup=content, override_encodings=(self.encoding,))
        self.source = feedparser.parse(dammit.unicode_markup)
        self.raw_entries = self.source.entries


fetchers = {
    'boersen-zeitung.de.rss': MockFeedFetcher('boersen-zeitung.de.rss', 'utf-8'),
    'broken-encoding.rss': MockFeedFetcher('broken-encoding.rss', 'iso-8859-2'),
    'dailymail-articles.rss.xml': MockFeedFetcher('dailymail-articles.rss.xml', 'utf-8'),
    'ea-stiftung.org.windows-1252.rss': MockFeedFetcher('ea-stiftung.org.windows-1252.rss', 'windows-1252'),
    'entities-in-description.rss': MockFeedFetcher('entities-in-description.rss', 'utf-8'),
    'slightly-broken-encoding.rss': MockFeedFetcher('slightly-broken-encoding.rss', 'utf-8'),
    'valid-encoding.iso-8859-2.rss': MockFeedFetcher('valid-encoding.iso-8859-2.rss', 'iso-8859-2'),
    'valid-named-entities.rss': MockFeedFetcher('valid-named-entities.rss', 'utf-8'),
    'valid-numerical-entities.atom': MockFeedFetcher('valid-numerical-entities.atom', 'utf-8'),
    'wz-net.de.rss': MockFeedFetcher('wz-net.de.rss', 'utf-8'),
}


@pytest.mark.parametrize('fetcher', [
    fetchers['boersen-zeitung.de.rss'],
    fetchers['broken-encoding.rss'],
    fetchers['dailymail-articles.rss.xml'],
    fetchers['ea-stiftung.org.windows-1252.rss'],
    fetchers['entities-in-description.rss'],
    fetchers['slightly-broken-encoding.rss'],
    fetchers['valid-encoding.iso-8859-2.rss'],
    fetchers['valid-named-entities.rss'],
    fetchers['valid-numerical-entities.atom'],
    fetchers['wz-net.de.rss'],
])
def test_parsing(fetcher):
    for entry in fetcher.entries:
        assert entry.id  # Just to prove that the entry has been parsed


@pytest.mark.parametrize('fetcher,title', [
    (fetchers['boersen-zeitung.de.rss'], 'Sachsenmilch AG: Widerruf der Zulassung zum Handel im regulierten Markt der Frankfurter'),
    # (fetchers['broken-encoding.rss'], '"Strażacy" (TVP 1) mają mniej widzów niż rok temu'),  # Confirmed correct by native speaker
    (fetchers['dailymail-articles.rss.xml'], "Verizon to pay $1.4M in 'supercookie' FCC settlement"),
    (fetchers['ea-stiftung.org.windows-1252.rss'], 'Stellenangebote Herbst 2015'),
    (fetchers['entities-in-description.rss'], 'A montra da natureza algarvia arranca esta sexta-feira em Tavira'),
    (fetchers['slightly-broken-encoding.rss'], 'Jak zrobić krzesło do ogrodu z dwóch desek'),
    # (fetchers['valid-encoding.iso-8859-2.rss'], 'Naukowcy potwierdzają: tak poprawisz swoje życie erotyczne'),
    (fetchers['valid-named-entities.rss'], 'Silly - „Wutfänger“ kommt am 6. Mai'),
    (fetchers['valid-numerical-entities.atom'], 'Dresden – Militärhistorsiches Museum'),
    (fetchers['wz-net.de.rss'], 'Brüssel rechnet mit drei Millionen Flüchtlingen'),
])
def test_titles(fetcher, title):
    assert fetcher.title
    assert next(fetcher.entries).title == title


@pytest.mark.parametrize('fetcher,summary', [
    (fetchers['boersen-zeitung.de.rss'], 'Sachsenmilch AG: Widerruf der Zulassung zum Handel'),
    (fetchers['broken-encoding.rss'], '<p>Drugi sezon serialu "Straşacy" w TVP 1 zadebiu'),
    (fetchers['dailymail-articles.rss.xml'], 'NEW YORK (AP) — Verizon will pay a $1.35 million f'),
    (fetchers['ea-stiftung.org.windows-1252.rss'], '<p>Die EAS ist in den letzten Monaten stark gewach'),
    (fetchers['entities-in-description.rss'], 'A Algarve Nature Week começa a 5 de Maio, no Sítio'),
    (fetchers['slightly-broken-encoding.rss'], '<img src="https://i.ytimg.com/vi/-IZ0MHIZuVc/maxre'),
    (fetchers['valid-named-entities.rss'], 'Hört hier in die erste Singleauskopplung rein'),
    (fetchers['valid-numerical-entities.atom'], 'Ich habe mich mal wieder ein wenig der Architektur'),
    (fetchers['wz-net.de.rss'], 'Brüßel (dpa) - In Europa dürften nach Einschätzung'),
])
def test_summaries(fetcher, summary):
    assert next(fetcher.entries).summary.startswith(summary)


@pytest.mark.parametrize('fetcher,content', [
    (fetchers['valid-numerical-entities.atom'], '<p style="text-align: justify;">Ich habe mich mal wieder ein wenig der Architektur gewidmet&#8230;also zumindest beim'),
])
def test_contents(fetcher, content):
    assert next(fetcher.entries).content.startswith(content)


@pytest.mark.parametrize('fetcher,id', [
    (fetchers['boersen-zeitung.de.rss'], 'https://www.boersen-zeitung.de/index.php?isin=&dpasubm=all&ansicht=meldungen&dpaid=834531'),
    (fetchers['broken-encoding.rss'], 'http://www.press.pl/newsy/pokaz.php?id=51890&rss=1'),
    (fetchers['dailymail-articles.rss.xml'], 'http://www.dailymail.co.uk/wires/ap/article-3480743/Verizon-pay-1-4M-supercookie-FCC-settlement.html?ITO=1490&ns_mchannel=rss&ns_campaign=1490'),
    (fetchers['ea-stiftung.org.windows-1252.rss'], '55c31ff3e4b0242e8b105638:55d7116fe4b0edd145cdb437:5627bfd4e4b045ddfccc8f40'),
    (fetchers['entities-in-description.rss'], 'urn:uuid:e6e8cba7-2916-2d42-911c-e9e7bd4fcb56'),
    (fetchers['slightly-broken-encoding.rss'], 'http://www.spryciarze.pl/zobacz/jak-zrobic-krzeslo-do-ogrodu-z-dwoch-desek'),
    (fetchers['valid-encoding.iso-8859-2.rss'], '19752121'),
    (fetchers['valid-named-entities.rss'], 'http://www.cdstarts.de/nachrichten/152896-Silly-Wutfaenger-kommt-am-6-Mai.html'),
    (fetchers['valid-numerical-entities.atom'], 'http://fotosichtweise.de/blog/?p=4428'),
    (fetchers['wz-net.de.rss'], 'http://www.wz-net.de/index.php?kat=20&ausgabe=69968&redaktion=1&artikel=110992073&sara=awesomeness&ea=opportunity'),
])
def test_ids(fetcher, id):
    assert fetcher.id
    assert next(fetcher.entries).id == id


@pytest.mark.parametrize('fetcher,updated', [
    (fetchers['boersen-zeitung.de.rss'], datetime(2015, 11, 5, 11, 14, 36)),
    (fetchers['broken-encoding.rss'], datetime(2016, 3, 23, 11, 20, 54)),
    (fetchers['dailymail-articles.rss.xml'], datetime(2016, 3, 7, 17, 41, 16)),
    (fetchers['ea-stiftung.org.windows-1252.rss'], datetime(2015, 10, 21, 17, 58, 10)),
    (fetchers['entities-in-description.rss'], datetime(2017, 5, 4, 11, 52, 21)),
    (fetchers['slightly-broken-encoding.rss'], datetime(2016, 3, 21, 13, 0)),
    (fetchers['valid-encoding.iso-8859-2.rss'], datetime(2016, 3, 11, 12, 46)),
    (fetchers['valid-named-entities.rss'], datetime(2016, 3, 22, 15, 52)),
    (fetchers['valid-numerical-entities.atom'], datetime(2016, 3, 13, 16, 59, 38)),
    (fetchers['wz-net.de.rss'], datetime(1970, 1, 1, 0, 0)),
])
def test_updated_dates(fetcher, updated):
    assert next(fetcher.entries).updated == updated


@pytest.mark.parametrize('fetcher,link', [
    (fetchers['boersen-zeitung.de.rss'], 'https://www.boersen-zeitung.de/index.php?isin=&dpasubm=all&ansicht=meldungen&dpaid=834531&sara=awesomeness&ea=opportunity'),
    (fetchers['broken-encoding.rss'], 'http://www.press.pl/newsy/pokaz.php?id=51890&rss=1'),
    (fetchers['dailymail-articles.rss.xml'], 'http://www.dailymail.co.uk/wires/ap/article-3480743/Verizon-pay-1-4M-supercookie-FCC-settlement.html?ITO=1490&ns_mchannel=rss&ns_campaign=1490'),
    (fetchers['ea-stiftung.org.windows-1252.rss'], 'http://www.ea-stiftung.org/blog/blog/stellenangebote-herbst-2015?sara=awesomeness&ea=opportunity'),
    (fetchers['entities-in-description.rss'], 'http://fugas.publico.pt/Noticias/373244_a-montra-da-natureza-algarvia-arranca-esta-sexta-feira-em-tavira'),
    (fetchers['slightly-broken-encoding.rss'], 'http://www.spryciarze.pl/zobacz/jak-zrobic-krzeslo-do-ogrodu-z-dwoch-desek'),
    (fetchers['valid-encoding.iso-8859-2.rss'], 'http://www.logo24.pl/Logo24/56,85832,19752121,naukowcy-potwierdzaja-tak-poprawisz-swoje-zycie-erotyczne.html'),
    (fetchers['valid-named-entities.rss'], 'http://www.cdstarts.de/nachrichten/152896-Silly-Wutfaenger-kommt-am-6-Mai.html'),
    (fetchers['valid-numerical-entities.atom'], 'http://fotosichtweise.de/blog/2016/dresden-militaerhistorsiches-museum/'),
    (fetchers['wz-net.de.rss'], 'http://www.wz-net.de/index.php?kat=20&ausgabe=69968&redaktion=1&artikel=110992073&sara=awesomeness&ea=opportunity'),
])
def test_links(fetcher, link):
    assert fetcher.link
    assert next(fetcher.entries).link == link
