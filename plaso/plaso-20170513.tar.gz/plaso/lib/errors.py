# -*- coding: utf-8 -*-
"""This file contains the error classes."""

class Error(Exception):
  """Base error class."""


class BadConfigObject(Error):
  """Raised when the configuration object is of the wrong type."""


class BadConfigOption(Error):
  """Raised when a faulty configuration option is encountered."""


class ConnectionError(Error):
  """Class that defines errors encountered connecting to a service."""


class HeapFull(Error):
  """Class that implements a heap full exception."""


class MaximumRecursionDepth(Error):
  """Raised when the maximum recursion depth is reached."""


class NotAText(Error):
  """Raised when trying to read a text on a non-text sample."""


class NoFormatterFound(Error):
  """Raised when no formatter is found for a particular event object."""


class ParseError(Error):
  """Raised when a parse error occurred."""


class PreProcessFail(Error):
  """Raised when a preprocess module is unable to gather information."""


class QueueAlreadyClosed(Error):
  """Raised when an attempt is made to close a queue that is already closed."""


class QueueAlreadyStarted(Error):
  """Raised when an attempt is made to start queue that is already started."""


class QueueClose(Error):
  """Class that implements a queue close exception."""


class QueueEmpty(Error):
  """Class that implements a queue empty exception."""


class QueueFull(Error):
  """Class that implements a queue full exception."""


class SerializationError(Error):
  """Class that defines serialization errors."""


class SourceScannerError(Error):
  """Class that defines source scanner errors."""


class TimestampError(Error):
  """Class that defines timestamp errors."""


class UnableToLoadRegistryHelper(Error):
  """Raised when unable to load a Registry helper object."""


class UnableToParseFile(Error):
  """Raised when a parser is not designed to parse a file."""


class UserAbort(Error):
  """Class that defines an user initiated abort exception."""


class WrongBencodePlugin(Error):
  """Error reporting wrong bencode plugin used."""


class WrongFormatter(Error):
  """Raised when the formatter is not applicable for a particular event."""


class WrongPlistPlugin(Error):
  """Error reporting wrong plist plugin used."""


class WrongPlugin(Error):
  """Raised when the plugin is of the wrong type."""


class WrongQueueType(Error):
  """Raised when an unsupported operation is attempted on a queue.

  For example, attempting to Pop from a Push-only queue.
  """
