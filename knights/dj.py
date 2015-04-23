from collections import defaultdict

from django.template import TemplateDoesNotExist, TemplateSyntaxError  # NOQA
from django.template.backends.base import BaseEngine
from django.template.backends.utils import csrf_input_lazy, csrf_token_lazy

from . import compiler
from . import loader


class KnightsTemplater(BaseEngine):

    def __init__(self, params):
        params = params.copy()
        options = params.pop('OPTIONS').copy()

        super(KnightsTemplater, self).__init__(params)

    def from_string(self, template_code):
        tmpl = compiler.kompile(template_code)
        return Template(tmpl)

    def get_template(self, template_name):
        try:
            tmpl = loader.load_template(template_name, self.template_dirs)
        except Exception as e:
            raise TemplateSyntaxError(e).with_traceback(e.__traceback__)
        if tmpl is None:
            raise TemplateDoesNotExist(template_name)
        return Template(tmpl)


class Template(object):

    def __init__(self, template):
        self.template = template

    def render(self, context=None, request=None):
        if context is None:
            context = {}
        if request is not None:
            context['user'] = request.user
            context['request'] = request
            context['csrf_input'] = csrf_input_lazy(request)
            context['csrf_token'] = csrf_token_lazy(request)
        ctx = defaultdict(str)
        ctx.update(context)
        return self.template(ctx)
