from collections import defaultdict

from django.template.backends.base import BaseEngine
from django.template.backends.utils import csrf_input_lazy, csrf_token_lazy
from django.template.base import (TemplateDoesNotExist,  # NOQA
                                  TemplateSyntaxError)

from .compiler import kompile
from .loader import TemplateLoader, TemplateNotFound


class KnightsTemplater(BaseEngine):

    def __init__(self, params):
        params = params.copy()

        super(KnightsTemplater, self).__init__(params)

        self.loader = TemplateLoader(self.template_dirs)

    def from_string(self, template_code):
        tmpl = kompile(template_code, loader=self.loader)
        return Template(tmpl)

    def get_template(self, template_name):
        try:
            tmpl = self.loader[template_name]
        except TemplateNotFound:
            raise TemplateDoesNotExist(template_name)
        except Exception as e:
            raise TemplateSyntaxError(e).with_traceback(e.__traceback__)
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
