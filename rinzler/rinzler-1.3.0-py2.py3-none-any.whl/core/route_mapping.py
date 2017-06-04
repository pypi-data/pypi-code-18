class RouteMapping(object):

    __routes = dict()

    def get(self, route, callback):
        self.__set_route('get', {route: callback})
        return self

    def post(self, route, callback):
        self.__set_route('post', {route: callback})
        return self

    def put(self, route, callback):
        self.__set_route('get', {route: callback})
        return self

    def delete(self, route, callback):
        self.__set_route('get', {route: callback})
        return self

    def head(self, route, callback):
        self.__set_route('get', {route: callback})
        return self

    def options(self, route, callback):
        self.__set_route('get', {route: callback})
        return self

    def __set_route(self, type_route, route):
        if type in self.__routes:
            self.__routes[type_route].append(route)
        else:
            self.__routes[type_route] = [route]
        return self

    def get__routes(self):
        return self.__routes
