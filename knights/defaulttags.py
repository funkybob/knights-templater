from .parse import Node
from .library import Library

import datetime

register = Library()


@register.tag(name='now')
def now(token, parser):

    def _now(context):
        # resolve bits
        val = datetime.datetime.now()
        return val.strftime(token[0])

    return _now
