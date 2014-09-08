from alib.script import Script

# Here's a dummy log, for testing Script.
class DummyEvaluator:

    def __init__(self):
        self.store = []

    def compare(self, *argv):
        # TODO: What is it that we are discarding here, and why?
        self.store.append(argv[2:]) # Discard local_dict.

# Create and run a script.
s = Script('2 + 2 == 5')
evaluator = DummyEvaluator()
s.run(evaluator)

# Now check the output is as expected.
data = evaluator.store[0]
data[1] == ['Eq']
data[2] == [compile(s, '', 'eval') for s in ('2 + 2', '5')]
