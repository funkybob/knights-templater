# knights-templater
One more Python templating engine won't hurt, surely?

This one translates templates into AST, and then into raw Python.

The syntax is reminiscent of Django's DTL, but within the tags it's almost raw
Python.

# Requirements

Python 3.4+

# Benchmarks

Everyone loves a tainted benchmark, right?

I've forked https://bitbucket.org/akorn/helloworld to add knights-templates
support.

https://bitbucket.org/funkybob/helloworld

- Django (1.8)
- Jinja2 (2.7.3)

And the results on my MacBook Air are:

    $ python -OO benchmark.py

    len(items) == 0

    01-initial         msec    rps  tcalls  funcs
    django             8087  12366     171     54
    jinja2             1278  78221      29     23
    knights             447 223834      21     10
    wheezy.template     243 412161      15      9

    02-include         msec    rps  tcalls  funcs
    django            17567   5692     393     66
    jinja2             7099  14086     113     41
    knights            1256  79601      44     18
    wheezy.template     506 197726      30     14

    03-extends         msec    rps  tcalls  funcs
    django            30714   3256     630     83
    jinja2             8980  11136     166     47
    knights            1564  63955      58     21
    wheezy.template     824 121397      48     19

    len(items) == 10

    01-initial         msec    rps  tcalls  funcs
    django            51815   1930    1237     58
    jinja2             4595  21764     120     23
    knights            4219  23700     154     15
    wheezy.template     809 123645      74      9

    02-include         msec    rps  tcalls  funcs
    django            62515   1600    1459     70
    jinja2            10550   9479     204     41
    knights            5059  19767     177     23
    wheezy.template    1093  91488      89     14

    03-extends         msec    rps  tcalls  funcs
    django            77127   1297    1696     86
    jinja2            12316   8119     279     47
    knights            5633  17754     240     26
    wheezy.template    1428  70028     107     19
