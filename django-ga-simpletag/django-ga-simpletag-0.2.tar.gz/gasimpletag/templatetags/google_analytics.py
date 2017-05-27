from django import template
from django.conf import settings


register = template.Library()

SCRIPT_CODE = """
<script>
  (function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){
  (i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),
  m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)
  })(window,document,'script','https://www.google-analytics.com/analytics.js','ga');

  ga('create', '%(property_id)s', 'auto');
  ga('send', 'pageview');
</script>
"""


@register.tag
def ga_js(parser, token):
    try:
        tag_name, property_id = token.split_contents()
        print(property_id)
    except ValueError:
        raise template.TemplateSyntaxError(
            "%r tag requires exactly 1 arguments" % token.contents.split()[0]
        )
    return GoogleAnalyticsNode(property_id)
    # if not settings.DEBUG:
    #     c = {
    #         'id': property_id
    #     }
    #     js = template.loader.get_template("ga.js")
    #     return js.render(c)
    # else:
    #     return ""


class GoogleAnalyticsNode(template.Node):
    def __init__(self, property_id):
        self.property_id = template.Variable(property_id)

    def render(self, context):
        code = SCRIPT_CODE % {'property_id': self.property_id.resolve(context)}
        if not settings.DEBUG:
            return code
        else:
            return ''
