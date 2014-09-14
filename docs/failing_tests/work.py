# All these tests fail.

1 == 2
(1 + '2') == 3
2 < 2

ddt or True
False or ddt
(2 + 2) ** Exception
(1 + '2') ** ValueError
# TypeError: isinstance() arg 2 must be a class, type, or tuple of classes and types
# (1 + '2') ** 4

'd' in 'abc'
