from __future__ import absolute_import

import os
import re

if 1:
    from .evaluator import Evaluator
    from .script import Script


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

    evaluator = Evaluator()
    script.run(evaluator, {})

    # Report on the outcome.
    success_count = 0
    for val in evaluator.data:
        if val is None:
            success_count += 1

    print('Total of {0} tests, {1} success.'.format(len(evaluator.data), success_count))

    for i, val in enumerate(evaluator.data, 1):
        if val is not None:
            print((i, val))
