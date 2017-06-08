import os
import sys
import json
from py_mini_racer import py_mini_racer

class Fusor(object):
    """An object for rendering React code into an html string with the following propertie(s):

    Attributes:
        ctx: A MiniRacer object for evaluating javascript code.
    """
    def __init__(self):
        """Return a Fusor object with a MiniRacer context."""
        path_to_react = os.path.join(os.path.dirname(__file__), './js/react.min.js')
        path_to_react_dom = os.path.join(os.path.dirname(__file__), './js/react-dom.min.js')
        path_to_react_dom_server = os.path.join(os.path.dirname(__file__), './js/react-dom-server.min.js')
         
        # Initialize V8 instance
        self.ctx = py_mini_racer.MiniRacer()
        
        # Read and evaluate React source code
        with open(path_to_react, "r") as react_file, \
            open(path_to_react_dom, "r") as react_dom_file, \
            open(path_to_react_dom_server, "r") as react_dom_server_file: 
            self.ctx.eval(react_file.read())
            self.ctx.eval(react_dom_file.read())
            self.ctx.eval(react_dom_server_file.read())



    def fuse(self, name, component, props=None, children=None, static=False):
        """Returns an html string of the evaluated string of React component (component)."""
        jsProps = json.dumps(props)
        jsChildren = json.dumps(children)
        react_code = f"(() => {{ {component} ; return React.createElement({name}, {jsProps}, {jsChildren}); }})()" 
        if static:
            return self.ctx.eval(f"ReactDOMServer.renderToStaticMarkup({react_code})")
        else:
            return self.ctx.eval(f"ReactDOMServer.renderToString({react_code})")
