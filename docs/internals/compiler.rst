Compiler
========

.. py:module:: knights.compiler

Contains the main compilation function for driving template construction.

To avoid clashing with the built-in `compile` this method is called `kompile`.


.. py:function:: kompile(source, debug=False)

   Compiles a template from the provided source string.

   Constructs a ``knights.parser.Parser`` class, loads the default `tags` and
   `helpers`, and builds a ``__call__`` method for the class which is
   effectively:

   .. code-block:: python

      return ''.join(str(x) for x in self._root(context))

   where ``context`` is the sole argument to ``__call__``.

   Next, it calls parser.build_method('_root') to consume the tokens.

   If, after this, parser.parent is not None, it will remove the _root method,
   relying on the parent to provide one.

   Next is calls parser.build_class(), wraps it in an ast.Module, and compiles
   it.

   Finally it executes the code, putting the parser.parent and parser.helpers
   into the global context.

   It returns the 'Template' object from the resulting global context.
