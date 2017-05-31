# coding=utf8
from unittest import TestCase

from sqlalchemy import create_engine, Column, Integer
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy.orm import sessionmaker, scoped_session


class TestRongService(TestCase):
    def test_update_token (self):
        engine = create_engine('postgresql+psycopg2://liming:@localhost/rongbing', convert_unicode=True, echo=True)
        db = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))

        class DeclaredBase(object):
            id = Column(Integer, primary_key=True, autoincrement=True)

        Base = declarative_base(cls=DeclaredBase)
        from rongyun_binding import RongService, bind_models
        bind_models(Base, db)
        Base.metadata.create_all(engine)

        RongService.initialize('0vnjpoad0c1iz', 'WaoOjj3RmebDBr')

        rong_id, rong_token = RongService.instance().update_token(1, 233, '123123', user_name="test123123")
        self.assertTrue(True)






