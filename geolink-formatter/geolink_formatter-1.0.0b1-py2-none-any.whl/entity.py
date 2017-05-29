# -*- coding: utf-8 -*-
import datetime


class Msg(object):

    invalid_argument = 'Invalid argument "{arg}": expected "{expected}", got "{got}"'
    """str: Message for invalid argument type."""


class Document(object):
    def __init__(self, id, title, category, doctype, files, enactment_date=None, federal_level=None,
                 authority=None, authority_url=None, type=None, subtype=None, cycle=None, decree_date=None):
        """Creates a new document instance.

        Args:
            id (str): The document identifier.
            title (str): The document title.
            category (str): The document category.
            doctype (str): The internal type of the document.
            files (list[geolink_formatter.entity.File]): The files contained by the document.
            enactment_date (datetime.date): The date of enactment.
            federal_level (str): The federal level of the document.
            authority (str): The name of the authority responsible for the document.
            authority_url (str): The URL of the authority's website.
            type (str): The official type of the document.
            subtype (str): The subtype of the document.
            cycle (str): The document cycle.
            decree_date (datetime.date): The date of decree.

        Raises:
            TypeError: Raised on missing argument or invalid argument type.
            ValueError: Raised on invalid argument value.

        """

        if not isinstance(files, list):
            raise TypeError(Msg.invalid_argument.format(
                arg='files',
                expected=list,
                got=files.__class__
            ))

        if len(files) < 1:
            raise ValueError('Argument "files" has to contain at least one element')

        if not isinstance(enactment_date, datetime.date):
            raise TypeError(Msg.invalid_argument.format(
                arg='enactment_date',
                expected=datetime.date,
                got=enactment_date.__class__
            ))

        if decree_date and not isinstance(decree_date, datetime.date):
            raise TypeError(Msg.invalid_argument.format(
                arg='decree_date',
                expected=datetime.date,
                got=decree_date.__class__
            ))

        self.__id__ = id
        self.__title__ = title
        self.__category__ = category
        self.__doctype__ = doctype
        self.__files__ = files
        self.__enactment_date__ = enactment_date
        self.__federal_level__ = federal_level
        self.__authority__ = authority
        self.__authority_url__ = authority_url
        self.__type__ = type
        self.__subtype__ = subtype
        self.__cycle__ = cycle
        self.__decree_date__ = decree_date

    @property
    def id(self):
        """str: The document identifier."""
        return self.__id__

    @property
    def title(self):
        """str: The document title."""
        return self.__title__

    @property
    def category(self):
        """str: The document category."""
        return self.__category__

    @property
    def doctype(self):
        """str: The internal type of the document."""
        return self.__doctype__

    @property
    def files(self):
        """list[geolink_formatter.entity.File]: The files contained by the document."""
        return self.__files__

    @property
    def enactment_date(self):
        """datetime.date: The date of enactment."""
        return self.__enactment_date__

    @property
    def federal_level(self):
        """str: The federal level of the document."""
        return self.__federal_level__

    @property
    def authority(self):
        """str: The name of the authority responsible for the document."""
        return self.__authority__

    @property
    def authority_url(self):
        """str: The URL of the authority's website."""
        return self.__authority_url__

    @property
    def type(self):
        """str: The official type of the document."""
        return self.__type__

    @property
    def subtype(self):
        """str: The subtype of the document."""
        return self.__subtype__

    @property
    def cycle(self):
        """str: The document cycle."""
        return self.__cycle__

    @property
    def decree_date(self):
        """str: The date of decree."""
        return self.__decree_date__


class File(object):
    def __init__(self, title, href, category):
        """Creates a new file instance.

        Args:
            title (str): The file's title.
            href (str): The URL to access the file.
            category (str): The file's category.

        """

        self.__title__ = title
        self.__href__ = href
        self.__category__ = category

    @property
    def title(self):
        """str: The file's title."""
        return self.__title__

    @property
    def href(self):
        """str: The URL to access the file."""
        return self.__href__

    @property
    def category(self):
        """str: The file's category."""
        return self.__category__
