from alib.contextlib import Suppress
from alib.contextlib import Suppressed

# These tests pass.  They are fairly clear.  Could wrap in function in
# case unwanted exceptions wreck the rest of the tests.
with Suppress() as suppressed:
   raise ValueError
bool(suppressed) is True

with Suppress() as suppressed:
    pass
bool(suppressed) is False

# Here's a way to run tests that raise an exception. They also provide
# for more compact writing of tests.

# This is a function definition, so must succeed (unless SyntaxError).
# TODO: Is it better to supply and use default values?
# TODO: Is it better to wrap this in a try_call or similar?  Then we
# are sure to get a result, which we can examine at our leisure.
# If we do this, perhaps we avoid the ** notation.
def doit(an_exception, reraise):

    with Suppress(reraise) as suppressed:
        if an_exception:
            raise an_exception

    return suppressed

# If no exception raised,  nothing is suppressed.
bool(doit(None, ())) is False
bool(doit(None, Exception)) is False

# If exception raised, something is suppressed.
exception = ValueError('Something went wrong')
bool(doit(exception, ())) is True

# The suppressed.value is the exception.
suppressed = doit(exception, ())
suppressed.value is exception

# In both cases we get an instance of Suppressed.  But if no exception
# is raised then as a boolean it is false.
type(suppressed) is Suppressed
type(doit(None, ())) is Suppressed

# Here a TypeError is re-raised.
doit(TypeError, TypeError) ** TypeError
doit(TypeError, Exception) ** TypeError
doit(TypeError, (TypeError, ValueError)) ** TypeError




