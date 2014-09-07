'''Test driver for rewriting code so far.'''

import ast
import os

from evaluator import Evaluator
from script import Script


def dump_parse_expr(s):

    tree = ast.parse(s, mode='eval')
    return ast.dump(tree.body)


if __name__ == '__main__':

    # Boilerplate.
    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, 'some_tests.py')

    with open(filename) as f:
        script = Script(f.read())

    # Create the globals_dict we will test.
    globals_dict = {}

    # Create the globals_dict we will test.
    ast_names = 'Attribute Call Compare Eq Load Lt Name Num'.split()
    globals_dict.update(
        (k, getattr(ast,k))
        for k in ast_names
        )

    globals_dict.update(
        ast = ast,
        dpe = dump_parse_expr,
        )


    evaluator = Evaluator()
    script.run(evaluator, globals_dict)

    # Report on the outcome.
    success_count = 0
    for val in evaluator.data:
        if val is None:
            success_count += 1

    print('Total of {0} tests, {1} success.'.format(len(evaluator.data), success_count))

    for i, val in enumerate(evaluator.data, 1):
        if val is not None:
            print((i, val))
