Default Helpers
===============

.. py:module:: knights.helpers

Helpers provide utility functions and classes for templates.

Any loaded template library can provide additional helpers.

.. py:function:: stringfilter(func)

   A decorator which ensures the first argument to func is cast as a str()

The default set of helpers are as follows:

.. py:function:: addslashes(value)

   Escape \, ", and ' characters by placing a \ before them.

.. py:function:: capfirst(value)

   Capitalise only the first character of the string.

.. py:function:: escape(value, mode='html')

   Escape unsafe characters in the string.

   By default applies HTML escaping on &, <, >, " and ' characters, using HTML
   entities instead.

   Also supports 'js' mode.
