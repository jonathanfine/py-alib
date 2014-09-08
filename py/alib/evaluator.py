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

        self.data = []


    def compare(self, locals_dict, globals_dict, test_no, discard):

        codes = globals_dict['_code_store'][test_no-1][0]
        ops = globals_dict['_code_store'][test_no-1][1]
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
            self.data.append(None)
        else:
            self.data.append((ops, values))


    def pow(self, locals_dict, globals_dict, test_no):

        codes = globals_dict['_code_store'][test_no-1][0]
        clean = True
        left, right = values = [
            try_eval(code, globals_dict, locals_dict)
            for code in codes
            ]

        if left.exception is None:
            if right.exception:
                self.data.append(values)
            else:
                self.data.append('Expected but did not get exception')
            return

        if isinstance(left.exception, right.value):
            self.data.append(None)
            return
        else:
            self.data.append(values)
