Flow Control
============

By default the syntax supports if/else and for.


If/Else
-------

Simple ``if`` expressions work just like in Python:

.. code-block:: html

   {% if value is True %}It is true!{% endif %}

You can also use ``else``:

.. code-block:: html

   Today is an {% if date // 2 %} even {% else %} odd {% endif %} date.

Currently ``elif`` is not supported -- nested ``if`` in ``else`` is the best solution.

For
---

The ``for`` block works just like in Python also.

.. code-block:: html

   {% for item in sequence %}{{ item }}{% endfor %}

Just like in Python, it can unpack items in a sequence:

.. code-block:: html

    {% for key, value in mydict.items() %}{{ key }}: {{ value }}{% endfor %}
