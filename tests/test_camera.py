import unittest
from smartmirror.camera import Camera


class TestCamera(unittest.TestCase):

    def test_class_object(self):
        obj = Camera()
        self.assertEqual(type(obj), Camera)

    def test_camera_state(self):
        obj = Camera()
        obj.api_runs = False
        self.assertEqual(obj.api_runs, False)
        self.assertEqual(obj.get_status(), False)
        self.assertEqual(obj.get_camera(), None)


if __name__ == '__main__':
    unittest.main()
