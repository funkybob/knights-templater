from __future__ import unicode_literals

import ast

from .context import ContextScope
from .parser import Parser
from .utils import Helpers


def kompile(src, raw=False, filename='<compiler>'):
    '''
    Creates a new class based on the supplied template, and returnsit.

    class Template(object):
        def __call__(self, context):
            return ''.join(self._iterator(context))

        def _iterator(self, context):
            return map(str, self._root(context)

        def _root(self, context):
            yield ''
            yield ...
            yield from self.head(context)

    Blocks create new methods, and add a 'yield from self.{block}(context)' to
    the current function

    '''

    parser = Parser(src)
    parser.load_library('knights.tags')
    parser.load_library('knights.helpers')

    parser.build_method('_root')

    if parser.parent:
        # Remove _root from the method list
        parser.methods = [
            method for method in parser.methods if method.name != '_root'
        ]

    klass = parser.build_class()

    # Wrap it in a module
    inst = ast.Module(body=[klass])

    ast.fix_missing_locations(inst)

    # Compile code to create class
    code = compile(inst, filename=filename, mode='exec', optimize=2)

    # Execute it and return the instance
    g = {
        '_': Helpers(parser.helpers),
        'parent': parser.parent,
        'ContextScope': ContextScope,
    }
    eval(code, g)

    klass = g['Template']
    if raw:
        return klass
    return klass()
