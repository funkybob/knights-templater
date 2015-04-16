'''
Default helper functions
'''
from functools import wraps

from .escape import escape_html, escape_js
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

ESCAPES = {
    'html': escape_html,
    'js': escape_js,
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
