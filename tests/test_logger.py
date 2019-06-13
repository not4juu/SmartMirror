import unittest
from smartmirror.Logger import Logger, init_logger


class TestLogger(unittest.TestCase):

    def test_init_logger(self):
        self.assertEqual(init_logger(logs_to_file=False), 0)

    def test_init_logger_one_instance(self):
        self.assertEqual(init_logger(logs_to_file=False), -1)

    def test_info_print(self):
        self.assertEqual(Logger.info("Test"), None)


if __name__ == '__main__':
    unittest.main()
