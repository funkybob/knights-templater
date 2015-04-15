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

   Optionally, it may contain an else:

   .. code-block:: html

      {% if ...expre... %}
      ...
      {% else %}
      ...
      {% endif %}

.. py:function:: for

   A python compatible {% for %} tag.

.. py:function:: include

   Include another template in situ, using the current context.

   .. code-block:: html

      {% include "othertemplate.html" %}

   Optionally, you can update the context by passing keyword arguments:

   .. code-block:: html

      {% include "other.html" foo=1, bar=baz * 6 %}

.. py:function:: with

   Temporarily augment the current context.

   .. code-block:: html

      {% with ...kwargs... %}
      ...
      {% endwith %}
