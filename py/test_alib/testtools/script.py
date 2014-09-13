from alib.testtools.script import Script

# Here's a dummy log, for testing Script.
class DummyEvaluator:

    def __init__(self):
        self.store = []

    def run_test(self, *argv):
        # TODO: What is it that we are discarding here, and why?
        # TODO: Test the key apppend to the store.
        self.store.append(argv[-1:]) # Discard key, local and global dicts.

# Create and run a script.
s = Script('2 + 2 == 5;2 < 4')
[c[0] for c in s.code_store] == ['compare', 'compare']
# c[1] is the code objects.
[c[2] for c in s.code_store] == [['Eq'], ['Lt']]

# TODO: Reinstate or remove these tests.
# evaluator = DummyEvaluator()
# s.run(evaluator)

# # Now check the output is as expected.
# # TODO: Start counting at 0 or at 1? System or user?
# # TODO: Not obvious what this test does.
# evaluator.store[0] == (0,) # First test.
# evaluator.store[1] == (1,) # Second test.
