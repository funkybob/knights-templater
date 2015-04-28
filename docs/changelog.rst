
1.0.1 (2015-04-28)
------------------

+ Added _iterator() method
+ Added {% super %} tag
+ Added ``static``, ``now`` and ``url`` helpers to compat.django
+ Fixed Django engine wrapper, and renamed to dj
+ ``loader.load_template`` now calls `os.path.abspath` on dirs

- Moved more code generation into Parser from kompiler.
- Removed debug flag
- Don't look up 'self' through context
- Fixed non-trivial for source values

1.0.0 (2015-04-20)
------------------

Initial release.
