Loading Templates
=================

Templates can be loaded from files.  The ``loader.TemplateLoader`` class makes
it easy to access a list of directories for templates.

First you need to create a ``TemplateLoader``

.. code-block:: python

   >>> from knights.loader import TemplateLoader
   >>> loader = TemplateLoader(['templates'])

The list of paths provided will be resolved relative to the CWD.

Now you can ask the loader to find a template in any of the supplied
directories:

.. code-block:: python

   >>> t = loader.load('index.html')

Additionally, the loader will act as a cache if used like a dict:

.. code-block:: python

   >>> t = loader['index.html']  # Will load and parse the class
   >>> s = loader['index.html']  # Will reuse the existing instance
