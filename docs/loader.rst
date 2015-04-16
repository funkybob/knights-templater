Loader
======

.. py:module:: knights.loader

Load templates from files.

.. py:attribute:: PATHS

   A list of PATHS to search for templates.

.. py:function:: add_path(path)

   Adds a path to the list of Paths to search for templates.

   First resolves the absolute path of ``path``, then, if it's not already in
   the list, adds it to PATHS

   Relative paths are resolved relative to CWD.

.. py:function:: load_template(name, paths=None, raw=False)

   Loads and compiles a template from ``name``.

   Searches paths for a template matching the name.  If ``paths`` is not
   supplied, it will use ``PATHS``.

   If a matching file can not be found None is returned.

   If ``raw`` is True, the template class will be returned, not an instance.
