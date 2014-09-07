'''Tools for writing tests.

Often, a test is something that is applied to a function.  Normally a
function is applied to its arguments, but in a test the function is
the argument.

>>> ReturnTest(4, 2, 2)(lambda a, b: a + b) is None
True

>>> ReturnTest(5, 2, 2)(lambda a, b: a + b)
WrongValue(expect=5, actual=4)

>>> ReturnTest(4, 2, '2')(lambda a, b: a + b)
ValueExpected(expect=4, actual=TypeError("unsupported operand type(s) for +: 'int' and 'str'",))

>>> RaiseTest(TypeError, 2, '')(lambda a, b: a + b) is None
True

# Use subscript to restore Python2/3 compatility.
>>> RaiseTest(ValueError, 2, '')(lambda a, b: a + b)[1]
TypeError("unsupported operand type(s) for +: 'int' and 'str'",)

>>> RaiseTest((TypeError, ValueError), 2, '')(lambda a, b: a + b) is None
True

# Use subscript to restore Python2/3 compatility.
>>> RaiseTest(TypeError, 2, 2)(lambda a, b: a + b)[1]
4


>>> test_suite = TestSuite([(4, 2, 2), ('ab', 'a', 'b'), (5, 2, 2)])
>>> test_suite(lambda a, b: a + b)
[(2, WrongValue(expect=5, actual=4))]


>>> addtests((5, 2, 2),)(lambda a, b: a + b)
Args(argv=(2, 2), kwargs={})
WrongValue(expect=5, actual=4)
<function <lambda> at 0x...>

'''


# TODO: Move in file?
def sequence_to_test(sequence):

    # TODO: Finish.
    return ReturnTest(*sequence)


# TODO: Move in file?
class TestSuite(object):

    def __init__(self, tests):

        self._tests = tuple(map(sequence_to_test, tests))

    def __call__(self, fn):

        result = []
        for index, value in enumerate(self._tests):
            failure = value(fn)
            if failure is not None:
                result.append((index, failure))

        return result


# TODO: Move in file?
def addtests(*tests):

    test_suite = TestSuite(tests)

    def next(fn):

        results = test_suite(fn)
        # TODO: Reporting of results to be configurable.
        for index, failure in results:
            print(repr(test_suite._tests[index]._args))
            print(failure)

        return fn

    return next


class FunctionTestFailure(tuple):

    '''
    >>> FunctionTestFailure(1, 2)
    FunctionTestFailure(expect=1, actual=2)

    >>> FunctionTestFailure(expect=1, actual=2)
    FunctionTestFailure(expect=1, actual=2)
    '''

    def __new__(cls, expect, actual):

        return tuple.__new__(cls, (expect, actual))

    def __repr__(self):

        args = (self.__class__.__name__,) + self
        return '%s(expect=%r, actual=%r)' % args

class WrongValue(FunctionTestFailure):
    pass

class WrongException(FunctionTestFailure):
    pass

class ValueExpected(FunctionTestFailure):
    pass

class ExceptionExpected(FunctionTestFailure):
    pass




def try_apply(fn, argv=[], kwargs={}):

    '''Execute fn, return either ReturnValue or ExceptionInstance.'''

    try:
        value = fn(*argv, **kwargs)
    except Exception as e:
        return ExceptionInstance(e)
    return ReturnValue(value)


# TODO: Can we use collections.namedtuple?

class singleton(tuple):

    '''Create a single element tuple. Use to hold/wrap a value.

    >>> singleton('anything')
    singleton('anything')

    >>> x = {}; singleton(x)[0] is x;
    True
    '''

    __slots__ = ()

    def __new__(cls, value):
        return tuple.__new__(cls, (value,))

    def __repr__(self):
        return '%s(%r)' % (self.__class__.__name__, self[0])


class ReturnValue(singleton):

    '''Holder for value returned by a function call.

    >>> ReturnValue('anything')
    ReturnValue('anything')

    >>> x ={}; ReturnValue(x).value is x
    True

    >>> ReturnValue('anything').exception is None
    True
    '''

    __slots__ = ()
    exception = None

    @property
    def value(self):
        return self[0]


class ExceptionInstance(singleton):

    '''Holder for exception raised by function call.

    >>> ExceptionInstance('anything')
    ExceptionInstance('anything')

    >>> x = {}; ExceptionInstance(x).exception is x
    True

    >>> hasattr(ExceptionInstance('anything'), 'value')
    False

    '''
    __slots__ = ()

    # Deliberately not providing a value attribute.

    @property
    def exception(self):
        return self[0]


class Args(tuple):

    '''

    >>> Args()
    Args(argv=(), kwargs={})

    # TODO: Yuck.  In Python3 this fails intermittently.
    # >>> Args(1, 2, a=3, b=4)
    # Args(argv=(1, 2), kwargs={'a': 3, 'b': 4})

    >>> Args(1, 2, a=3, b=4) == ((1, 2), dict(a=3, b=4))
    True

    >>> Args(2, 2)(lambda a, b: a + b)
    4

    >>> Args(a=1, b=2)(dict) == dict(a=1, b=2)
    True


    >>> Args(2, 2).try_call(lambda a, b: a + b)
    ReturnValue(4)

    '''

    __slots__ = ()

    def __new__(cls, *argv, **kwargs):

        return tuple.__new__(cls, (argv, kwargs))

    @property
    def argv(self):
        return self[0]

    @property
    def kwargs(self):
        return self[1]


    def __call__(self, fn):

        return fn(*self.argv, **self.kwargs)

    # TODO: Fix __repr__.
    def __repr__(self):

        return 'Args(argv=%r, kwargs=%r)' % self

    def try_call(self, fn):

        return try_apply(fn, *self)



class ReturnTest(object):


    def __init__(self, _expect, *argv, **kwargs):

        self._expect = _expect
        self._args = Args(*argv, **kwargs)

    def __call__(self, fn):
        '''Test that when called the function returns expected value.'''

        result =  self._args.try_call(fn)

        if result.exception:
            return ValueExpected(self._expect, result.exception)

        if result.value != self._expect:
            return WrongValue(self._expect, result.value)

        return None


class RaiseTest(object):


    def __init__(self, _expect, *argv, **kwargs):

        self._expect = _expect
        self._args = Args(*argv, **kwargs)

    def __call__(self, fn):
        '''Test that when called the function raises expected exception.'''

        result =  self._args.try_call(fn)

        if isinstance(result.exception, self._expect):
            return None

        if result.exception:
            return WrongException(self._expect, result.exception)

        return ExceptionExpected(self._expect, result.value)



def returns(_expect, *argv, **kwargs):
    '''
    Side-effect only decorator.
    '''
    expect = _expect

    def next(fn):
        actual = fn(*argv, **kwargs)
        if actual != expect:
            print(actual, expect)
        return fn

    return next


if 0 and __name__ == '__main__':


    # Decorator syntax.
    @returns(4, 2, 2)
    def plus(a, b):
        return a + b

    # Direct syntax.
    returns(4, 2, 2)(plus)

    assert ReturnValue(1) == (1,)
    assert type(ReturnValue(1)) is ReturnValue


    print(Args(1, 2, 3, d=4, e=5))

    print(Args(1, 2).apply(plus))
    print(Args(1, '').apply(plus))


if __name__ == '__main__':

    import doctest
    doctest.testmod(optionflags=doctest.ELLIPSIS)


    print('OK')
