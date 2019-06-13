import unittest
from smartmirror.api_state import ApiState
from smartmirror.glo_messages import GLO_MSG


class TestApiState(unittest.TestCase):

    def test_class_object(self):
        obj = ApiState()
        self.assertEqual(type(obj), ApiState)

    def test_init_api_state(self):
        obj = ApiState()
        self.assertEqual(obj.api_runs, True)
        self.assertEqual(obj.api_info, GLO_MSG['NO_ERROR'])

    def test_api_state(self):
        obj = ApiState()
        obj.api_runs = False
        obj.api_info = "test"
        self.assertEqual(obj.api_runs, False)
        self.assertEqual(obj.api_info, "test")


if __name__ == '__main__':
    unittest.main()
