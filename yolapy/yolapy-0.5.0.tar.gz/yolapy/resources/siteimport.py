class SiteImportResourceMixin(object):
    """Yola API methods for SiteImports"""

    _path = '/pr/jobs/sites/'

    def create_site_import(self, **data):
        """Create a SiteImport"""
        return self.post(
            self._path, json=data).json()

    def get_site_import(self, id):
        """Return data for a specific SiteImport"""
        return self.get('{url}{id}/'.format(url=self._path, id=id)).json()

    def list_site_imports(self, **options):
        """Return a paginated list of SiteImports"""
        return self.get(self._path, params=options).json()
