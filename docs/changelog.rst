1.2 (2015-??-??)
----------------

Syntax Changes

+ Make ``extends`` and ``load`` require string argument.

Optimisations

+ Inline _iterable into __call__

1.1 (2015-04-28)
----------------

Features:

+ Added _iterator() method
+ Added {% super %} tag
+ Added ``static``, ``now`` and ``url`` helpers to compat.django
+ Fixed Django engine wrapper, and renamed to dj
+ ``loader.load_template`` now calls `os.path.abspath` on dirs

Fixes:

- Moved more code generation into Parser from kompiler.
- Removed debug flag
- Don't look up 'self' through context
- Fixed non-trivial for source values

1.0 (2015-04-20)
----------------

Initial release.
