import ast
from alib.trytools import try_eval, ReturnValue, ExceptionInstance
from alib.testtools.evaluator import inspect
from alib.testtools.evaluator import eval_code_factory
from alib.testtools.evaluator import call_factory
from alib.asttools import parse_expr

def test_eval(src):

    node = parse_expr(src)
    fn = inspect(ast.Expr(node))
    evaluator = eval_code_factory(globals(), globals())
    return fn(evaluator)


def test_call(src):

    root = parse_expr(src)
    fn = call_factory(root)
    evaluator = eval_code_factory(globals(), globals())
    return fn(evaluator)


def f(*argv, **kwargs):
    return argv, kwargs


test_eval('2 + 2 == 5') == (['Eq'], [ReturnValue(4), ReturnValue(5)])
test_eval('2 + 2 == 4') is None
test_eval('2 < 3') is None
test_eval('1 + [] < 4') == (
    ['Lt'],
    [try_eval('1 + []'), ReturnValue(4)]
    )

test_eval('(1 + []) ** TypeError') is None
test_eval('(1 + []) ** Exception') is None

test_call('f()') == ReturnValue(((), {}))
test_call('f(1, 2, a=3, b=4)') == ReturnValue(((1, 2), {'a': 3, 'b': 4}))
