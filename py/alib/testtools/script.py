from __future__ import absolute_import
import ast
import itertools
import os
import sys
from ..asttools import replace
from .evaluator import inspect

__metaclass__ = type


def make_splice_node(n):

    format = '_run_test({0})'.format
    new_tree = ast.parse(format(n), mode='exec')

    # Strip off unwanted boilerplate.
    return new_tree.body[0]

def make_iter_splice_nodes():

    n = 0
    while 1:
        yield make_splice_node(n)
        n += 1


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


    def run(self, globals_dict=None):
        '''Run script, rewritten expression passed to evaluator.

        Code objects are passed to evaluator methods.  The evaluator
        might be a test routine.
        '''
        if globals_dict is None:
            globals_dict = {}

        test_results = []

        # Use a closure so we capture the evaluator.
        # Could also use a instance method + functools.partial.
        def run_test(test_no):

            f_caller = sys._getframe().f_back
            code = self.code_store[test_no]
            result = code(f_caller.f_locals, f_caller.f_globals)
            test_results.append(result)


        globals_dict.update(
            _run_test=run_test, # Evaluate changed expressions.
            )

        eval(self.code, globals_dict)
        return test_results




