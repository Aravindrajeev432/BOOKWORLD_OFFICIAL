from atexit import register
import urllib
from django import template
register = template.Library()
@register.simple_tag(takes_context=True)
def url_add_query(context, **kwargs):
    """ Updates the current path from existing GET parameters. """
    request = context.get('request')

    get = request.GET.copy()
    get.update(kwargs)
    return u'{path}?{params}'.format(path=request.path,
                params=urllib.parse.urlencode(get, 'utf-8'))