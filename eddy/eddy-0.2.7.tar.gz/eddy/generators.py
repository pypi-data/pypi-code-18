from typing import Dict, Any, List
import os

import jinja2
from jinja2 import Environment, FileSystemLoader, select_autoescape

def jinja_functions(user_functions : Dict[str, Any], env, writer) -> Dict[str, Any]:
    def get_style(style : str) -> str :
        return os.path.join(os.path.abspath(env['URL']), "styles", style, "main.css")

    def get_colorscheme(colorscheme : str) -> str:
        return os.path.join(os.path.abspath(env['URL']), "styles",  "colorschemes" ,  colorscheme)

    helpers = {
        'get_style' : get_style,
        'get_colorscheme' : get_colorscheme,
    }

    return {**user_functions, **helpers}


class Generator():
    def __init__(self, logger, writer):
        logger.debug("Inititalizad generator")
        self.logger = logger
        self.writer = writer
        self.pages : List[dict]= []
        self.jinja_env = Environment(
            loader=FileSystemLoader(writer.templates))

    def get_context(self, file_data : Dict[str, Any]) -> None:
        self.pages.append(file_data)

    def generate(self) -> None:
        self.pages = self.generate_links(self.pages)
        for page in self.pages:
            jinja_helpers = jinja_functions(page['JINJA_FUNCTIONS'], page, self.writer)
            self.jinja_env.globals.update(jinja_helpers)
            template = self.jinja_env.get_template(os.path.join(page['SITE_TEMPLATE'], page['TEMPLATE'] + ".html"))
            output = template.render(page)
            self.writer.write(page['PATH'], output)
            self.writer.make_public(
                [(os.path.join(self.writer.style(page['STYLE'])),
                  self.writer.public_style(page['STYLE'])),
                 (os.path.join(self.writer.style("colorschemes")),
                  self.writer.public_style("colorschemes")),
                ])


    def generate_links(self, data):
        filelinks = [page['URL'] + os.path.basename(self.writer.public_link(page['PATH'])) for page in data if not 'index' in page['PATH']]
        filenames = [os.path.splitext(os.path.basename(filename))[0] for filename in filelinks]
        pages = [{**d, "links": filelinks, "names": filenames} for d in data]

        return pages
