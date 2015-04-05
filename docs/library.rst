Library
=======

.. py:module:: knights.library

Provides a class for defining custom template utility libraries.

.. py:class:: Library

   .. py:attribute:: tags = {}

      A dict of template tag handler functions

   .. py:attribute:: helpers = {}

      A dict of helpers to be added to the template modules global scope.


Custom tags
-----------

To define a custom tag or helper, you first need a library.

.. code-block:: python

   from knights.library import Library

   register = Library()

You must call the instance ``regsiser`` as the Parser will only look for that
name, currently.

Next, you can register helpers as follows:

.. code-block:: python

   @register.helper
   def addone(value):
       return value + 1

If the name you want to use is reserved or a builtin, you can pass it to the
decorator:

.. code-block:: python

   @register.helper(name='sun')
   def addone(value):
       return value + 1


Custom tag handlers are more complex, as they require you to construct AST.
Howerver, they are just as simple to register.

.. code-block:: python

   @register.tag
   def mytag(parser, token):
      ...

Tags are parsed the parser, and the rest of the token text after their name
was split from the front.
