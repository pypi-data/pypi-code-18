from subconscious.model import RedisModel, Column
from uuid import uuid1
from .base import BaseTestCase
import enum


class StatusEnum(enum.Enum):
    ACTIVE = 'active'
    INACTIVE = 'inactive'


class TestUser(RedisModel):
    id = Column(primary_key=True)
    name = Column(index=True)
    age = Column(index=True, type=int)
    locale = Column(index=True, type=int, required=False)
    status = Column(type=str, enum=StatusEnum, index=True)


class TestOrderBy(BaseTestCase):
    def setUp(self):
        super(TestOrderBy, self).setUp()
        self.user_names = []
        for i in range(9):
            user = TestUser(id=str(uuid1()), name='name-{}'.format(i), age=i, locale=i+10, status='active')
            self.loop.run_until_complete(user.save(self.db))
            self.user_names.append(user.name)
        self.user_names_sorted_desc = sorted(self.user_names, reverse=True)

    def test_order_by(self):
        async def _test():
            user_names = [x.name async for x in TestUser.filter_by(self.db, status='active', order_by='name')]
            self.assertEqual(self.user_names, user_names)
            user_names = [x.name async for x in TestUser.filter_by(self.db, status='active', order_by='-name')]
            self.assertEqual(self.user_names_sorted_desc, user_names)

        self.loop.run_until_complete(_test())

    def test_query_with_order_by(self):
        async def _test():
            user_names = [x.name async for x in TestUser.query(self.db).filter(status='active').order_by('name')]
            self.assertEqual(self.user_names, user_names)
            user_names = [x.name async for x in TestUser.query(self.db).filter(status='active').order_by('-name')]
            self.assertEqual(self.user_names_sorted_desc, user_names)
        self.loop.run_until_complete(_test())

    def test_query_order_by_get_first(self):
        async def _test():
            user_name = await TestUser.query(self.db).filter(status='active').order_by('name').first()
            self.assertEqual(self.user_names[0], user_name.name)
            user_name = await TestUser.query(self.db).filter(status='active').order_by('-name').first()
            self.assertEqual(self.user_names[-1], user_name.name)
        self.loop.run_until_complete(_test())

    def test_query_with_limit(self):
        async def _test():
            user_names = [x.name async for x in TestUser.query(self.db).filter(
                status='active').order_by('name').offset(1).limit(3)]
            self.assertEqual(self.user_names[1:4], user_names)
            user_names = [x.name async for x in TestUser.query(self.db).filter(
                status='active').order_by('-name').offset(1).limit(3)]
            self.assertEqual(self.user_names_sorted_desc[1:4], user_names)
        self.loop.run_until_complete(_test())

    def test_empty_filter_by(self):
        async def _test():
            user_names = [x.name async for x in TestUser.query(self.db).order_by('name').offset(1).limit(3)]
            self.assertEqual(self.user_names[1:4], user_names)
        self.loop.run_until_complete(_test())
