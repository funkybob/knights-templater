Lexer
-----

.. py:module:: knights.lexer

The Lexer processes the source string by breaking it into a sequence of Tokens.

.. py:class:: TokenType

   An Emum of token types.  Valid values are:

   - comment
   - text
   - var
   - block

.. py:class:: Token

   .. py:attribute:: mode

      A TokenType.

   .. py:attribute:: token

      The raw text content of the token.

   .. py:attribute:: lineno

      An estimate of the source line.

.. py:function:: tokenise(source)

   A generator yielding Tokens from the source.

   This uses `re.finditer` to break up the source string for tag, var and
   comments, inferring text nodes between.
