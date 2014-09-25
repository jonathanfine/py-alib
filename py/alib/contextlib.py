from __future__ import absolute_import

__metaclass__ = type


class Suppressed:

    __slots__ = ['value']
    # TODO: Why can't I set cls.value = None?
    #    value = None

    def __init__(self):
        self.value = None


    def __bool__(self):

        return self.value is not None

    __nonzero__ = __bool__      # For Python 2.5, 2.6 and 2.7.


    def raise_if(self, excp_types):
        '''Raise self.value if instance of excp_types.'''

        # We assume that excp is either None or an exception.
        excp = self.value
        if excp and isinstance(excp, excp_types):
            raise excp


class Suppress:

    def __init__(self, reraise=()):

        self.reraise = reraise


    def __enter__(self):
        self.suppressed = Suppressed()
        return self.suppressed

    def __exit__(self, exc_type, exc_value, traceback):

        if exc_type is None:
            return False        # Nothing to suppress.

        if isinstance(exc_value, self.reraise):
            return False        # Don't suppress.

        # Still here? Then suppress the exception.
        self.suppressed.value = exc_value
        return True
