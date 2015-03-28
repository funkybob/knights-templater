import ast

from .library import Library
from .parse import BasicNode, Node

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
            nodelist.append(node)

    def __call__(self, context):
        args = [arg.id for arg in self.args]
        kwargs = self.resolve_keywords(context)

        source = kwargs['_in']
        content = []
        for item in iter(source):
            # Update the context
            ctx = dict(context)
            if args:
                ctx.update(zip(args, item))
            else:
                ctx.update(item=item)
            # Render nodelist
            content.extend(str(x(ctx)) for x in self.nodelist)

        return ''.join(content)


@register.tag(name='endfor')
class EndForNode(Node):
    pass

# for ... empty
# if


@register.tag(name='if')
class IfNode(Node):
    def __init__(self, parser, token):
        super().__init__(parser, token)
        code = ast.parse(token, mode='eval')
        # Apply filter mangling?
        self.condition = compile(code, filename='<if tag>', mode='eval')

        self.true_nodelist = []
        self.false_nodelist = []

        for node in parser.parse_node():
            if isinstance(node, (EndIfNode, ElseNode)):
                break
            self.true_nodelist.append(node)

        if isinstance(node, EndIfNode):
            return

        for node in parser.parse_node():
            if isinstance(node, EndIfNode):
                break
            self.false_nodelist.append(node)

    def __call__(self, context):
        if eval(self.condition, context, {}):
            nodelist = self.true_nodelist
        else:
            nodelist = self.false_nodelist

        return ''.join(str(x(context)) for x in nodelist)


@register.tag(name='endif')
class EndIfNode(Node):
    pass


@register.tag(name='else')
class ElseNode(Node):
    pass

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
