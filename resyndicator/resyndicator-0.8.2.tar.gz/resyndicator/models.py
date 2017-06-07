from utilofies.stdlib import canonicalized
from sqlalchemy import create_engine, Column, DateTime, Unicode
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base
from . import settings


DefaultBase = declarative_base(name='DefaultBase')  # The default base
CustomBase = declarative_base(name='CustomBase')  # The base to be used outside the module
engine = create_engine(settings.DATABASE)


class DefaultSession:
    """Session that creates the default table."""

    def __new__(cls):
        """Session proxy to delay relation creation."""
        DefaultBase.metadata.create_all(engine)
        Session = scoped_session(sessionmaker(bind=engine))
        return Session()


class CustomSession:
    """Session that creates any custom tables."""

    def __new__(cls):
        """Session proxy to delay relation creation."""
        CustomBase.metadata.create_all(engine)
        Session = scoped_session(sessionmaker(bind=engine))
        return Session()


class EntryBase(object):
    """
    An abstract entry not bound to SQLAlchemy. Subclass it as mix-in together with the
    `CustomBase` to create your own database representation. Use `Entry` to use the default.
    """
    __tablename__ = 'entry'

    created = False  # Resyndicator-internal marker

    id = Column(Unicode, primary_key=True)
    updated = Column(DateTime, index=True, nullable=False)
    published = Column(DateTime)
    fetched = Column(DateTime)
    title = Column(Unicode)
    author = Column(Unicode)
    link = Column(Unicode, index=True)
    summary = Column(Unicode)
    summary_type = Column(Unicode)
    content = Column(Unicode)
    content_type = Column(Unicode)
    source_id = Column(Unicode)
    source_title = Column(Unicode)
    source_link = Column(Unicode, index=True)

    def as_dict(self):
        return canonicalized({
            'id': self.id,
            'updated': self.updated,
            'published': self.published,
            'title': self.title,
            'author': self.author,
            'link': self.link,
            'description': self.summary,
            'content': self.content,
            'source': {'id': self.source_id,
                       'title': self.source_title,
                       'updated': self.updated,
                       'links': [{'href': self.source_link, 'rel': 'self'}]}})

    def __repr__(self):
        return '<BaseEntry({id})>'.format(id=self.id)


class Entry(EntryBase, DefaultBase):
    """Default SQLAlchemy entry representation."""
    pass
