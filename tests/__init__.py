import unittest

from tests.test_logger import TestLogger

def all_tests():
    test_suite = unittest.TestSuite()
    test_suite.addTest(unittest.makeSuite(TestLogger))
    return test_suite


if __name__ == '__main__':
    runner = unittest.TextTestRunner ()
    runner.run(all_tests())
