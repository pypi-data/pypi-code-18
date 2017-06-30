# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os
import re
import logging

from grymp.processors import processor

logger = logging.getLogger(__name__)


class Feature(processor.Processor):
    """
    Handles the processing of a release's feature.
    """

    # possible extensions of the feature, searched in order
    _EXTENSIONS = ['mkv', 'MKV']

    @staticmethod
    def translate_name(name):
        """
        Guess the feature name from the file name.

        :param name: The feature file name.
        :return: Our best guess at the original name.
        """

        _SUBSTITUTIONS = {
            'Dont': 'Don\'t'
        }

        result = re.match(r'(.+?)\.\d{4}\.', name)
        if not result:
            raise ValueError('Unable to identify any name')

        title = result.group(1)
        title = title.replace('-', ' - ')
        title = title.replace('.', ' ')
        terms = title.split(' ')
        terms = [_SUBSTITUTIONS[term] if term in _SUBSTITUTIONS else term
                 for term in terms]
        return ' '.join(terms)

    def process(self, base, name, feature_dir):
        """
        Process the feature in the release directory.

        :param base: The release directory, containing the feature.
        :param name: The name of the feature.
        :param feature_dir: The directory to move the feature to.
        :return: True if the feature was transferred successfully; False if the
                 user cancelled a prompt.
        :raises IOError: If there the feature could not be found.
        """
        for extension in self._EXTENSIONS:
            try:
                path = self._find_file_by_extension(base, extension)
                logger.debug('Located feature at %s', path)
                return self._fs.transfer(
                    path,
                    os.path.join(feature_dir, name + '.' + self._EXTENSIONS[0]))
            except IOError:
                continue

        raise IOError('Failed to identify feature in {0}'.format(base))
