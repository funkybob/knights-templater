.. Knights Templater documentation master file, created by
   sphinx-quickstart on Sat Mar 28 13:12:00 2015.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Knights Templater's documentation!
=============================================

Contents:

.. toctree::
   :maxdepth: 2

Introduction
============

This is one of my many template engine projects.

My specific focus this time was to use Python to compile the tag expressions,
and then use AST NodeTransformers to alter them to "work".
 
(See `Green Tree Snakes`_ for an excellent introductin to Python AST.)

Internals
=========

Lexer
-----

The lexer was pulled straight from django-contemplation, and then simplified by
removing "verbatim" support.

It uses the re.finditer function to successively find tags in the source
string, inferring text nodes between them.

.. code-block:: python

    tag_re = re.compile(
        '|'.join([
            r'{\!\s*(?P<load>.+?)\s*\!}',
            r'{%\s*(?P<tag>.+?)\s*%}',
            r'{{\s*(?P<var>.+?)\s*}}',
            r'{#\s*(?P<comment>.+?)\s*#}'
        ]),
        re.DOTALL
    )

This shows there are four types of nodes:

Load:
    Directive to load a tag library

Tag:
    Block tag directive.

Var:
    Var expression.

Comment:
    Comment

------
Parser
------

There are currently two parser in use.

Parser 1
--------

The original parser currently functions well enough to produce templates with
var nodes and block nodes, including IF and FOR block node implementations. It
even supports loadable tag/filter libraries.

It is defined in parser.py, and used by ``base.Template``.

It retains the state of:

- a lexer generator
- a dict of tags
- a dict of filters

After passing the raw template source when instanciating it, calling it will
return a list() of nodes.  The ``Template`` then compiles the equivalent of:

.. code-block:: python

   return ''.join(str(x(context)) for x in nodelist)

Internally it calls ``self.parse_node()`` to yield the next node.  This method
determines if the next lexer token is a Load, Text, Var or Block.

For Load tokens, it immediately imports the library, and tries to update its
tags/filters maps from 'library' in it.

For Text tokens, it creates a TextNode which renders as just its token.

For Var tokens, it creates a VarNode, which compiles the token as Python,
then visits the nodes using a ``NodeTransformer``.  This Transformer finds all
>> operations and tries to turn them into filter uses.

For example, 

.. code-block:: django

   {{ foo >> bar }}

would become

.. code-block:: python

   _filters['bar'](foo)

and

.. code-block:: django

   {{ foo >> bar(baz) }}

would become

.. code-block:: python

   _filters[bar](foo, baz)

Node tokens have the first "word" split, and looked up in the tags map.  The
callable found there is passed the parser and the rest of the token, and
expected to return a callable for rendering time.

Since the parse_node method is a generator, block nodes can call it to build
child nodelists.


Parser 2
--------

The second parser was born from a desire to implement template inheritance.

The obvious solution to implementing overridable blocks in the template was to
make them a class, and each block be a method.

The plan was to have each token ``yield`` its value, added them to the body of
the ``_root`` method.  Overridable blocks would create a new method that
otherwise functions the same, and contribute a ``yield from`` expression to
their parent block.

Inheriting a template means adding a new base class, accessing super means
accessing ``super()``.

So far I've got ``klass.kompile`` which will construct AST for a class, compile
it, then return an instance of it.

First it creates a Parser instance, which holds the token stream, a list of
base classes (just 'object' by default), a list of methods, and a map of tags
loaded.

Then it builds a ``__call__`` method in AST.  This method is effectively:

.. code-block:: python

   def __call__(self, context):
       return ''.join(str(x) for x in self._root(context))

Next it uses the ``parser.build_method`` method to define ``_root``, the main
block container method.

Then it uses ``parser.build_class`` to build AST for defining the class, wraps
it in a Module, and compiles it.

Finally it returns the class created.  An instance of which is a callable which
will accept a dict as context, and return the rendered template.

The ``parser.build_method`` function accepts a name for the method, and
optionally a list of end tokens.  It creates a method in AST, then iterates
``parser.parse_node(endnodes)`` for all it can get, appending the results to
the body of the method.

In ``parser.parse_node``, the token stream is iterated.

Load tags will cause a library load [currently unimplemented].

Text nodes will create a Yield statement, yielding the string literal.

Var nodes will compile their token as Python, and apply a NodeTransformer which
changes all Name nodes to become context lookups.

.. admonition::  This is currently tragically naive

   It will likely break non-trivial expressions.

The `{% block name %}` tag is implemented and functioning correctly.

A simple `{% if _expr_ %}` tag has been implemented, also.

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

.. _Green Tree Snakes: https://greentreesnakes.readthedocs.org/en/latest/

