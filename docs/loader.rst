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

.. py:function:: load_template(name)

   Loads and compiles a template from ``name``.

   Searches PATHS for a template matching the name.

   Relative names are supported, but can not result in paths outside those in
   the PATHS list.

   Returns either the compiled template class, or None.
