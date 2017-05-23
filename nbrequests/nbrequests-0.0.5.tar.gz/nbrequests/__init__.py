from __future__ import print_function
from uuid import uuid4

from IPython.display import display_html, display_javascript
from jinja2 import Environment, PackageLoader


__all__ = ['display_request']


templates = Environment(
    loader=PackageLoader('nbrequests', 'templates')
)


def display_request(r):
    rq_id = str(uuid4())
    rs_id = str(uuid4())
    html = templates.get_template('requests.html')
    display_html(html.render(r=r, rq_id=rq_id, rs_id=rs_id), raw=True)
    js_template = templates.get_template('requests.js')
    display_javascript(
            js_template.render(r=r, rq_id=rq_id, rs_id=rs_id),
            raw=True)
