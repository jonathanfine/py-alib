import ast

from ast import Compare
from ast import Eq
from ast import Expr
from ast import Expression

import marshal

a = ast.parse('f(3) == 10')

for line in a.body:

    if isinstance(line, Expr):
        print(line)

        value = line.value

        if isinstance(value, Compare):
            print(value)

            ops = value.ops

            if len(ops) == 1 and isinstance(ops[0], Eq):

                print('bingo')
                left = value.left
                right = value.comparators[0]
                print(left, right)

                left = compile(Expression(left), '', 'eval')
                right = compile(Expression(right), '', 'eval')


print(eval(left, dict(f=lambda x: x**2)))
print(eval(right))


def g(x):
    return x + 1

# Grouping tests, bail out on first failure.
# Could support dictlist syntax aaa(bbb=3)[ ... ]
[
    g(3) == 2,
    g(4) == 7,
    g(9) == 11,
    g(12) == 24,
]
