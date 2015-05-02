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

Using Python 3.4.3 from brew

- Django (1.8)
- Jinja2 (2.7.3)
- Mako (1.0.1)
- Tenjin (1.1.1)
- tornado (4.1)
- wheezy.html (0.1.147)
- wheezy.template (0.1.160)

And the results on my MacBook Air are:

    $ python -OO benchmark.py

    len(items) == 0

    01-initial         msec    rps  tcalls  funcs
    django             8315  12027     171     54
    jinja2             1389  72012      29     23
    knights             434 230598      20      9
    mako               3927  25462      48     36
    tenjin              995 100523      34     23
    tornado            1310  76358      36     20
    wheezy.template     215 465426      15      9

    02-include         msec    rps  tcalls  funcs
    django            20185   4954     413     68
    jinja2             7349  13607     113     41
    knights            1253  79814      43     17
    mako              15386   6499     154     51
    tenjin             3367  29701      99     29
    tornado            1381  72417      43     20
    wheezy.template     476 210222      30     14

    03-extends         msec    rps  tcalls  funcs
    django            34737   2879     664     88
    jinja2             9479  10550     166     47
    knights            1615  61936      57     20
    mako              23369   4279     230     65
    tenjin             5097  19620     130     37
    tornado            1594  62734      48     20
    wheezy.template     814 122903      48     19

    len(items) == 10

    01-initial         msec    rps  tcalls  funcs
    django            54328   1841    1237     58
    jinja2             4798  20842     120     23
    knights            4122  24259     143     14
    mako               6835  14631     137     36
    tenjin             3094  32316     103     23
    tornado            5385  18571     227     20
    wheezy.template     828 120825      74      9

    02-include         msec    rps  tcalls  funcs
    django            71065   1407    1479     72
    jinja2            11818   8462     204     41
    knights            4968  20128     166     22
    mako              19102   5235     243     51
    tenjin             5589  17891     168     29
    tornado            5498  18189     234     20
    wheezy.template    1099  91016      89     14

    03-extends         msec    rps  tcalls  funcs
    django            89759   1114    1730     91
    jinja2            13428   7447     279     47
    knights            5394  18540     229     25
    mako              28499   3509     319     65
    tenjin             7564  13221     199     37
    tornado            5442  18375     239     20
    wheezy.template    1530  65380     107     19

* Note: wheezy.html has a C-optimised version of escape().
  When not used it can impact their render speed from 20 to 50 %

* Note: Jinja2 and Mako use MarkupSafe, which has C-optimised functions for
  escaping.
