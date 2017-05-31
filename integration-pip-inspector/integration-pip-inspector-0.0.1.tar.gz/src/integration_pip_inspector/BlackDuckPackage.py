class BlackDuckPackage(object):

    key = None
    name = None
    version = None
    dependencies = []

    def __init__(self, key, name, version, dependencies):
        self.key = key
        self.name = name
        self.version = version
        self.dependencies = dependencies

    def add_dependency(self, package):
        self.dependencies.append(package)

    def render_id(self):
        id_ = self.name + "==" + self.version
        return id_

    def flatten(self):
        flattened = []
        for pkg in self.dependencies:
            pkg_id = pkg.render_id()
            flattened.append(pkg)
            flattened.extend(pkg.flatten())
        flattened = self._remove_duplicates(flattened)
        return flattened

    def _remove_duplicates(self, packages):
        unique = []
        for package in packages:
            found = False
            for pkg in unique:
                if package.render_id() == pkg.render_id():
                    found = True
                    break
            if not found:
                unique.append(package)
        return unique
