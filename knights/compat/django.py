from django.core.urlresolvers import reverse
from django.utils import timezone
from django.utils.encoding import iri_to_uri

from knights.library import Library

register = Library()


@register.helper
def now(fmt: str) -> str:
    return timezone.now().strftime(fmt)


@register.helper
def url(name: str, *args: list, **kwargs: dict) -> str | None:
    try:
        return reverse(name, args=args, kwargs=kwargs)
    except:  # noqa: E722
        return None


@register.helper
def static(filename: str) -> str:
    try:
        from django.conf import settings  # noqa: PLC0415
    except ImportError:
        prefix = ''
    else:
        prefix = iri_to_uri(getattr(settings, filename, ''))
    return prefix
