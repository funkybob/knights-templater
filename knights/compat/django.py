import ast

from django.core.urlresolvers import reverse
from django.utils.encoding import iri_to_uri

import datetime

from knights.library import Library

register = Library()


@register.helper
def now(fmt):
    return datetime.datetime.now().strftime(fmt)


@register.helper
def url(name, *args, **kwargs):
    try:
        return reverse(name, args=args, kwargs=kwargs)
    except:
        return None


@register.helper
def static(filename):
    try:
        from django.conf import settings
    except ImportError:
        prefix = ''
    else:
        prefix = iri_to_uri(getattr(settings, name, ''))
    return prefix
