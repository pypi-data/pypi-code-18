from django import template

from django.utils.encoding import smart_text
from django.contrib.staticfiles import finders
from django.contrib.staticfiles.storage import staticfiles_storage
from django.conf import settings

from django_mailcss import conf

register = template.Library()


class MailCssNode(template.Node):
    def __init__(self, nodelist, filter_expressions):
        self.nodelist = nodelist
        self.filter_expressions = filter_expressions

    def render(self, context):
        rendered_contents = self.nodelist.render(context)
        css = ''
        for expression in self.filter_expressions:
            path = expression.resolve(context, True)
            if path is not None:
                path = smart_text(path)

            css_loader = conf.get_css_loader()()
            css = ''.join((css, css_loader.load(path)))

        engine = conf.get_engine()(html=rendered_contents, css=css)
        return engine.render()


@register.tag
def mailcss(parser, token):
    nodelist = parser.parse(('endmailcss',))

    # prevent second parsing of endmailcss
    parser.delete_first_token()

    args = token.split_contents()[1:]

    return MailCssNode(
        nodelist,
        [parser.compile_filter(arg) for arg in args])
