import ast

from alib.asttools import get_statement_lists
from alib.asttools import iter_statements

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

# TODO: This teset is a bit ugly.
get_statement_lists(ast.BinOp()) == () # No statements - no lists.
[
    s[i].lineno
    for s, i
    in iter_statements( ast.parse(IF))
] == [1, 2, 4]                  # Powers of two, as it happens.
