import cv2
from smartmirror.glo_messages import GLO_MSG
from smartmirror.api_state import ApiState
from smartmirror.Logger import Logger


"""
    Camera Class

    - using a cv2 module enable a camera connection with device
"""


class Camera(ApiState):

    Enabled = True
    Disabled = False

    def __init__(self):
        super().__init__()
        self.camera = None
        self.api_runs = False

        self._camera_connection()

    def _camera_connection(self):
        Logger.debug("Find camera connection")
        try:
            self.camera = cv2.VideoCapture(0)
            if not self.camera.isOpened():
                raise NameError
        except cv2.error as exception:
            Logger.critical("OpenCV camera hardware problem: {0}".format(exception))
            self.api_info = GLO_MSG['API_CAMERA_CONNECTION_FAILURE']
            self.api_runs = self.Disabled
            return
        except Exception as exception:
            Logger.critical("Camera hardware is not connected: {0}".format(exception))
            self.api_info = GLO_MSG['API_CAMERA_CONNECTION_FAILURE']
            self.api_runs = self.Disabled
            return
        self.api_info = GLO_MSG['API_WINDOW_INITIALIZED']
        self.api_runs = self.Enabled
        return

    def get_status(self):
        return self.api_runs

    def get_camera(self):
        return self.camera if self.api_runs else None


if __name__ == "__main__":
    pass
