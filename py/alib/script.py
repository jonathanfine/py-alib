import ast
import os
import marshal
import sys

__metaclass__ = type

class Script:

    def __init__(self, source, filename='<unknown>'):

        # Parse source to tree, edit, compile and save resulting code.
        self.test_counter = 0
        self.filename = filename
        self.code_store = []
        tree = ast.parse(source, filename=self.filename)
        edit_body_exprs(self.edit_expr, tree)
        self.code = compile(tree, self.filename, 'exec')


    def run(self, evaluator, globals_dict=None):
        '''Run script, rewritten expression passed to evaluator.

        Code objects are passed to evaluator methods.  The evaluator
        might be a test routine.
        '''
        if globals_dict is None:
            globals_dict = {}

        evaluator = _WrappedEvaluator(evaluator) # Interface mismatch.
        globals_dict.update(
            _evaluator_=evaluator, # Evaluate changed expressions.
            _code_store = self.code_store,
            )

        eval(self.code, globals_dict)


    # This function helps defined the transformation we want.
    # Wish to enumerate tests in script.
    def edit_expr(self, expr):
        '''Start making the changes I want.'''

        value = expr.value

        # Filter the comparisons for change.
        if type(value) is ast.Compare:
            self.test_counter += 1
            return log_compare(self.code_store, self.test_counter, value)
        elif type(value) is ast.BinOp and type(value.op) == ast.Pow:
            self.test_counter += 1
            return log_pow(self.code_store, self.test_counter, value)
        else:
            # TODO: Raise exception or warning?
            return expr             # Leave unchanged.


# To sort out an interface mismatch
class _WrappedEvaluator:

    def __init__(self, inner):
        self._inner = inner

    def compare(self, *argv):

        # Prepend locals and globals to argv.
        # Assume the code sequence is the last item.
        f_caller = sys._getframe().f_back
        argv = (
            f_caller.f_locals,
            f_caller.f_globals
            ) + argv[:-1] + ([marshal.loads(s) for s in argv[-1]],)
        return self._inner.compare(*argv)

    def pow(self, *argv):

        # Prepend locals and globals to argv.
        # Assume the code sequence is the last item.
        f_caller = sys._getframe().f_back
        argv = (
            f_caller.f_locals,
            f_caller.f_globals
            ) + argv[:-1] + ([marshal.loads(s) for s in argv[-1]],)
        return self._inner.pow(*argv)



# This function helps defined the tranformation we want.
# TODO: Rename this function.
def log_compare(code_store, test_no, node):

    # TODO: I think this is done, but is it?
    # Replace compare node with log._compare.
    # Produce the ops.
    ops = node.ops
    ops_arg = [type(op).__name__ for op in ops]

    # Produce the values.
    values = [node.left] + node.comparators
    code_store.append([
            compile(ast.Expression(v), '', 'eval')
            for v in values
            ])
    val_args = map(marshal.dumps, code_store[-1])

    # Done so return new node.
    format = '_evaluator_.compare({0}, {1}, {2})'.format
    # TODO: Clean up this mess.
    # TODO: Check that body appears just where I expect.
    if 0:
        # TODO: Produces
        # Expression(body=Call(func=Attribute(value=Name(id='log'
        new_tree = ast.parse(format(ops_arg, val_args), mode='eval')
    else:
        # TODOD: Produces
        # Module(body=[Module(body=[Expr(value=Call( ...
        new_tree = ast.parse(format(test_no, ops_arg, val_args), mode='exec')

    # Strip off unwanted boilerplate.
    return new_tree.body[0]


def log_pow(code_store, test_no, node):

    val_args = [
        marshal.dumps(compile(ast.Expression(v), '', 'eval'))
        for v in (node.left, node.right)
        ]

    code_store.append([
            compile(ast.Expression(v), '', 'eval')
            for v in (node.left, node.right)
            ])
    val_args = map(marshal.dumps, code_store[-1])

    format = '_evaluator_.pow({0}, {1})'.format
    new_tree = ast.parse(format(test_no, val_args), mode='exec')

    return new_tree.body[0]


# This utility function is based on ast module.
def edit_body_exprs(fn, tree):
    '''Use fn to edit expressions used as statements.
    '''
    # TODO: I don't like this use of subclassing.
    class Transformer(ast.NodeTransformer):

        def generic_visit(self, node):

            body = getattr(node, 'body', None)
            if body is None:
                super(Transformer, self).generic_visit(node)
                return node
            else:
                node.body = [
                    fn(line)
                    if type(line) is ast.Expr
                    else self.generic_visit(line)
                    for line in body
                    ]
                return node

    # We're editing the tree, not visiting it.
    return Transformer().visit(tree)
