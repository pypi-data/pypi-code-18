from pathlib import Path

from abc import abstractmethod

from peek_plugin_base.PeekPlatformCommonHookABC import PeekPlatformCommonHookABC
from peek_plugin_base.PeekPlatformFrontendHookABC import PeekPlatformFrontendHookABC


class PeekServerPlatformHookABC(PeekPlatformCommonHookABC, PeekPlatformFrontendHookABC):
    @property
    @abstractmethod
    def dbConnectString(self) -> str:
        """ DB Connect String

        :return: The SQLAlchemy database engine connection string/url.

        """

    @property
    @abstractmethod
    def fileStorageDirectory(self) -> Path:
        """ File Storage Directory

        This method returns a Path object providing access to the managed
        file storage location where the plugin can persistently store any files it
        wants to.

        See https://docs.python.org/3/library/pathlib.html#basic-use

        :returns: The plugins managed storage Path object.
        """
