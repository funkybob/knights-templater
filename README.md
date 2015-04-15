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

And the results on my MacBook Air are:

Django (1.8)
Jinja2 (2.7.3)

    $ python benchmark.py

    len(items) == 0

    01-initial         msec    rps  tcalls  funcs
    django             8011  12483     173     56
    jinja2             1292  77400      29     23
    knights             408 245158      24      8

    02-include         msec    rps  tcalls  funcs
    django            18193   5497     395     67
    jinja2             6849  14600     113     41
    knights            1191  83991      28      8

    03-extends         msec    rps  tcalls  funcs
    django            29791   3357     632     84
    jinja2             8639  11575     166     47
    knights            1593  62771      36     11

    len(items) == 10

    01-initial         msec    rps  tcalls  funcs
    django            51509   1941    1209     60
    jinja2             4628  21608     120     23
    knights            5921  16888     162     12

    02-include         msec    rps  tcalls  funcs
    django            72161   1386    1431     71
    jinja2            10276   9731     204     41
    knights            6721  14878     166     12

    03-extends         msec    rps  tcalls  funcs
    django            74033   1351    1668     87
    jinja2            12033   8310     279     47
    knights            7357  13592     174     15
