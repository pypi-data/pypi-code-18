import datetime
import pytest
from .. import settings

settings.DATABASE = 'sqlite://'
settings.BASE_URL = 'http://example.com/'

from ..models import DefaultSession, Entry  # noqa


@pytest.fixture(scope='module')
def db(request):
    year = datetime.date.today().year
    session = DefaultSession()
    session.add(
        Entry(
            id='http://example.com/mock-title-1',
            updated=datetime.datetime(year, 5, 17, 0, 0, 10),
            published=datetime.datetime(year, 5, 17, 0, 0, 0),
            title='Mock Title 1',
            author='Mock Author 1',
            link='http://example.com/mock-title-1',
            summary='Mock summary 1',
            summary_type='text',
            content='<p>Mock content 1</p>',
            content_type='html',
            source_id='http://example.com/feed/atom/',
            source_title='Mock Source 1',
            source_link='http://example.com/feed/atom/'))
    session.add(
        Entry(
            id='http://example.com/mock-title-2',
            updated=datetime.datetime(year, 5, 18, 0, 0, 10),
            published=datetime.datetime(year, 5, 18, 0, 0, 0),
            title='Mock Title 2',
            author='Mock Author 2',
            link='http://example.com/mock-title-2',
            summary='<p>Mock summary 2</p>',
            summary_type='html',
            content='<p>Mock content 2</p>',
            content_type='html',
            source_id='http://example.com/feed/atom/',
            source_title='Mock Source 2',
            source_link='http://example.com/feed/atom/'))
    session.add(
        Entry(
            id='http://example.com/mock-title-3',
            updated=datetime.datetime(year, 5, 19, 0, 0, 10),
            published=datetime.datetime(year, 5, 19, 0, 0, 0),
            title='Mock Title 3',
            author='Mock Author 3',
            link='http://example.com/mock-title-3',
            summary='Mock summary 3',
            summary_type='text',
            content='<p>Mock content 3</p>',
            content_type='html',
            source_id='http://example.com/feed/atom/',
            source_title='Mock Source 3',
            source_link='http://example.com/feed/atom/'))
    session.add(
        Entry(
            id='https://claviger.net/mock-title-4',
            updated=datetime.datetime(year, 5, 19, 0, 0, 10),
            published=datetime.datetime(year, 5, 19, 0, 0, 0),
            title='Mock Title 4',
            author='Mock Author 4',
            link='https://claviger.net/mock-title-4',
            summary='Mock summary 4',
            summary_type='text',
            content='<p>Mock content 4</p>',
            content_type='html',
            source_id='https://claviger.net/feeds/all.atom',
            source_title='Mock Source 4',
            source_link='https://claviger.net/feeds/all.atom'))
    session.add(
        Entry(
            id='https://claviger.net/mock-title-5',
            updated=datetime.datetime(year, 5, 20, 0, 0, 10),
            published=datetime.datetime(year, 5, 20, 0, 0, 0),
            title='Mock Title 5',
            author='Mock Author 5',
            link='https://claviger.net/mock-title-5',
            summary='Mock summary 5',
            summary_type='text',
            content='<p>Mock content 5</p>',
            content_type='html',
            source_id='https://claviger.net/feeds/all.atom',
            source_title='Mock Source 5',
            source_link='https://claviger.net/feeds/all.atom'))
    session.add(
        Entry(
            id='https://claviger.net/nothing-in-common',
            updated=datetime.datetime(year, 4, 20, 0, 0, 10),
            published=datetime.datetime(year, 4, 20, 0, 0, 0),
            title='Nothing in Common',
            author='Mock Author 6',
            link='https://claviger.net/nothing-in-common',
            summary='Mock summary 6',
            summary_type='text',
            content='<p>Mock content 6</p>',
            content_type='html',
            source_id='https://claviger.net/feeds/all.atom',
            source_title='Mock Source 6',
            source_link='https://claviger.net/feeds/all.atom'))
    session.commit()

    def fin():
        session.query(Entry).filter_by(
            source_id='http://example.com/feed/atom/').delete()

    request.addfinalizer(fin)
    return session
