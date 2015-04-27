Loading Templates
=================

Templates can be loaded from files.  The loader needs a file name, and a list of directories to search for it.

.. code-block:: python

   >>> from knights import loader
   >>> t = loader.load_template('index.html', ['.'])

If your application has a set of known template dirs, you can add them to the search path, and omit the list from load_template:

.. code-block:: python

   >>> from knights import loader
   >>> loader.add_path('.')
   >>> t = loader.load_template('index.html')

