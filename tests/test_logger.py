import unittest
from smartmirror import Logger


class TestLogger(unittest.TestCase):
    def test_init_logger(self):
        self.assertEqual(Logger.init_logger(outIntoFile=False), 0)
    def test_init_logger_one_instance(self):
        self.assertEqual(Logger.init_logger(outIntoFile=False), -1)

if __name__ == '__main__':
    unittest.main()
