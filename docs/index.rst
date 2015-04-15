.. Knights Templater documentation master file, created by
   sphinx-quickstart on Sat Mar 28 13:12:00 2015.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Knights Templater's documentation!
=============================================

Contents:

.. toctree::
   :maxdepth: 2

   lexer
   parser
   library
   compiler
   loader
   helpers
   tags

Requirements
============

Python 3.4+

Introduction
============

This is one of my many template engine projects.

My specific focus this time was to use Python to compile the tag expressions,
and then use AST NodeTransformers to alter them to "work".

(See `Green Tree Snakes`_ for an excellent introductin to Python AST.)

Quick Start
===========

Compile and render a template from a string:

.. code-block:: python

    >>> import knights
    >>> tclass = knights.kompile('Hello {{ name}}, how are you?')
    >>> t = tclass()
    >>> print(t({'name': 'Bob'}))
    Hello Bob, how are you?

Load a template from a directory:

.. code-block:: python

   >>> from knights import loader
   >>> loader.add_path('templates/')
   >>> tclass = loader.load_template('index.html')
   >>> t = tclass()
   >>> t.render({....})
   ...

.. _Green Tree Snakes: https://greentreesnakes.readthedocs.org/en/latest/

