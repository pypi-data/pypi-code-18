from coreapi import Link as BaseLink


class Link(BaseLink):

    def __init__(self, url=None, action=None, encoding=None,
                 transform=None, title=None, description=None, fields=None,
                 authentication=None, formats=None):
        super().__init__(url, action, encoding, transform, title, description,
                         fields)
        if (authentication is not None) and (not isinstance(authentication,
                                                            bool)):
            raise TypeError("Argument 'authentication' must be a boolean.")
        if (formats is not None) and (not isinstance(formats, (list, tuple))):
            raise TypeError("Argument 'formats' must be a list.")

        self._authentication = (False if (authentication is None) else
                             authentication)
        self._formats = () if (formats is None) else formats


    @classmethod
    def from_base_link(cls, link, authentication, formats):
        instance = cls(link.url, link.action, link.encoding, link.transform,
                       link.title, link.description, link.fields,
                       authentication, formats)
        del link
        return instance

    @property
    def authentication(self):
        return self._authentication

    @property
    def formats(self):
        return self._formats
