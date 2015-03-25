from .library import Library

import datetime

register = Library()


@register.tag(name='now')
def now(parser, token):

    args, kwargs = parser.parse_args(token)

    def _now(context):
        a, k = parser.resolve_args(context, args, kwargs)
        val = datetime.datetime.now()
        return val.strftime(a[0])

    return _now
