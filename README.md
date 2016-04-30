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

- Django (1.9.5)
- Jinja2 (2.8)
- knights-templater (1.3)
- Mako (1.0.4)
- Tenjin (1.1.1)
- tornado (4.3)
- wheezy.html (0.1.147)
- wheezy.template (0.1.167)

Legend:
    msec  : milliseconds per render
    rps   : renders per second
    tcalls: total function calls
    funcs : distinct functions called

Performed on my old Core2Duo E8500:

    len(items) == 0

    01-initial         msec    rps  tcalls  funcs
    django            13226   7561     171     55
    jinja2             2684  37257      29     23
    knights             701 142644      20      9
    mako               6138  16291      48     36
    tenjin             1839  54391      34     23
    tornado            2096  47709      36     20
    wheezy.template     296 338407      15      9

    02-include         msec    rps  tcalls  funcs
    django            35133   2846     430     72
    jinja2            32744   3054     201     54
    knights            1933  51726      43     17
    mako              23634   4231     154     51
    tenjin             6473  15449      99     29
    tornado            2137  46804      43     20
    wheezy.template     668 149604      30     14

    03-extends         msec    rps  tcalls  funcs
    django            54128   1847     682     89
    jinja2            37533   2664     273     59
    knights            2424  41248      57     20
    mako              34599   2890     230     65
    tenjin             9829  10174     148     40
    tornado            2266  44134      48     20
    wheezy.template    1240  80674      48     19

    04-outer           msec    rps  tcalls  funcs
    django            54136   1847     682     89
    jinja2            38920   2569     273     59
    knights            2473  40433      57     20
    mako              35532   2814     233     65
    tenjin             9899  10102     148     40
    tornado            2247  44498      48     20
    wheezy.template    1261  79272      48     19

    len(items) == 10

    01-initial         msec    rps  tcalls  funcs
    django            85435   1170    1237     59
    jinja2             8528  11726     120     23
    knights            5696  17557     143     14
    mako              10660   9381     137     36
    tenjin             4492  22264     103     23
    tornado            7041  14202     227     20
    wheezy.template    1188  84155      74      9

    02-include         msec    rps  tcalls  funcs
    django           106752    937    1496     75
    jinja2            33734   2964     292     54
    knights            6603  15146     166     22
    mako              28664   3489     243     51
    tenjin             9312  10739     168     29
    tornado            6999  14287     234     20
    wheezy.template    1579  63314      89     14

    03-extends         msec    rps  tcalls  funcs
    django           129641    771    1748     92
    jinja2            45724   2187     386     59
    knights            7772  12867     229     25
    mako              39965   2502     319     65
    tenjin            12185   8207     199     37
    tornado            6787  14735     239     20
    wheezy.template    2112  47340     107     19

    04-outer           msec    rps  tcalls  funcs
    django           155362    644    2228     92
    jinja2            44932   2226     427     59
    knights           11172   8951     339     25
    mako              43095   2320     382     65
    tenjin            14834   6741     277     40
    tornado           10311   9699     349     20
    wheezy.template    2642  37849     137     19


* Note: wheezy.html has a C-optimised version of escape().
  When not used it can impact their render speed from 20 to 50 %

* Note: Jinja2 and Mako use MarkupSafe, which has C-optimised functions for
  escaping.
