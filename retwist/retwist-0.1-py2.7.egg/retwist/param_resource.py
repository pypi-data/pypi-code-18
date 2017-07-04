import inspect

import twisted.web.resource

import retwist.param


class ParamResource(twisted.web.resource.Resource):
    """
    Twisted resource with convenient parsing of parameters.
    
    Parameters are defined at class level:
    
    age = retwist.Param()
    
    By the time your render_* method gets passed a request object, look for the parsed parameters in request.url_args.
    """

    def render(self, request):
        """
        Before we render this request as normal, parse parameters, and add them to the request!
        :param request: Twisted request object
        :return: Byte string or NOT_DONE_YET - see IResource.render
        """
        request.url_args = self.parse_args(request)
        return twisted.web.resource.Resource.render(self, request)

    def parse_args(self, request):
        """
        Parse arguments from request. Throws twisted.web.error.Error instances on client errors.
        
        :param request: Twisted request 
        :return: Dictionary of parameter names to parsed values
        """
        return {
            name: param.parse_from_request(name, request)
            for name, param in inspect.getmembers(self)
            if isinstance(param, retwist.Param)
        }