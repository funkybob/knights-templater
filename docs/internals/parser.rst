------
Parser
------

.. py:module:: knights.parser

The Parser processes the Token stream from the `lexer` and produces a Template
class.

.. py:class:: Parser(source, loader)

   Used to parse token streams and produce a template class.

   .. py:attribute:: loader

      The ``loader.TemplateLoader`` instance for this parser to use, or None.
      This value is passed via the ``compiler.kompile`` call from the
      ``loader.TempateLoader``, and is required for the ``{% extends %}`` and
      ``{% include %}`` tags to work.

   .. py:attribute:: stream

      A ``lexer.tokenise`` generator.

   .. py:attribute:: parent = None

      The parent class to use for this Template

   .. py:attribute:: methods

      A list of ast.Method nodes

   .. py:attribute:: tags

      Tag generators loaded from tag libraries.

   .. py:attribute:: helpers

      Helper functions loaded from tag libraries.

   .. py:method:: load_library(path)

      Load a custom tag library from ``path``.

      It is assumed it will contain an object called `register`, which will
      have dict properties `tags` and `helpers` to be updated with the parsers.

   .. py:method:: build_method(name, endnodes=None)

      Build a new method called `name`, and make its body the set of nodes up
      to any listed in `endnodes`, or the end if None.

      The method is appended to self.methods

   .. py:method:: parse_node(endnodes=None)

      Yield a stream of AST Nodes based on self.stream

      `text` nodes will produce effectively:

      .. code-block:: python

         yield token

      `var` nodes will produce code to evaluate the expression and yield their
      value.

      `block` nodes will be resolved through the registered tags, unless they
      match any listed in ``endnodes``, in which case the raw name will be
      yielded before terminating the loop.

   .. py:method:: parse_nodes_until(\*endnodes)

      Return two values - a list of nodes, and the name of the matching end
      node.  This is used for implementing

   .. py:method:: build_class

      Construct a Class definition from the current state.

      The base class will either be 'object' if self.parent is None, else
      'parent'.

   .. py:method:: parse_expression(expr)

      Helper method to parse an expression and convert raw variable references
      to context lookups.

   .. py:method:: parse_args(expr)

      Helper method to parse an expression and yield a list of args and kwargs.


.. py:function:: wrap_name_in_context(name)

   Utility function to turn an ast.Name() node into code to affect:

   .. code-block:: py

      context['name']

.. py:class:: VarVisitor

   A subclass of :ast:NodeTransformer which applies `wrap_name_in_context` to
   all Name nodes in the AST it visits.
