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

Using Python 3.5.1 on Debian

- Django (1.10.0)
- Jinja2 (2.8)
- knights-templater (1.3)
- Mako (1.0.4)
- Tenjin (1.1.1)
- tornado (4.4.1)
- wheezy.html (0.1.147)
- wheezy.template (0.1.167)

Legend:
    msec  : milliseconds per render
    rps   : renders per second
    tcalls: total function calls
    funcs : distinct functions called

Performed on my i5-4200U laptop:

    len(items) == 0

    01-initial         msec    rps  tcalls  funcs
    django             4708  21241     165     56
    jinja2              872 114683      29     23
    knights             309 324025      20      9
    mako               2147  46570      48     36
    tenjin              668 149752      34     23
    tornado             929 107640      45     24
    wheezy.template     143 697091      15      9

    02-include         msec    rps  tcalls  funcs
    django            13309   7514     432     71
    jinja2            12401   8064     201     54
    knights             866 115519      43     17
    mako               9006  11104     154     51
    tenjin             2387  41886      99     29
    tornado             951 105182      52     24
    wheezy.template     296 337269      30     14

    03-extends         msec    rps  tcalls  funcs
    django            22127   4519     685     88
    jinja2            15609   6407     273     59
    knights            1049  95298      57     20
    mako              13611   7347     230     65
    tenjin             3563  28067     130     37
    tornado             993 100713      57     24
    wheezy.template     527 189705      48     19

    04-outer           msec    rps  tcalls  funcs
    django            22180   4509     685     88
    jinja2            15474   6462     273     59
    knights            1053  94965      57     20
    mako              14100   7092     233     65
    tenjin             3523  28389     130     37
    tornado             991 100932      57     24
    wheezy.template     534 187185      48     19

    len(items) == 10

    01-initial         msec    rps  tcalls  funcs
    django            30390   3291    1171     61
    jinja2             3350  29851     120     23
    knights            2746  36417     143     14
    mako               4040  24752     137     36
    tenjin             2122  47115     103     23
    tornado            3211  31139     236     24
    wheezy.template     568 176015      74      9

    02-include         msec    rps  tcalls  funcs
    django            39864   2509    1438     75
    jinja2            15426   6482     292     54
    knights            3276  30527     166     22
    mako              10741   9310     243     51
    tenjin             3871  25836     168     29
    tornado            3272  30559     243     24
    wheezy.template     731 136849      89     14

    03-extends         msec    rps  tcalls  funcs
    django            50971   1962    1691     92
    jinja2            18643   5364     386     59
    knights            3687  27122     229     25
    mako              15925   6279     319     65
    tenjin             5154  19402     199     37
    tornado            3306  30252     248     24
    wheezy.template     985 101494     107     19

    04-outer           msec    rps  tcalls  funcs
    django            62058   1611    2183     96
    jinja2            20227   4944     427     59
    knights            5453  18338     339     25
    mako              17872   5595     382     65
    tenjin             6154  16251     259     37
    tornado            4859  20582     358     24
    wheezy.template    1310  76312     137     19


* Note: wheezy.html has a C-optimised version of escape().
  When not used it can impact their render speed from 20 to 50 %

* Note: Jinja2 and Mako use MarkupSafe, which has C-optimised functions for
  escaping.
