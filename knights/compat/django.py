
from django.core.urlresolvers import reverse
from django.utils import timezone
from django.utils.encoding import iri_to_uri

from knights.library import Library

register = Library()


@register.helper
def now(fmt):
    return timezone.now().strftime(fmt)


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
        prefix = iri_to_uri(getattr(settings, filename, ''))
    return prefix
