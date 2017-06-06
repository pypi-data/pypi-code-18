# coding: utf8

# Copyright 2013-2015 Vincent Jacques <vincent@vincent-jacques.net>

import unittest


class MockException(Exception):
    """
    @todoc
    """

from .expectation_grouping import OrderedExpectationGroup, UnorderedExpectationGroup, AtomicExpectationGroup, OptionalExpectationGroup, AlternativeExpectationGroup, RepeatedExpectationGroup
from .expectation_handling import ExpectationHandler
from .replacer import Replacer

# @todo When an arguments validator fails, include description of failure in exception (see PyGithub's replay mode: comparers have to log by themselves to make it practical)


class TestCase(unittest.TestCase):
    """
    TestCase()

    A convenience base class for test cases needing a single mock :class:`Engine`.
    It inherits from :class:`unittest.TestCase` and sets-up and tears-down one for you.
    """

    @property
    def mocks(self):
        """
        The mock :class:`Engine`.
        """
        return self.__mocks

    def setUp(self):
        """
        Do not forget to call the base version if you override it.
        """
        super(TestCase, self).setUp()
        self.__mocks = Engine()

    def tearDown(self):
        """
        Do not forget to call the base version if you override it.
        """
        self.__mocks.tear_down()
        super(TestCase, self).tearDown()


class Engine:
    """
    The main class in MockMockMock.
    It acts as a factory for :class:`Mock` instances and
    a link between them (for ordering and verification of expectations).
    """
    def __init__(self):
        self.__handler = ExpectationHandler(OrderedExpectationGroup())
        self.__replacer = Replacer()

    def create(self, name):
        """
        Create a new :class:`Mock`.

        :param str name: The name of the mock to create.
        :return: :class:`Mock`.
        """
        return Mock(name, self.__handler)

    def replace(self, name):  # @todo Add optional param to pass the mock in (to allow replacing several things by same mock)
        """
        @todoc
        """
        mock = self.create(name)
        self.__replacer.replace(name, mock)
        return mock

    def tear_down(self):
        """
        @todoc
        """
        self.__replacer.tear_down()
        self.__handler.tearDown()

    tearDown = tear_down
    """
    Alias for :meth:`tear_down`.
    """

    @property
    def unordered(self):
        """
        @todoc with link to user guide (Expectations grouping)
        """
        return self.__handler.push_group(UnorderedExpectationGroup())

    @property
    def ordered(self):
        """
        @todoc with link to user guide (Expectations grouping)
        """
        return self.__handler.push_group(OrderedExpectationGroup())

    @property
    def atomic(self):
        """
        @todoc with link to user guide (Expectations grouping)
        """
        return self.__handler.push_group(AtomicExpectationGroup())

    @property
    def optional(self):
        """
        @todoc with link to user guide (Expectations grouping)
        """
        return self.__handler.push_group(OptionalExpectationGroup())

    @property
    def alternative(self):
        """
        @todoc with link to user guide (Expectations grouping)
        """
        return self.__handler.push_group(AlternativeExpectationGroup())

    @property
    def repeated(self):
        """
        @todoc with link to user guide (Expectations grouping)
        """
        return self.__handler.push_group(RepeatedExpectationGroup())

    @property
    def records(self):
        """
        @todoc with link to user guide (Recording)
        """
        return self.__handler.get_recorded_calls()


class Mock(object):
    """
    Mock()

    @todoc
    
    See :class:`Engine` for creating instances of this class.
    """
    def __init__(self, name, handler):
        self.__name = name
        self.__handler = handler

    @property
    def expect(self):
        """
        @todoc
        """
        return self.__handler.expect(self.__name)

    @property
    def object(self):
        """
        @todoc
        """
        return self.__handler.object(self.__name)

    def record(self, real_object):
        """
        @todoc
        """
        # @todo In record mode, catch exceptions. Funny: there is not always a "return" key in get_recorded_calls
        return self.__handler.record(self.__name, real_object)
