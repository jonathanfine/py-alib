from alib.trytools import ReturnValue
from alib.trytools import ExceptionInstance
from alib.trytools import try_eval
from alib.trytools import try_wrap

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

ExceptionInstance(exc) == ExceptionInstance(exc)
ExceptionInstance(ValueError(1, 2, 3)) == ExceptionInstance(ValueError(1, 2, 3))
ExceptionInstance(ValueError(1, 2, 3)) != 'anything else'

ValueError('message') != ValueError('message') # Gotcha!


def test_try_wrap():
    '''Here we are testing try_wrap.'''

    # TODO: Is this useful?
    @try_wrap
    def doit(value, exception=None):
        '''The docstring.'''

        if exception:
            raise exception
        else:
            return value

    doit.__doc__ ==  '''The docstring.'''
    doit.__name__ == 'doit'

    class MyException(Exception):
        pass

    obj = object()
    excp = MyException(1, 2, 3)

    doit(obj).exception == None
    doit(obj).value == obj
    doit(None, excp).exception == excp
    doit(None, excp).value ** AttributeError


# TODO: Use a decorator for this?
test_try_wrap()
