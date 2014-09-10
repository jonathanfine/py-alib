import itertools
import operator

# TODO: Migrate to alib.itertools (perhaps).
# TODO: Provide tests.
repeat_empty_tuple = itertools.repeat(())

def attrgettertuple(names):
    '''Always returns a tuple, whatever the length of argv.'''

    n = len(names)
    if n == 0:
        return repeat_empty_tuple
    getter = operator.attrgetter(*names)
    if n == 1:
        return lambda x: (getter(x),)
    else:
        return getter


# Not found an Python asdl parse I can use - need to build by hand
# what I need.  Doesn't take long.  Easier to do by hand than to write
# and test a program to do this.

BODY_TYPES = [
    # (<Name>, <stmt* fields>).

    ('Module', 'body'),
    ('Interactive', 'body'),
    ('Suite', 'body'),
    ('FunctionDef', 'body'),
    ('ClassDef', 'body'),

    ('For', 'body', 'orelse'),
    ('While', 'body', 'orelse'),
    ('If', 'body', 'orelse'),

    ('With', 'body'),

    ('Try', 'body', 'orelse', 'finalbody'), # Python 3 only.
    ('TryExcept', 'body', 'orelse'), # Python 2.6 and 2.7 only.
    ('TryFinally', 'body', 'finalbody'), # Python 2.6 and 2.7 only.
]

BODY_TYPE_LOOKUP = dict(
    (bt[0], attrgettertuple(bt[1:]))
    for bt in BODY_TYPES
)

def get_statement_lists(node):
    '''Return tuple of the statement lists for the node.'''

    key = type(node).__name__
    fn = BODY_TYPE_LOOKUP.get(key)
    return fn(node) if fn else ()
