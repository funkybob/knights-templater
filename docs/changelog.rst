1.3 (2015-??-??)
----------------

Fixes:

- Don't resolve builtins via the context

1.2 (2015-05-16)
----------------

Syntax Changes

+ Make ``extends`` and ``load`` require string argument.

Optimisations

+ Inline _iterable into __call__
+ Changed escape_html and escape_js to lambdas

Fixes:

- Count line numbers from 1
- Set line numbers on all nodes returned from parse_node

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
