from demands.pagination import PaginatedResults
from six import iteritems

from yolapy.services import Yola


class SiteImport(object):
    """Represents a SiteImport resource from the Yola API"""

    def __init__(self, **kwargs):
        for key, val in iteritems(kwargs):
            setattr(self, key, val)

    @classmethod
    def create(cls, url, user_id):
        """Create a SiteImport with the Yola API"""
        return cls(**Yola().create_site_import(url, user_id))

    @classmethod
    def get(cls, id):
        """Get a SiteImport from the Yola API"""
        return cls(**Yola().get_site_import(id))

    @classmethod
    def list(cls, **filters):
        """Get a list of SiteImports from the Yola API"""
        site_imports = PaginatedResults(
            Yola().list_site_imports, kwargs=filters)
        return [cls(**site_import) for site_import in site_imports]
