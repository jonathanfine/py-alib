from __future__ import absolute_import

import linecache
import os
import re
from functools import partial
from ..contextlib import Suppress

if 1:
    from .script import Script

# This makes it easier and safer to suppress all but
# KeyboardInterrupt.
suppress = partial(Suppress, KeyboardInterrupt)


# TODO: On Linux import not finding AAA.PY.
f_cond = re.compile(r'^[_a-z][_a-z0-9]*\.py$', flags=re.IGNORECASE).match
d_cond = re.compile(r'^[_a-z][_a-z0-9]*$', flags=re.IGNORECASE).match

def iter_d_f(walker, d_cond, f_cond):

    for d, ds, fs in walker:
        ds.sort()
        fs.sort()
        for f in filter(f_cond, fs):
            yield d, f


def testit(filename):

    print('Testing ' + filename)

    # Don't fall over if filename does not exist - #1.
    # Instead print the exception and return.
    with suppress() as suppressed:
        with open(filename) as f:
            src = f.read()

        script = Script(src)
        test_results = script.run({})

    if suppressed:
        # TODO: Improve str(suppressed).
        print(repr(suppressed.value))
        return

    # Report on the outcome.
    success_count = 0
    for val in test_results:
        if val is None:
            success_count += 1

    print('Total of {0} tests, {1} success.'.format(len(test_results), success_count))

    src_line_format = 'line {0}:  {1}'.format
    for i, val in enumerate(test_results, 1):
        if val is not None:
            lineno = val[0]
            error = val[1:]
            src_line = linecache.getline(filename, lineno).strip()
            print(src_line_format(lineno, src_line))
            # TODO: Tidy up format of this line.
            print('          ' + repr(error))
