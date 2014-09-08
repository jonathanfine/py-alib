from alib.script import Script

# Here's a dummy log, for testing Script.
class DummyEvaluator:

    def __init__(self):
        self.store = []

    def compare(self, *argv):
        # TODO: What is it that we are discarding here, and why?
        self.store.append(argv[-1:]) # Discard local and global dicts.

# Create and run a script.
s = Script('2 + 2 == 5;2 < 4')
[c[1] for c in s.code_store] == [['Eq'], ['Lt']])


evaluator = DummyEvaluator()
s.run(evaluator)

# Now check the output is as expected.
# TODO: Start counting at 0 or at 1? System or user?
evaluator.store[0] == (1,) # First test.
evaluator.store[1] == (2,) # Second test.
