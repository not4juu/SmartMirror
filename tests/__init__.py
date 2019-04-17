import unittest
from tests.test_logger import TestLogger
from tests.test_api_state import ApiState
"""
TODO: check if all suites all runs
"""
def all_tests():
    test_suite = unittest.TestSuite()
    test_suite.addTest(unittest.makeSuite(TestLogger))
    test_suite.addTest(unittest.makeSuite(ApiState))
    return test_suite


if __name__ == '__main__':
    runner = unittest.TextTestRunner ()
    runner.run(all_tests())
    pass