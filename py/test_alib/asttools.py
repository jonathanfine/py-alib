import ast

from alib.asttools import get_statement_lists
from alib.asttools import iter_statements
from alib.asttools import replace
from alib.pending import Link_i_i

__metaclass__ = type

'body' in ast.If()._fields      # Gotcha - ast.If() has body?
ast.If().body ** AttributeError # Gotcha - has no body.

# Produce a real if node for testing.
IF = '''\
if a:
   345
else:
   456
'''
If_node = ast.parse(IF).body[0]

# TODO: This test is a bit ugly.  Please fix.
If_node.body is not None
If_node.orelse is not None

# Get the statement lists.
sl = get_statement_lists(If_node)

# Check the line numbers.
If_node.lineno == 1
sl[0][0].lineno == 2
sl[1][0].lineno == 4

len(sl) == 2

# TODO: Make this test easier to write and run.
get_statement_lists(ast.BinOp()) == () # No statements - no lists.
[
    s[i].lineno
    for s, i
    in iter_statements( ast.parse(IF))
] == [1, 2, 4]                  # Powers of two, as it happens.


# Smoke test.
tree = ast.parse(IF)
list(replace(tree, lambda x: None, ())) # Gotcha - need list.

# TODO: Make these tests easier to write and run.
tree = ast.parse(IF)
w = Link_i_i()

aaa = replace(tree, w.inspect, w.make_insertions())
list(aaa) == [1, 2, 4]

aaa = replace(tree, w.inspect, w.make_insertions())
list(aaa) == [4, 5, 7]
