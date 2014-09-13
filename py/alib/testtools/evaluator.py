'''Evaluate expressions
'''

from __future__ import absolute_import

import ast
import operator

from ..trytools import try_eval


__metaclass__ = type


def inspect(node):

    if isinstance(node, ast.Expr):

        value = node.value
        if type(value) is ast.Compare:
            return compare_factory(value)
        elif type(value) is ast.BinOp and type(value.op) is ast.Pow:
            return pow_factory(value)


compare_dict = dict(
    # TODO: Finish this dict.
    Eq = operator.eq,
    In = lambda a, b: operator.contains(b, a),
    Is = operator.is_,
    Lt = operator.lt,
    IsNot = operator.is_not,
    NotEq = operator.ne,
    )


def compare_factory(node):

    codes = [
        compile(ast.Expression(v), '', 'eval')
        for v in [node.left] + node.comparators
        ]
    ops = [type(op).__name__ for op in node.ops]


    def compare(l_dict, g_dict):

        # TODO: Special case a single operation.
        # TODO: If you special case that, make sure you test.
        clean = True
        values = []
        for code in codes:
            val_or_exc = try_eval(code, g_dict, l_dict)
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

    return compare


def pow_factory(node):

    codes = [
        compile(ast.Expression(v), '', 'eval')
        for v in (node.left, node.right)
        ]

    def pow(l_dict, g_dict):

        clean = True
        left, right = values = [
            # TODO: Sort aout l_dict, g_dict order mismatch.
            try_eval(code, g_dict, l_dict)
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

    return pow
