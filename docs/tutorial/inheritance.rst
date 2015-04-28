Inheritance
===========

Templates are able to extend other templates, allowing you to avoid duplication.

The base template much declare ``{% block %}`` which can be overriden.  Each block has an unique name, which becomes a method on the class.

.. code-block:: html

   <!DOCTYPE html>
   <html>
       <head>
           <title>{% block title %}default title{% endblock %}</title>
       </head>
       <body>{% block content %}{% endblock %}</body>
   </html>

Any blocks not overriden by an inheriting template will default to their parent classes implementation, as you'd expect.

.. code-block:: html

   {% extends base.html %}
   {% block title %}My Title {% endblock%}

The ``super`` tag allows you to access blocks from the parent class.

.. code-block:: html

   {% extends base.html %}
   {% block title %}{% super title %} - Extra title{% endblock %}


