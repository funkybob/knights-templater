Loader
======

.. py:module:: knights.loader

Load templates from files.

.. py:class:: TemplateNotFound(Exception)

   The exception class raised when a template can not be found.

.. py:class:: TemplateLoader(paths)

   Provides a way to load templates from a list of directories.

   `paths` is a list of paths to search for template files.  Relative paths
   will be resolved relative to CWD.

   A TemplateLoader will also act as a cache if accessed as a dict.

   .. code-block:: python

      >>> loader = TemplateLoader(['templates'])
      >>> tmpl = loader['index.html']

   .. py:method:: load(name, raw=False)

      Find the template `name` in one of the `paths` and compile it.

      If the `raw` flag is passed, the returned value will be the class, not an
      instance.
