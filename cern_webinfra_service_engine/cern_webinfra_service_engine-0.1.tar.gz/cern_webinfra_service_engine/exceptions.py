class MethodNotAllowed(Exception):
    def __init__(self, method):
        self.method = method

    def __str__(self):
        return "no request  handler for the method: " \
               "%s" % self.method


class RouteNotSpecified(Exception):
    def __init__(self, route):
        self.route = route

    def __str__(self):
        return "no request   handler for the path: " "%s " \
               "check your endpoint class implementation" \
               % self.route