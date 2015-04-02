'''
Default helper functions
'''
from contextlib import contextmanager
from functools import wraps

from .library import Library

register = Library()


def stringfilter(func):
    """
    Decorator for filters which should only receive unicode objects. The object
    passed as the first positional argument will be converted to a unicode
    object.
    """
    @wraps(func)
    def _dec(*args, **kwargs):
        if args:
            args = list(args)
            args[0] = str(args[0])
        return func(*args, **kwargs)

    return _dec


@register.helper
@contextmanager
def forwrapper(context, **kwargs):
    '''
    Helper for the for tag
    '''
    ctx = dict(context, **kwargs)
    yield ctx

# add
# addslashes


@register.helper
@stringfilter
def addslashes(value):
    return value.replace('\\', '\\\\').replace('"', '\\"').replace("'", "\\'")

# capfirst


@register.helper
@stringfilter
def capfirst(value):
    return value and value[0].upper() + value[1:]

# center
# cut
# date
# default
# default_if_none
# dictsort
# dictsortreversed
# divisibleby
# escape
# escapejs

_js_escapes = {
    ord('\\'): '\\u005C',
    ord('\''): '\\u0027',
    ord('"'): '\\u0022',
    ord('>'): '\\u003E',
    ord('<'): '\\u003C',
    ord('&'): '\\u0026',
    ord('='): '\\u003D',
    ord('-'): '\\u002D',
    ord(';'): '\\u003B',
    ord('\u2028'): '\\u2028',
    ord('\u2029'): '\\u2029'
}

# Escape every ASCII character with a value less than 32.
_js_escapes.update((ord('%c' % z), '\\u%04X' % z) for z in range(32))

ESCAPES = {
    'html': lambda text: text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;').replace("'", '&#39;'),
    'js': lambda text: text.translate(_js_escapes)
}


@register.helper
@stringfilter
def escape(value, mode='html'):
    return ESCAPES[mode](value)

# filesizeformat
# first
# fix_ampersands
# floatformat
# force_escape
# get_digit
# iriencode
# join
# last
# length
# length_is
# linebreaks
# linebreaksbr
# linenumbers
# ljust
# lower
# make_list
# phone2numeric
# pluralize
# pprint
# random
# removetags
# rjust
# safe
# safeseq
# slice
# slugify
# stringformat
# striptags
# time
# timesince
# timeuntil
# title
# truncatechars
# truncatechars_html
# truncatewords
# truncatewords_html
# unordered_list
# upper
# urlencode
# urlize
# urlizetrunc
# wordcount
# wordwrap
# yesno
