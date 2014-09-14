Alib provides simple testing without boilerplate.  For example, if
*myfile.py* contains the line::

     7 * 8 == 54  # I'm not sure about this!

then running::

    $ python -m alib.test myfile.py

will, because the test fails, report the test line and the nature of
the failure::

    line 3:  7 * 8 == 54  # I'm not sure about this!
    (['Eq'], [ReturnValue(56), ReturnValue(54)])

Exceptions are caught.  The input line::

    (1 + '2') == 3  # Can we add a string to a number?

produces::

    line 4:  (1 + '2') == 3  # Can we add a string to a number?
    (['Eq'], [ExceptionInstance(TypeError), ReturnValue(3)]

This test line succeeds (because the left hand side raises the right
hand side).::

    (1 + '2') ** TypeError  # We can't add a string to a number.

To test all Python files in the folder *path/to/mydir* run the command::

    $ python -m alib.test path/to/mydir
