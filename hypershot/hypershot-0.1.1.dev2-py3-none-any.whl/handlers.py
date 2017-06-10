""" Hypershot Built-In Handlers for Image Hosters.
"""
import os
import re
import pprint
import collections
from urllib.parse import urlparse

import requests
from addict import Dict as attrdict

from . import config, util

# TODO: https://malzo.com/ (Chevereto, anon)
# TODO: https://picload.org/
# TODO: http://www.casimages.com/
# TODO: Chevereto


class UploadHandlerBase():
    """Base class for image hosting handlers with some common logic."""

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
        if config.debug:
            print("Handler CFG:", self.settings)

        # Validate settings
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

        if config.debug:
            print("Handler CFG (validated):", self.settings)

        # Resolve '.netrc' (AFTER debug logging)
        if self.settings.login == '.netrc':
            import netrc

            service_host = urlparse(self.settings.url).netloc
            known_logins = netrc.netrc()
            account = known_logins.authenticators('hypershot:' + service_host)
            if not account:
                account = known_logins.authenticators(service_host)
            if not all((account, account[0] or account[1])):
                raise ValueError("Account for host {host} not found in ~/.netrc file"
                                 .format(host=service_host))
            self.settings.login = account[0] or account[1]
            self.settings.password = account[2] or ''

        if self.settings.login:
            self.settings.login = self.settings.login.strip()
        if self.settings.password:
            self.settings.password = self.settings.password.strip()

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
        return attrdict(link='') if config.dry_run else None


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

        if config.debug:
            print("imgur upload result:", pprint.pformat(result, indent=4))
        return result


class CheveretoHandler(UploadHandlerBase):
    """Uploading to Chevereto sites."""

    DEFAULTS = dict(
        types={'JPEG', 'PNG'},
    )
    AUTH_RE = r'PF\.obj\.config\.auth_token = "([^"]+)";'

    def __init__(self, settings):
        super().__init__(collections.ChainMap(dict(settings), ImgurHandler.DEFAULTS))

    def upload(self, image):
        """Upload the given image."""
        result = super().upload(image)
        if not result:
            session = requests.session()

            # First get the `auth_token`, then login
            response = session.get(self.settings.url + '/login')
            auth_token = re.search(self.AUTH_RE, response.text).group(1)
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
            files = [('source', (os.path.basename(image), open(image, 'rb')))]

            # Perform upload
            response = session.post(self.settings.url + '/json', data=payload, files=files, headers=headers)
            result = attrdict(response.json())

            if result.status_code != 200:
                message = result.get('error', {}).get('message') or 'UNKNOWN REASON'
                raise RuntimeError('Chevereto upload of "{}" to "{}" failed: {}'.format(
                    image, self.settings.url, message))

            ##result.link = result.image.image.url

        if config.debug:
            print("Chevereto @", self.settings.url, "upload result:", pprint.pformat(result, indent=4))
        return result


REGISTRY = dict(
    imgur=ImgurHandler,
    chevereto=CheveretoHandler,
)
