from django import template


register = template.Library()

@register.simple_tag(takes_context=True)
def page_url(context, page):
    request = context['request']
    args = {}
    for key, value in request.GET.items():
        args[key] = value[0] if isinstance(value, (list, tuple)) else value
    args['page'] = page
    return '?' + '&'.join('{0}={1}'.format(key, value) for key, value in args.items())
