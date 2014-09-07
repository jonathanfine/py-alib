from alib.trytools import ReturnValue
from alib.trytools import ExceptionInstance
from alib.trytools import try_eval

try_eval('2 + 2') == ReturnValue(4)
type(try_eval('2 + []')) == ExceptionInstance
type(try_eval('2 + []').exception) == TypeError

obj = object()
ReturnValue(obj) == ReturnValue(obj)
ReturnValue(obj).value is obj
ReturnValue(obj).exception is None

exc = ValueError('message')
ExceptionInstance(exc).exception is exc
ExceptionInstance(exc).value ** AttributeError

ValueError('message') != ValueError('message')
ExceptionInstance(exc) == ExceptionInstance(exc)
ExceptionInstance(ValueError()) != ExceptionInstance(ValueError())



