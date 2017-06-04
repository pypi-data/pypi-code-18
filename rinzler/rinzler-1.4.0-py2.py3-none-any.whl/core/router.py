import json
from django.http import HttpResponse
from django.http.request import HttpRequest
from django.views.generic import TemplateView
from rinzler.core.route_mapping import RouteMapping
from django.views.decorators.csrf import csrf_exempt


class Router(TemplateView):
    __request = None
    __callable = None
    __app = dict()
    __route = None
    __uri = None
    __method = None
    __bound_routes = dict()

    def __init__(self, route, controller):
        self.__route = route
        self.__callable = controller
        self.__app = RouteMapping()

    @csrf_exempt
    def route(self, request: HttpRequest):
        self.__request = request
        self.__uri = request.path[1:]
        self.__method = request.method

        routes = self.__callable().connect(self.__app)

        self.__bound_routes = routes.get__routes()

        end_point = self.get_end_point_uri()
        acutal_params = self.get_url_params(end_point)

        return self.exec_route_callback(acutal_params)

    def exec_route_callback(self, actual_params):

        if self.__method.lower() in self.__bound_routes:
            for bound in self.__bound_routes[self.__method.lower()]:

                route = list(bound)[0]
                expected_params = self.get_url_params(route)

                if len(actual_params) == len(expected_params):
                    pattern_params = self.get_callback_pattern(expected_params, actual_params)
                    return bound[route](self.__request, **pattern_params)

        return self.no_route_found(self.__request)

    @staticmethod
    def get_callback_pattern(expected_params, actual_params):
        pattern = dict()
        key = 0
        for exp_param in expected_params:
            if exp_param[0] == '{' and exp_param[-1:] == '}':
                pattern[exp_param[1:-1]] = actual_params[key]
            key = key + 1
        return pattern

    @staticmethod
    def get_url_params(end_point):
        var_params = end_point.split('/')

        if len(var_params) == 1 and var_params[0] == '':
            return []

        elif len(var_params) == 1 and var_params[0] != '':
            return [var_params[0]]
        else:
            params = list()
            for param in var_params:
                if len(param) > 0:
                    params.append(param)
            return params

    def get_end_point_uri(self):
        uri_prefix = len(self.__route)
        return self.__uri[uri_prefix:]

    @csrf_exempt
    def no_route_found(self, request):
        response = {
            "status": False,
            "exceptions": {
                "message": "No route found for {0} {1}".format(self.__method, self.__route),
            },
            "request": {
                "method": self.__method,
                "path_info": self.__uri,
                "content": request.body.decode("utf-8")
            },
            "message": "We are sorry, but something went terribly wrong."
        }
        return HttpResponse("{0}".format(json.dumps(response)), content_type="application/json", status=404)
