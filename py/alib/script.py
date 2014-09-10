from __future__ import absolute_import
import ast
import itertools
import os
import sys
from .asttools import replace

__metaclass__ = type


def make_splice_node(n):

    format = '_run_test({0})'.format
    new_tree = ast.parse(format(n), mode='exec')

    # Strip off unwanted boilerplate.
    return new_tree.body[0]

def make_iter_splice_nodes():

    n = 1                       # TODO: Change this strange value.
    while 1:
        yield make_splice_node(n)
        n += 1


def inspect(node):

    if isinstance(node, ast.Expr):

        value = node.value
        if type(value) is ast.Compare:
            return (
                'compare',
                [
                    compile(ast.Expression(v), '', 'eval')
                    for v in [value.left] + value.comparators
                    ],
                [type(op).__name__ for op in value.ops]
                )
        elif type(value) is ast.BinOp and type(value.op) is ast.Pow:
            return (
                'pow',
                [
                    compile(ast.Expression(v), '', 'eval')
                    for v in (value.left, value.right)
                    ]
                )


class Script:

    def __init__(self, source, filename='<unknown>'):

        # Parse source to tree, edit, compile and save resulting code.
        self.test_counter = 0
        self.filename = filename

        # Make and use the tree in the new way.
        tree = ast.parse(source, filename=self.filename)
        removed = list(replace(tree, inspect, make_iter_splice_nodes()))
        self.code = compile(tree, self.filename, 'exec')
        self.code_store = removed


    def run(self, evaluator, globals_dict=None):
        '''Run script, rewritten expression passed to evaluator.

        Code objects are passed to evaluator methods.  The evaluator
        might be a test routine.
        '''
        if globals_dict is None:
            globals_dict = {}

        evaluator = _WrappedEvaluator(evaluator) # Interface mismatch.
        globals_dict.update(
            _run_test=evaluator.run_test, # Evaluate changed expressions.
            _code_store = self.code_store,
            )

        eval(self.code, globals_dict)


# To sort out an interface mismatch
class _WrappedEvaluator:

    def __init__(self, inner):
        self._inner = inner

    def run_test(self, *argv):

        # Prepend locals and globals to argv.
        # Assume the code sequence is the last item.
        f_caller = sys._getframe().f_back
        argv = (
            f_caller.f_locals,
            f_caller.f_globals
            ) + argv
        return self._inner.run_test(*argv)


