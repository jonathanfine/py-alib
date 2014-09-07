'''When run, self-test the testtools module.'''

import ast
import os
import marshal

__metaclass__ = type

try:
    import astkit as tmp
    ast_render = tmp.render.SourceCodeRenderer.render
    del tmp
except ImportError:
    ast_render = ast.dump

dirname = os.path.dirname(__file__)

filename = os.path.join(dirname, 'test_add.py')
with open(filename) as f:
    tree = ast.parse(f.read())


if 0:
    print(ast.dump(tree))


def add(x, y):
    return x + y


if 1:
    # Pick out and evaluate all suitable expressions.
    for line in tree.body:
        value = getattr(line, 'value', None)
        if value is None:
            continue

        if type(value) is ast.Compare:
            ops = value.ops
            # Make a test for this.
            if [op for op in ops if type(op) is not ast.Eq]:
                raise ValueError

            aaa = [value.left] + value.comparators

            bbb = [
                compile(ast.Expression(aa), '', 'eval')
                for aa in aaa
                ]

            print(tuple(
                    eval(bb, dict(add=add))
                    for bb in bbb
                    ))


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


def subst(expr):
    '''Start making the changes I want.'''

    value = expr.value

    # Filter the comparisons for change.
    if type(value) is ast.Compare:
        return  log_compare(value)
    else:
        return expr             # Leave unchanged.


def log_compare(node):

    # TODO: I think this is done, but is it?
    # Replace compare node with log._compare.
    # Produce the ops.
    ops = node.ops
    ops_arg = [type(op).__name__ for op in ops]

    # Produce the values.
    values = [node.left] + node.comparators
    val_args = [
        marshal.dumps(compile(ast.Expression(v), '', 'eval'))
        for v in values
        ]

    # Done so return new node.
    format = 'log._compare(globals(), locals(), {0}, {1})'.format
    # TODO: Clean up this mess.
    # TODO: Check that body appears just where I expect.
    if 0:
        new_tree = ast.parse(format(ops_arg, val_args), mode='eval')
        # TODO: Above value produces: Expression(body=Call(func=Attribute(value=Name(id='log'
    else:
        new_tree = ast.parse(format(ops_arg, val_args), mode='exec')

    # To avoid: Module(body=[Module(body=[Expr(value=Call( ...
    return new_tree.body[0]

def add(x, y):
    return x + y

class Log:

    def _compare(self, loc, glob, ops, args):

        # Evaluate prior to comparison.
        codes = [marshal.loads(item) for item in args]
        values = [
            eval(co, dict(add=add)) # TODO: Yuck.
            for co in codes
            ]

        print(('compare', ops, values))


if 1:
    edit_body_exprs(subst, tree)
    co = compile(tree, '', 'exec')
    eval(co, dict(log=Log()))


if ast_render:
    print(ast_render(tree))
