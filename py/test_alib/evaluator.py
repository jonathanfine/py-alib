from alib.script import Script
from alib.trytools import ReturnValue, ExceptionInstance
from alib.evaluator import Evaluator

def test_eval(src):
    script = Script(src)
    evaluator = Evaluator()
    script.run(evaluator)
    actual = evaluator.data
    assert len(actual) == 1
    return actual[0]

test_eval('2 + 2 == 5') == (['Eq'], [ReturnValue(4), ReturnValue(5)])

