# -*- coding: utf-8 -*-
"""Report related attribute container object definitions."""

from plaso.containers import interface
from plaso.containers import manager
from plaso.lib import timelib


class AnalysisReport(interface.AttributeContainer):
  """Class to represent an analysis report attribute container.

  Attributes:
    filter_string (str): event filter expression.
    plugin_name (str): name of the analysis plugin that generated the report.
    report_array (array[str]): ???
    report_dict (dict[str]): ???
    text (str): report text.
    time_compiled (int): timestamp of the date and time the report was compiled.
  """
  CONTAINER_TYPE = u'analysis_report'

  def __init__(self, plugin_name=None, text=None):
    """Initializes the analysis report.

    Args:
      plugin_name (Optional[str]): name of the analysis plugin that generated
          the report.
      text (Optional[str]): report text.
    """
    super(AnalysisReport, self).__init__()
    self.filter_string = None
    self.plugin_name = plugin_name
    self.report_array = None
    self.report_dict = None
    # TODO: rename text to body?
    self.text = text
    self.time_compiled = None

  def CopyToDict(self):
    """Copies the attribute container to a dictionary.

    Returns:
      dict[str, object]: attribute values per name.
    """
    dictionary = {}
    for attribute_name, attribute_value in self.GetAttributes():
      if attribute_value is None:
        continue

      dictionary[attribute_name] = attribute_value

    return dictionary

  def GetString(self):
    """Retrieves a string representation of the report.

    Returns:
      str: string representation of the report.
    """
    string_list = []
    string_list.append(u'Report generated from: {0:s}'.format(self.plugin_name))

    time_compiled = getattr(self, u'time_compiled', 0)
    if time_compiled:
      time_compiled = timelib.Timestamp.CopyToIsoFormat(time_compiled)
      string_list.append(u'Generated on: {0:s}'.format(time_compiled))

    filter_string = getattr(self, u'filter_string', u'')
    if filter_string:
      string_list.append(u'Filter String: {0:s}'.format(filter_string))

    string_list.append(u'')
    string_list.append(u'Report text:')
    string_list.append(self.text)

    return u'\n'.join(string_list)


manager.AttributeContainersManager.RegisterAttributeContainer(AnalysisReport)
