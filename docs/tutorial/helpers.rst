Helpers
=======

Template are compiled in their own module, with almost nothing else in their namespace.

Some extra helper functions are available inside the ``_`` object.

.. code-block:: html

   {{ _.escape_html(foo) }}


Additional helpers can be loaded using the {% load %} tag.
