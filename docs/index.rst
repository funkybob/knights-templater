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

Introduction
============

This is one of my many template engine projects.

My specific focus this time was to use Python to compile the tag expressions,
and then use AST NodeTransformers to alter them to "work".

(See `Green Tree Snakes`_ for an excellent introductin to Python AST.)

Quick Start
===========

.. code-block:: python

    >>> import knights
    >>> t = knights.kompile('Hello {{ name}}, how are you?')
    >>> print(t()({'name': 'Bob'}))
    Hello Bob, how are you?

.. _Green Tree Snakes: https://greentreesnakes.readthedocs.org/en/latest/

