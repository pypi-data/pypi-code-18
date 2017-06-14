""" Hypershot Built-In Handlers for Image Hosters.
"""
import os
import re
import json
import yaml
import textwrap
import collections
from urllib.parse import urlparse

import requests
from addict import Dict as attrdict

from . import config, util

# TODO: https://picload.org/
# TODO: http://www.casimages.com/


def _pure_ascii(text):
    """Replace any non-ASCII values in a string."""
    return text.encode('ascii', errors='replace').decode('ascii').replace('?', '_')


class UploadHandlerBase():
    """Base class for image hosting handlers with some common logic."""
    # None means no interpolation, an empty ``set()`` means no excludes
    INTERPOLATE_EXCLUDES = None

    DEFAULTS = dict(
        limit=0,
        thumb_size=0,
        url='',
        login='',
        password='',
        nsfw=False,
    )
    TYPE_ALIASES=(
        {'JPEG', 'JPG'},
    )
    FAKE_USER_AGENT = (  # a fake user-agent for paranoid sites
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        ' (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
    )

    def __init__(self, settings):
        self.settings = attrdict(collections.ChainMap(
            dict(settings), UploadHandlerBase.DEFAULTS).items())
        self._dump_settings()

        self._validate_settings()
        self._dump_settings('validated')

        if self.INTERPOLATE_EXCLUDES is not None:
            self._interpolate_settings()
            self._dump_settings('interpolated')

    def _dump_settings(self, label=''):
        """Debug output of handler settings."""
        label = ' ({})'.format(label) if label else ''
        data_dump = textwrap.indent(yaml.dump(self.settings.to_dict(), indent=4), '    ')
        if 'password' in self.settings:
            data_dump = data_dump.replace(self.settings.password,
                                          re.sub(r'[^-._]', '?', self.settings.password))
        config.log.debug('%s config%s:\n%s', self.__class__.__name__, label, data_dump)

    def _validate_settings(self):
        """Validate configuration / service settings."""
        self.settings.url = self.settings.url.rstrip('/')
        self.settings.limit = util.bibytes(self.settings.limit)
        self.settings.types = {x.upper() for x in self.settings.types}
        self.settings.thumb_size = self.settings.thumb_size or config.thumb_size

        for boolean in ('nsfw',):
            self.settings[boolean] = util.coerce_to_default_type(
                boolean, self.settings[boolean], False)

        for aliases in self.TYPE_ALIASES:
            if not self.settings.types.isdisjoint(aliases):
                self.settings.types.update(aliases)

        if self.settings.login == '.netrc':
            self._resolve_netrc()

        if self.settings.login:
            self.settings.login = self.settings.login.strip()
        if self.settings.password:
            self.settings.password = self.settings.password.strip()

    def _resolve_netrc(self):
        """Resolve a ``.netrc`` value in ``login``."""
        import netrc

        service_host = urlparse(self.settings.url).netloc
        known_logins = netrc.netrc()
        account = known_logins.authenticators('hypershot:' + service_host)
        if not account:
            account = known_logins.authenticators(service_host)
        if not account or not(account[0] or account[1]):
            raise ValueError("Account for host '{host}' not found in '~/.netrc' file"
                             .format(host=service_host))
        self.settings.login = account[0] or account[1]
        self.settings.password = account[2] or ''

    def _interpolate_settings(self):
        """Interpolate (format) settings values, even nested ones."""
        def interpolate(mapping, namespace):
            'Helper'
            changed = False
            for key, val in mapping.items():
                if key in self.INTERPOLATE_EXCLUDES:
                    continue
                if isinstance(val, dict):
                    interpolate(val, namespace)
                elif isinstance(val, str) and '{' in val:
                    try:
                        val = val.format(**namespace)
                    except (TypeError, ValueError, IndexError, AttributeError) as cause:
                        config.log.warning('Cannot interpolate "{}": {}'.format(val, cause))
                    mapping[key] = val
                    changed = True
            return changed

        for _ in range(25):  # no endless replacement loop
            if not interpolate(self.settings, self.settings):
                break

    def validate(self, image):
        """Perform some checks before uploading."""
        if not os.path.exists(image):
            raise AssertionError('Image file "{}" does not exist!'.format(image))

        if self.settings.limit and os.path.getsize(image) > self.settings.limit:
            raise AssertionError('Image file "{}" is too big ({} > {})!'.format(image,
                util.to_bibytes(os.path.getsize(image)),
                util.to_bibytes(self.settings.limit)))

        _, ext = os.path.splitext(image)
        if ext.lstrip('.').upper() not in self.settings.types:
            raise AssertionError(
                'Image file extension "{}" not supported by "{}", expected one of {}!'
                .format(ext, self.settings.url, ', '.join(sorted(self.settings.types))))

    def upload(self, image):
        """Upload the given image."""
        self.validate(image)
        return attrdict(hypershot=attrdict(link='', thumb='')) if config.dry_run else None

    def post_process(self, image, result):
        """Standard processing after uploading."""
        result.hypershot.image = os.path.abspath(image)
        if 'square' not in result.hypershot:
            result.hypershot.square = None

        # TODO: Add our own thumbnail on demand

        metadata = json.dumps(result, indent=4, sort_keys=True)
        config.log.debug('%s @ "%s" upload result:\n%s',
                         self.__class__.__name__, self.settings.url, metadata)

        if not config.dry_run and config.json_files:
            with open(os.path.splitext(image)[0] + '.json', 'w') as json_handle:
                json_handle.write(metadata + '\n')

        return result


class FileUploadHandler(UploadHandlerBase):
    """ Uploading to any simple host accepting file-upload POSTs,
        and returning TEXT or HTML with an embedded image link,
        or JSON with attributes allowing to construct such a link.
    """
    INTERPOLATE_EXCLUDES = {'image_url'}

    def upload(self, image):
        """Upload the given image."""
        result = super().upload(image)
        if not result:
            session = requests.session()

            # Prepare upload
            headers = {'User-Agent': self.FAKE_USER_AGENT}
            headers.update(self.settings.get('headers', {}))
            files = [(self.settings.files_field_name,
                      (_pure_ascii(os.path.basename(image)), open(image, 'rb'))
                    )]

            # Perform upload
            response = session.post(self.settings.upload_url,
                                    data=self.settings.get('data'), files=files, headers=headers)
            response_type = response.headers.get('content-type', 'application/octet-stream')
            response_type = response_type.split(';')[0]
            config.log.debug("File upload response: HTTP %d %r\n    %r%s\n    [%d bytes, %s, charset=%s]",
                             response.status_code, response.reason,
                             response.text if config.debug else response.text[:100],
                             '...' if len(response.text) > 99 else '',
                             len(response.text), response_type, response.encoding)

            # Check response
            if response.status_code != requests.codes.ok:
                message = response.reason or 'UNKNOWN REASON'
                raise RuntimeError('File upload of "{path}" to "{url}" failed: HTTP {code} {msg}'.format(
                    path=image, url=self.settings.url, code=response.status_code, msg=message))

            # Build result from settings and response data
            namespace = self.settings.to_dict()
            if response_type == 'application/json':
                response_key = 'json'
                namespace[response_key] = response.json()
            elif response_type in {'text/plain', 'text/html'}:
                response_key = 'text'
                namespace[response_key] = response.text
                if 'response_regex' in self.settings:
                    match = re.search(self.settings.response_regex, response.text)
                    if not match:
                        raise RuntimeError('Cannot find regex {regex!r} in response from "{url}"'.format(
                                           url=self.settings.url,
                                           regex=self.settings.response_regex))
                    response_key = 'response'
                    namespace[response_key] = match.groupdict()
            else:
                raise RuntimeError('Unknown response type "{ctype}" while uploading "{path}" to "{url}"'
                                   .format(path=image, url=self.settings.url, ctype=response_type))
            result = attrdict((response_key, namespace[response_key]))
            result.hypershot.link = self.settings.image_url.format(**namespace)

        return self.post_process(image, result)


class ImgurHandler(UploadHandlerBase):
    """ Uploading to ``imgur.com``.

        The ``login`` is the client ID, the ``password`` is the client secret.
    """

    DEFAULTS = dict(
        url='https://api.imgur.com/',
        limit='10M',
        types={'JPEG', 'PNG', 'GIF', 'APNG', 'TIFF', 'PDF', 'XCF'},
    )

    def __init__(self, settings):
        super().__init__(collections.ChainMap(dict(settings), ImgurHandler.DEFAULTS))

        assert self.settings.login and self.settings.login != '.netrc', "Missing imgur client ID!"
        assert self.settings.password, "Missing imgur client secret!"

    def upload(self, image):
        """Upload the given image."""
        from imgurpython import ImgurClient
        from imgurpython.helpers.error import ImgurClientError

        result = super().upload(image)
        if not result:
            client = ImgurClient(self.settings.login, self.settings.password)
            result = attrdict(client.upload_from_path(image))
            result.hypershot.link = result.link
            result.hypershot.thumb = "{0}l.{1}".format(*result.link.rsplit('.', 1))
            result.hypershot.square = "{0}s.{1}".format(*result.link.rsplit('.', 1))

        return self.post_process(image, result)


class CheveretoHandler(UploadHandlerBase):
    """Uploading to Chevereto sites."""

    DEFAULTS = dict(
        types=['JPEG', 'PNG', 'BMP', 'GIF'],
        nsfw=False,
    )
    AUTH_RE = r'PF\.obj\.config\.auth_token *= *"([^"]+)";'

    def __init__(self, settings):
        super().__init__(collections.ChainMap(dict(settings), ImgurHandler.DEFAULTS))

    def upload(self, image):
        """Upload the given image."""
        result = super().upload(image)
        if not result:
            session = requests.session()

            # First get the `auth_token`, then login
            auth_url = self.settings.url + ('/login' if self.settings.login else '/')
            response = session.get(auth_url)
            auth_match = re.search(self.AUTH_RE, response.text)
            if not auth_match:
                raise RuntimeError("Cannot find auth token @ {}".format(auth_url))
            auth_token = auth_match.group(1)
            if self.settings.login:
                session.post(self.settings.url + '/login', data={
                    'auth_token': auth_token,
                    'login-subject': self.settings.login,
                    'password': self.settings.password,
                })

            # Prepare upload
            headers = {'User-Agent': self.FAKE_USER_AGENT}
            payload = dict(
                type='file',
                action='upload',
                privacy='public',
                auth_token=auth_token,
                category_id=None,
                nsfw=self.settings.nsfw,
            )
            files = [('source', (_pure_ascii(os.path.basename(image)), open(image, 'rb')))]

            # Perform upload
            response = session.post(self.settings.url + '/json', data=payload, files=files, headers=headers)
            result = attrdict(response.json())

            if response.status_code != requests.codes.ok:
                message = result.get('error', {}).get('message') or 'UNKNOWN REASON'
                raise RuntimeError('Chevereto upload of "{path}" to "{url}" failed: {msg}'.format(
                    path=image, url=self.settings.url, msg=message))

            result.hypershot.link = result.image.image.url
            result.hypershot.thumb = result.image.thumb.url

        return self.post_process(image, result)


REGISTRY = dict(
    file_upload=FileUploadHandler,
    imgur=ImgurHandler,
    chevereto=CheveretoHandler,
)
