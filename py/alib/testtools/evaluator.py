'''Evaluate expressions
'''

from __future__ import absolute_import

from .trytools import try_eval
import operator

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


class Evaluator:

    def __init__(self):

        pass                    # Was self.data = [].

    @staticmethod
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


    @staticmethod
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
