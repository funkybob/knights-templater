from .library import Library
from .parse import BasicNode

import datetime

register = Library()

# autoescape
# block
# comment
# csrf_token
# cycle
# debug
# extends
# filter
# firstof
# for

@register.tag(name='for')
class ForNode(BasicNode):
    def __init__(self, parser, token):
        super().__init__(parser, token)
        self.nodelist = nodelist = []
        # Collect nodes until we find a endfor
        for node in parser.parse_node():
            if isinstance(node, EndForNode):
                break
            self.nodelist.append(node)

    def __call__(self, context):
        args = [arg.id for arg in self.args]
        kwargs = self.resolve_keywords(context)

        source = kwargs['_in']
        content = []
        for item in iter(source):
            # Update the context
            if args:
                ctx = dict(context, zip(args, item))
            else:
                ctx = dict(context, item=item)
            # Render nodelist
            content.extend(x(ctx) for x in self.nodelist)

        return ''.join(content)

@register.tag(name='endfor')
class EndForNode(BasicNode):
    pass

# for ... empty
# if
# ifchanged
# ifequal
# ifnotequal
# include
# load
# now

@register.tag(name='now')
class NowNode(BasicNode):
    def render(self, fmt):
        val = datetime.datetime.now()
        return val.strftime(fmt)

# regroup
# spaceless
# ssi
# templatetag
# url
# verbatim
# widthratio
# with
