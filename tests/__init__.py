import unittest
from tests.test_logger import TestLogger
from tests.test_api_state import ApiState
from tests.test_camera import TestCamera
"""
TODO: check if all suites all runs
"""


def all_tests():
    test_suite = unittest.TestSuite()
    test_suite.addTest(unittest.makeSuite(TestLogger))
    test_suite.addTest(unittest.makeSuite(ApiState))
    test_suite.addTest(unittest.makeSuite(TestCamera))
    return test_suite


if __name__ == '__main__':
    runner = unittest.TextTestRunner ()
    runner.run(all_tests())
    pass