import inspect
import dotmap

class DIError(Exception):
    pass

class Container (object):

    __dependencies = {}
    __container = {}

    def register(self, dependency, name):
        self.__dependencies[name] = dependency
        return self

    def registerFactory(self, dependency, name):
        dependency.__ditype__ = 'factory'
        self.register(dependency, name)

    def get(self, name):
        if name in self.__container:
            return self.__container[name]

        dependency = self.__getDependencyByName(name)
        classDependency = self.__getClassDependency(dependency)

        self.__container[name] = classDependency
        return self.__container[name]

    def getImplementation(self, parent, name):
        return self.get(parent + '-' + name)

    def __getDependencyByName(self, name):
        try:
            return self.__dependencies[name]
        except:
            raise DIError('Can not find the service ' + name)

    def __getClassDependency(self, dependency):
        args = []
        if inspect.isfunction(dependency):
            if hasattr(dependency, '__ditype__') and dependency.__ditype__ == 'factory':
                args.append(self)
            else:
                for arg in inspect.getargspec(dependency)[0]:
                    args.append(self.get(arg))
            return dotmap.DotMap(dependency(*args))

        if inspect.isfunction(dependency.__init__) or inspect.ismethod(dependency.__init__):
            if hasattr(dependency, '__ditype__') and dependency.__ditype__ == 'factory':
                args.append(self)
            else:
                for arg in inspect.getargspec(dependency.__init__)[0]:
                    if arg != "self":
                        args.append(self.get(arg))
        return dependency(*args)


