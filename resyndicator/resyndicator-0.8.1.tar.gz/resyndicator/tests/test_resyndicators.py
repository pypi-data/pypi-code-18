import pytest
from datetime import timedelta, datetime
from sqlalchemy.sql import or_
from ..models import Entry
from ..resyndicators import Resyndicator


resyndicator1 = Resyndicator(
    title='Resyndicator 1',
    past=timedelta(days=365),
    query=or_(
        Entry.source_link.in_([
            'http://example.com/feed/atom/',
            'http://feeds.feedburner.com/TheGivewellBlog',
        ])
    ),
    cluster_level=0.1
)
resyndicator2 = Resyndicator(
    title='Resyndicator 2',
    past=timedelta(days=365),
    query=or_(
        Entry.source_link.in_([
            'http://weird-address.com/',
        ])
    )
)
resyndicator_clustered = Resyndicator(
    title='Resyndicator Clustered',
    past=timedelta(days=365),
    query=or_(
        Entry.source_link.in_([
            'https://claviger.net/feeds/all.atom',
        ])
    ),
    cluster_level=0.7
)


@pytest.mark.parametrize('resyndicator,length', [
    (resyndicator1, 3),
    (resyndicator2, 0),
])
def test_get_entries(db, resyndicator, length):
    assert len(resyndicator.entries()) == length


@pytest.mark.parametrize('resyndicator,field,value', [
    (resyndicator1, 'title', 'Mock Title 3'),
    (resyndicator1, 'author', 'Mock Author 3'),
    (resyndicator1, 'link', 'http://example.com/mock-title-3'),
    (resyndicator1, 'updated', datetime(2017, 5, 19, 0, 0, 10)),
    (resyndicator1, 'published', datetime(2017, 5, 19, 0, 0)),
    (resyndicator1, 'summary', 'Mock summary 3'),
    (resyndicator1, 'summary_type', 'text'),
    (resyndicator1, 'content', '<p>Mock content 3</p>'),
    (resyndicator1, 'content_type', 'html'),
])
def test_entries(db, resyndicator, field, value):
    assert getattr(resyndicator.entries()[0], field) == value


@pytest.mark.parametrize('resyndicator,length', [
    (resyndicator1, 3),
    (resyndicator2, 0),
])
def test_feed_entries(db, resyndicator, length):
    feed = resyndicator.feed()
    assert feed.count('<entry') == length


def test_clustered_feed(db):
    entries = resyndicator_clustered.entries()
    feed = resyndicator_clustered.feed()
    assert feed.count('<entry') == 2
    assert len(entries) == 2
    assert entries[0].updated.day == 19  # The older one
    assert entries[0].title == 'Mock Title 4'
