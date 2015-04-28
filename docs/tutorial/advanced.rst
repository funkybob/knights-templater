Advanced Usage
==============

Since Templates are Python classes, you can use them like any other class.


Inheriting
----------

You can add your own methods for providing extra functionality just like with
any other Python class.

If you want your method to work with `{% block %}` it must accept ``context``
as its first positional argument, and will be called in a `yield from` clause:

.. code-block:: python

   yield from self.blockname(context)


Re-use
------

Logically, you can also call blocks on a template the same way.  Pass a
dict-like object as context, and they return a generator.
