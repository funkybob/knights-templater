First Steps
===========

Install using pip:

.. code-block:: sh

   $ pip install knights-templater


Compile a template from a string:

.. code-block:: python

   >>> from knights import kompile
   >>> t = kompile('''Hello {{ name }}, how are you?''')
   >>> t
   <Template object at 0x101362358>

Template objects are callable.  To render, just call them with a dict of values for their rendering context.

.. code-block:: python

   >>> t({'name': 'Bob'})
   'Hello Bob, how are you?'

The {{ var }} token supports Python syntax, and so is very powerful:

.. code-block:: python

   >>> t = kompile('''Hello {{ name.title() }}!''')
   >>> t({'name': 'wally west'})
   'Hello Wally West!'

The rendering process will cast everything to strings, so you don't have to.

.. code-block:: python

   >>> t = kompile('''Progress: {{ done * 100.0 / total }}% ''')
   >>> t({'total': 300, 'done': 180})
   'Progress: 60.0% '

Note, however, this is done only after the expression is evaluated.

.. code-block:: python

   >>> t({'total': 300, 'done': 'some'})
   Traceback (most recent call last):
     File "<stdin>", line 1, in <module>
     File "<compiler>", line 1, in __call__
     File "<compiler>", line 1, in _root
   TypeError: can't multiply sequence by non-int of type 'float'
