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

    $ python benchmark.py

    len(items) == 0

    01-initial         msec    rps  tcalls  funcs
    django             8416  11882     173     56
    jinja2             1282  78003      29     23
    knights             382 261828      23      9
    wheezy.template     223 447869      15      9

    02-include         msec    rps  tcalls  funcs
    django            18398   5435     395     67
    jinja2             7003  14279     113     41
    knights            1360  73505      35      9
    wheezy.template     527 189631      30     14

    03-extends         msec    rps  tcalls  funcs
    django            34262   2919     632     84
    jinja2             9781  10224     166     47
    knights            1690  59162      39     12
    wheezy.template     851 117446      48     19

    len(items) == 10

    01-initial         msec    rps  tcalls  funcs
    django            55839   1791    1209     60
    jinja2             5049  19808     120     23
    knights            5140  19456     151     12
    wheezy.template     893 111948      74      9

    02-include         msec    rps  tcalls  funcs
    django            64784   1544    1431     71
    jinja2            10741   9310     204     41
    knights            6339  15776     163     12
    wheezy.template    1171  85428      89     14

    03-extends         msec    rps  tcalls  funcs
    django            76842   1301    1668     87
    jinja2            12695   7877     279     47
    knights            7101  14082     102     15
    wheezy.template    1538  65006     107     19
