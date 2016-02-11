import os

from django.template import Library


register = Library()


@register.filter
def environ(key):
    value = os.environ.get(key)
    if value is None:
        raise ValueError('Environment Variable Not Found: {0}'.format(key))
    return value
