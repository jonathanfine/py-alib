from __future__ import absolute_import

import os
import re

if 1:
    from .script import Script
    from .evaluator import lookup


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

    with open(filename) as f:
        script = Script(f.read())

    # TODO: Remove this ugliness.
    test_results = script.run(lookup, {})

    # Report on the outcome.
    success_count = 0
    for val in test_results:
        if val is None:
            success_count += 1

    print('Total of {0} tests, {1} success.'.format(len(test_results), success_count))

    for i, val in enumerate(test_results, 1):
        if val is not None:
            print((i, val))
