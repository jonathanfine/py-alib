'''Scratch work file

It's convenient when exploring to have tests and code in the same
file.

To run:
    $ python testtools/testit.py testtools/work.py
'''


# Just to warm up
2 + 2 == 4
(2 + '') ** TypeError



'{0:b}'.format(1) == '1'
'{0:b>2}'.format(1) == 'b1'

'{0:>2}'.format(1) == ' 1'
'{0:x>2}'.format(1) == 'x1'


'{0:>>2}'.format(1) == '>1'
'{0:{1}>2}'.format(1, 'X') == 'X1'
'{0:{1}>2}'.format(1, '{') == '{1'
'{0:{1}>2}'.format(1, 'XX') ** ValueError


# Here's a way to reduce boilerplate.
def fn(s, v):
    return s.format(v)

fn('{a}', 'a') ** KeyError
'{0b}'.format(10) ** KeyError
fn('{0:>2}', 1) == ' 1'

type('{0b}'.format) == type(len) # No exception.

# Here's another way to reduce boilerplate.
def pairs_from_iter(items):

    iterator = iter(items)
    while 1:
        yield next(iterator), next(iterator)

list(pairs_from_iter(range(6))) == [(0, 1), (2, 3), (4, 5)]

def triples_from_iter(items):

    iterator = iter(items)
    while 1:
        yield next(iterator), next(iterator), next(iterator)


# Here's a nice way to do a data loop.
for s, v, e in triples_from_iter([
        # Compare to the not much longer:
        # fn('{0}', 'a') == 'a'
        # fn('{a}', 'a') ** KeyError
        # This data loop not helping with clarity.
        #
        # Providing external fn allows test to be exported.  But this
        # works both ways.
        '{0}', 'a', 'a',
        '{0}', 10, '10',
        '{0:d}', 10, '10',
        '{0:b}', 10, '1010',
        '{0:x}', 10, 'a',
        '{0:X}', 10, 'A',
        ]):
    s.format(v) == e


# TODO: Would like this to be run as a test.  We see up from what's
# going to happen to the data.
[
    s.format(v) == e
    for s, v, e in triples_from_iter([
            '{0}', '', 'a',
            ])
    ]
