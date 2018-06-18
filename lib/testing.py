import os.path
import inspect
import unittest

import lib.subclass


def test():
    tests = []

    root_dir = os.path.realpath(
        os.path.join(
            os.path.dirname(__file__),
            '..',
            '..'
        )
    )

    # Find all unit tests
    for subclass in lib.subclass.walk(unittest.TestCase):
        if root_dir in inspect.getfile(subclass):
            for test in unittest.TestLoader().loadTestsFromTestCase(subclass):
                tests.append(test)

    unittest.TextTestRunner(verbosity=2).run(
        unittest.TestSuite(tests)
    )

