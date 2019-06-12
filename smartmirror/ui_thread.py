from threading import Thread
from smartmirror.glo_messages import GLO_MSG
from smartmirror.glo_messages import GET_MESSAGE
from smartmirror.api_window import ApiWindow
from smartmirror.network import Network
from smartmirror.authorization import Authorization
from smartmirror.camera import Camera
import smartmirror.Logger as Logger

"""
    User Interface Thread
"""


class UiThread(Thread):
    def __init__(self, messages_handler):
        Thread.__init__(self, name="UI_Thread")
        self.MessagesHandler = messages_handler
        self.close_thread = False
        self.api_window = None
        self.authorization_complete = False
        self.user_name = ""
        self.camera = None
        Logger.logging.debug("Initialization of User Interface Thread class")

    def init_window(self):
        self.api_window = ApiWindow()
        if not self.api_window.api_runs:
            self.close_thread = True
        self.MessagesHandler.send_message(self.api_window.api_info)

    def init_camera(self):
        self.camera = Camera()
        self.MessagesHandler.send_message(self.camera.api_info)
        if self.camera.get_status() is self.camera.Enabled:
            self.api_window.display_camera(enable_camera=True)
        else:
            self.api_window.display_camera(enable_camera=False)

    def authorization_callback(self, name):
        self.user_name = name
        self.authorization_complete = True
        Logger.logging.debug("User authorized as: {0}".format(self.user_name))

    """
        Authorization functions
    """
    def start_authorization(self, authorization_callback):
        self.api_window.start_pulse_text("Authorization")
        self.auth = Authorization(self.camera.get_camera(), authorization_callback)
        self.auth.run(method='opencv_face_recognition', debug=False)
        #self.auth.run(method='dlib_face_recognition', debug=True)
        Logger.logging.debug("Api Window start authorization process")

    def stop_authorization(self):
        self.auth.stop()
        self.api_window.stop_pulse_text()
        Logger.logging.debug("Api Window stop authorization process")
        self.api_window.user_view(name=self.user_name, display=True)

    def verify_access(self):
        if self.camera.api_runs:
            self.start_authorization(self.authorization_callback)
            while not self.authorization_complete:
                self.run_api_window()
            self.stop_authorization()
        else:
            Logger.logging.error("Authorization process will not start when camera is not connected")
            self.api_window.start_pulse_text("Authorization \n Required !")

    def network_connection(self):
        if self.authorization_complete:
            if Network.enabled():
                self.api_window.init_network_dependency()
                self.api_window.display_wifi(enable_wifi=True)
            self.MessagesHandler.send_message(Network.get_status())

    def run_api_window(self):
        if not self.api_window.api_runs:
            self.close_thread = True
            self.authorization_complete = True
            Logger.logging.debug("Close thread : \"{0}\"".format(
                GET_MESSAGE(self.api_window.api_info)))
            self.MessagesHandler.send_message(self.api_window.api_info)
        self.api_window.refresh()

    def run_messages_handler(self):
        handler = {
            GLO_MSG['MICROPHONE_FAILURE']: self.handler_microphone_failure,
            GLO_MSG['MICROPHONE_INITIALIZED']: self.handler_microphone_initialized,
            GLO_MSG['DISPLAY_WEATHER']: self.handler_display_weather,
            GLO_MSG['HIDE_WEATHER']: self.handler_hide_weather,
            GLO_MSG['DISPLAY_NEWS']: self.handler_display_news,
            GLO_MSG['HIDE_NEWS']: self.handler_hide_news,
            GLO_MSG['DISPLAY_CLOCK']: self.handler_display_clock,
            GLO_MSG['HIDE_CLOCK']: self.handler_hide_clock,
        }
        message_id = self.MessagesHandler.get_message()
        if message_id is None:
            return None
        call_handler = handler.get(
            message_id, lambda: self.MessagesHandler.send_message_again(message_id))
        Logger.logging.debug(call_handler.__name__)
        call_handler()

    def handler_microphone_failure(self):
        self.close_thread = True

    def handler_microphone_initialized(self):
        self.api_window.display_microphone(enable_microphone=True)

    def handler_display_weather(self):
        self.api_window.weather_view(display=True)

    def handler_hide_weather(self):
        self.api_window.weather_view(display=False)

    def handler_display_news(self):
        self.api_window.news_view(display=True)

    def handler_hide_news(self):
        self.api_window.news_view(display=False)

    def handler_display_clock(self):
        self.api_window.clock_view(display=True)

    def handler_hide_clock(self):
        self.api_window.clock_view(display=False)

    def run(self):
        Logger.logging.debug("User_Interface thread runs")
        self.init_window()
        self.init_camera()
        self.verify_access()
        self.network_connection()
        while not self.close_thread:
            self.run_api_window()
            self.run_messages_handler()
        Logger.logging.debug("User_Interface thread ends")


if __name__ == "__main__":
    pass
