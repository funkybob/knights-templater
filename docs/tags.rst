Tags
====

.. py:module:: knights.tags

Default tags.

.. py:function:: load name

   Loads template library ``name``.

.. py:function:: extends name

   Make this Template class extend the template in ``name``

.. py:function:: block name

   Declares a new overridable block in the template.

   This will result in a new method on the class of the same name, so names
   must be valid Python identifiers.

.. py:function:: if expr

   Implements a simple if conditional.

   .. code-block:: html

      {% if ...expr... %}
      ...
      {% endif %}

.. py:function:: for

   A python compatible {% for %} tag.

