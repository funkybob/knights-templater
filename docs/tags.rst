Default Tags
============

.. py:module:: knights.tags

Default tags.

.. py:function:: load name

   .. code-block:: html

      {% load foo.bar.baz %}

   Loads template library ``name``.

   The name is treated as a python import path, and the loaded module is
   expected to have a 'register' member, being an instance of :library:Library

.. py:function:: extends name

   .. code-block:: html

      {% extends base.html %}

   Make this Template class extend the template in ``name``

.. py:function:: super name

   .. code-block:: html

      {% super blockname %}

   Renders the contents of ``blockname`` from the parent template.

.. py:function:: block name

   .. code-block:: html

      {% block foo %}
      ...
      {% endblock %}

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

   .. code-block:: html

      {% for a in sequence %}
      ...
      {% endfor %}

   A python compatible {% for %} tag.

   .. code-block:: html

      {% for a, b, c in foo.get(other=1) %}
      ...
      {% endfor %}

   The target values will be stacked on the scope for the duration, and removed
   once the loop exits.

   Also you can provide an 'empty' block for when the list is empty.

   .. code-block:: html

      {% for a in sequence %}
      ...
      {% empty %}
      sequence is empty
      {% endfor %}

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
