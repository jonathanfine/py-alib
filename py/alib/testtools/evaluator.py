'''Evaluate expressions
'''

from __future__ import absolute_import

import ast
import operator

from ..trytools import try_eval


__metaclass__ = type


compare_dict = dict(
    # TODO: Finish this dict.
    Eq = operator.eq,
    In = lambda a, b: operator.contains(b, a),
    Is = operator.is_,
    Lt = operator.lt,
    IsNot = operator.is_not,
    NotEq = operator.ne,
    )


class Compare:

    def __init__(self, node):

        assert type(node) is ast.Compare
        self.code = [
            compile(ast.Expression(v), '', 'eval')
            for v in [node.left] + node.comparators
            ]
        self.ops = [type(op).__name__ for op in node.ops]


    def __call__(self, locals_dict, globals_dict):

        return compare(locals_dict, globals_dict, self.code, self.ops)


class Pow:

    def __init__(self, node):

        assert type(node) is ast.BinOp and type(node.op) is ast.Pow

        self.code = [
            compile(ast.Expression(v), '', 'eval')
            for v in (node.left, node.right)
            ]


    def __call__(self, locals_dict, globals_dict):

        return pow(locals_dict, globals_dict, self.code)


def compare(locals_dict, globals_dict, codes, ops):

    # TODO: Special case a single operation.
    # TODO: If you special case that, make sure you test.
    clean = True
    values = []
    for code in codes:
        val_or_exc = try_eval(code, globals_dict, locals_dict)
        if val_or_exc.exception:
            clean = False
        values.append(val_or_exc)

    comparisons = []
    for left, op, right in zip(values, ops, values[1:]):

        # TODO: Might raise exception.
        if left.exception or right.exception:
            comp = None
        else:
            comp = bool(compare_dict[op](left.value, right.value))
            if not comp:
                clean = False
        comparisons.append(comp)

    if clean:
        return None
    else:
        return ops, values


def pow(locals_dict, globals_dict, codes):

    clean = True
    left, right = values = [
        try_eval(code, globals_dict, locals_dict)
        for code in codes
        ]

    if left.exception is None:
        if right.exception:
            return values
        else:
            return 'Expected but did not get exception'

    if isinstance(left.exception, right.value):
        return None
    else:
        return values

lookup = dict(compare=compare, pow=pow)
