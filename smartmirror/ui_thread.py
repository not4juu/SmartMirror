from threading import Thread
from smartmirror.glo_messages import GLO_MSG
from smartmirror.glo_messages import GET_MESSAGE
from smartmirror.api_window import ApiWindow
from smartmirror.authorization import Authorization
from smartmirror.camera import Camera
from smartmirror.network import Network
from smartmirror.speaker import Speaker
from smartmirror.Logger import Logger

"""
    User Interface Thread
"""


class UiThread(Thread):
    def __init__(self, messages_handler):
        Thread.__init__(self, name="UI_Thread")
        self.MessagesHandler = messages_handler
        self.close_thread = False

        self.api_window = None
        self.camera = None
        self.speaker = None

        self.authorization_complete = False
        self.authorized_user_name = ""
        self.quit_authorization = False
        Logger.debug("Initialization of User Interface Thread class")

    def init_window(self):
        self.api_window = ApiWindow()
        if not self.api_window.api_runs:
            self.close_thread = True

        self.MessagesHandler.send_message(self.api_window.api_info)
        self.init_speaker()

    def init_speaker(self):
        self.speaker = Speaker()

    def init_camera(self):
        self.camera = Camera()
        if self.camera.get_status() is self.camera.Enabled:
            self.api_window.display_camera(enable_camera=True)
        else:
            self.api_window.display_camera(enable_camera=False)

        self.MessagesHandler.send_message(self.camera.api_info)

    def authorization_callback(self, name):
        self.authorized_user_name = name
        self.authorization_complete = True
        Logger.info("User authorized as: {0}".format(self.authorized_user_name))

    """
        Authorization functions
    """
    def start_authorization(self):
        self.api_window.start_pulse_text("Autoryzacja")
        self.auth = Authorization(self.camera.get_camera(), self.authorization_callback)
       # self.auth.run(method='opencv_face_recognition', debug=False)
        self.auth.run(method='dlib_face_recognition', debug=False)
        Logger.debug("Start authorization process")

    def stop_authorization(self):
        self.auth.stop()
        self.api_window.stop_pulse_text()
        Logger.debug("Stop authorization process")
        if self.authorization_complete:
            self.speaker.say("Witaj w inteligentnym lustrze {0}".format(self.authorized_user_name))
            self.api_window.user_view(name=self.authorized_user_name, display=True)

    def run_authorization(self):
        if self.camera.api_runs:
            self.start_authorization()
            while not (self.authorization_complete or self.quit_authorization):
                self.run_api_window()
            self.stop_authorization()
            self.network_connection()
        else:
            Logger.error("Authorization process will not start when camera is not connected")
            self.api_window.start_pulse_text("Wymagana \nautoryzacja")

    def network_connection(self):
        if self.authorization_complete and not self.close_thread:
            if Network.enabled():
                self.api_window.init_network_dependency()
                self.api_window.display_wifi(enable_wifi=True)
                self.api_window.weather_view(display=True)
                self.api_window.news_view(display=True)
            else:
                self.api_window.display_wifi(enable_wifi=False)
            self.MessagesHandler.send_message(Network.get_status())

    def run_api_window(self):
        if self.api_window.api_runs:
            self.api_window.refresh()
        else:
            self.close_thread = True
            self.quit_authorization = True
            Logger.debug("Close thread : \"{0}\"".format(GET_MESSAGE(self.api_window.api_info)))
            self.MessagesHandler.send_message(self.api_window.api_info)

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
            GLO_MSG['LOGOUT']: self.handler_logout,
        }
        message_id = self.MessagesHandler.get_message()
        if message_id is None:
            return None
        call_handler = handler.get(
            message_id, lambda: self.MessagesHandler.send_message_again(message_id))
        Logger.debug(call_handler.__name__)
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

    def handler_logout(self):
        self.api_window.user_view(name="", display=False)
        self.api_window.weather_view(display=False)
        self.api_window.news_view(display=False)
        self.authorization_complete = False
        self.run_authorization()

    def run(self):
        Logger.info("User_Interface thread runs")
        self.init_window()
        self.init_camera()
        self.run_authorization()
        while not self.close_thread:
            self.run_api_window()
            self.run_messages_handler()
        Logger.info("User_Interface thread ends")


if __name__ == "__main__":
    pass
