import ast
from alib.trytools import try_eval, ReturnValue, ExceptionInstance
from alib.testtools.evaluator import inspect
from alib.asttools import parse_expr

def test_eval(src):

    node = parse_expr(src)
    fn = inspect(ast.Expr(node))
    return fn({},{})


test_eval('2 + 2 == 5') == (['Eq'], [ReturnValue(4), ReturnValue(5)])
test_eval('2 + 2 == 4') is None
test_eval('2 < 3') is None
test_eval('1 + [] < 4') == (
    ['Lt'],
    [try_eval('1 + []'), ReturnValue(4)]
    )
test_eval('(1 + []) ** TypeError') is None
test_eval('(1 + []) ** Exception') is None
