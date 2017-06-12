""".. Ignore pydocstyle D400.

===================
Frontend validators
===================

Following validators are for validating :class:`~django.db.models.ImageField`,
but can also be used with coresponding :class:`form fields
<django.forms.ImageField>`.

To use them, list them in ``validators`` attribute of coresponding field:

.. code-block:: python

    my_field = models.ImageField(validators=[<validator_1>, <validator_2>,...])

.. autofunction:: rolca.frontend.validators.validate_format
.. autofunction:: rolca.frontend.validators.validate_size
.. autofunction:: rolca.frontend.validators.validate_long_edge

"""
import logging

from PIL import Image

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured, ValidationError
from django.utils.translation import ugettext as _


logger = logging.getLogger(__name__)  # pylint: disable=invalid-name


def _humanize_size(nbytes):
    """Transform given number of bytes to human readable unit."""
    suffix = None
    for suffix in ['B', 'KB', 'MB', 'GB']:
        if nbytes < 1024:
            break
        nbytes /= 1024

    humanized = '{:.2f}'.format(nbytes).rstrip('0').rstrip('.')
    return '{} {}'.format(humanized, suffix)


def validate_format(value):
    """Check if file format is among allowed ones in settings.

    List of allowed formats is read from ``ROLCA_ACCEPTED_FORMATS`` setting.
    If the setting is not defined, validation passes.

    :param value: value of the field to be checked
    :type value: ~django.core.files.uploadedfile.UploadedFile

    :raise ValidationError: if image format is not among allowed formats

    :raise ImproperlyConfigured: if ``ROLCA_ACCEPTED_FORMATS`` setting is
        defined but is not a list
    """
    accepted_formats = getattr(settings, 'ROLCA_ACCEPTED_FORMATS', [])

    if not accepted_formats:
        logger.warning('`validate_format` validation cannot be performed, because '
                       '`ROLCA_ACCEPTED_FORMATS` setting is not defined.')
        return

    if not isinstance(accepted_formats, list):
        msg = '`ROLCA_ACCEPTED_FORMATS` setting must be of type `list`.'
        logger.error(msg)
        raise ImproperlyConfigured(msg)

    image = Image.open(value)
    if image.format not in accepted_formats:
        raise ValidationError(_('Only following image types are supported: '
                                '{}').format(', '.join(accepted_formats)))


def validate_size(value):
    """Check if file is smaller then specified in settings.

    Maximum file size is read from ``ROLCA_MAX_SIZE`` setting. If the setting
    is not defined, validation passes.

    :param value: value of the field to be checked
    :type value: ~django.core.files.uploadedfile.UploadedFile

    :raise ValidationError: if image size is greated than one define in
        settings

    :raise ImproperlyConfigured: if ``ROLCA_MAX_SIZE`` setting is
        defined but is not a integer
    """
    max_size = getattr(settings, 'ROLCA_MAX_SIZE', None)

    if not max_size:
        logger.warning('`validate_size` validation cannot be performed, because '
                       '`ROLCA_MAX_SIZE` setting is not defined.')
        return

    if not isinstance(max_size, int):
        msg = '`ROLCA_MAX_SIZE` setting must be of type `int`.'
        logger.error(msg)
        raise ImproperlyConfigured(msg)

    if value.size > max_size:
        raise ValidationError(_('Uploaded file must be smaller than '
                                '{}.').format(_humanize_size(max_size)))


def validate_long_edge(value):
    """Check if the long edge of the image meets requirements.

    Maximum length of the long edge is read from ``ROLCA_MAX_LONG_EDGE``
    setting. If the setting is not defined, validation passes.

    :param value: value of the field to be checked
    :type value: ~django.core.files.uploadedfile.UploadedFile

    :raise ValidationError: if long edge is greated than one define in settings

    :raise ImproperlyConfigured: if ``ROLCA_MAX_LONG_EDGE`` setting is
        defined but is not a integer
    """
    max_long_edge = getattr(settings, 'ROLCA_MAX_LONG_EDGE', None)

    if not max_long_edge:
        logger.warning('`validate_long_edge` validation cannot be performed, '
                       'because `ROLCA_MAX_LONG_EDGE` setting is not defined.')
        return

    if not isinstance(max_long_edge, int):
        msg = '`ROLCA_MAX_LONG_EDGE` setting must be of type `int`.'
        logger.error(msg)
        raise ImproperlyConfigured(msg)

    image = Image.open(value)
    if max(image.size) > max_long_edge:
        raise ValidationError(_('Long edge of the image cannot excede '
                                '{}px.').format(max_long_edge))
