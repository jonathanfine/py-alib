from alib.script import Script
from alib.trytools import ReturnValue, ExceptionInstance
from alib.evaluator import Evaluator
from alib.trytools import try_eval

def test_eval(src):
    script = Script(src)
    evaluator = Evaluator()
    script.run(evaluator)
    actual = evaluator.data
    assert len(actual) == 1
    return actual[0]


test_eval('2 + 2 == 5') == (['Eq'], [ReturnValue(4), ReturnValue(5)])
test_eval('2 + 2 == 4') is None
test_eval('2 < 3') is None
test_eval('1 + [] < 4') == (
    ['Lt'],
    [try_eval('1 + []'), ReturnValue(4)]
    )
test_eval('(1 + []) ** TypeError') is None
test_eval('(1 + []) ** Exception') is None