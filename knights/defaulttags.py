from .library import Library
from .parse import BasicNode

import datetime

register = Library()


@register.tag(name='now')
class NowNode(BasicNode):
    def render(self, fmt):
        val = datetime.datetime.now()
        return val.strftime(fmt)
