from threading import Thread
from smartmirror.glo_messages import GLO_MSG
from smartmirror.glo_messages import GET_MESSAGE
from smartmirror.api_window import ApiWindow
from smartmirror.network import Network
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
        Logger.logging.debug("Initialization of User Interface Thread class")

    def init_window(self):
        self.api_window = ApiWindow()
        Logger.logging.debug("Command recognition class state: {0}".format(
            GET_MESSAGE(self.api_window.api_info)))
        self.MessagesHandler.send_message(self.api_window.api_info)

    def network_connection(self):
        if Network.enabled():
            self.api_window.display_wifi_enable()
        else:
            self.close_thread = False
        self.MessagesHandler.send_message(Network.get_status())

    def run_api_window(self):
        if not self.api_window.api_runs:
            self.close_thread = True
            Logger.logging.debug("Close thread : \"{0}\"".format(
                GET_MESSAGE(self.api_window.api_info)))
            self.MessagesHandler.send_message(self.api_window.api_info)
        self.api_window.refresh()

    def run_messages_handler(self):
        handler = {
            GLO_MSG['MICROPHONE_FAILURE']: self.handler_microphone_failure,
            GLO_MSG['MICROPHONE_INITIALIZED']: self.handler_microphone_initialized,
            GLO_MSG['DISPLAY_WEATHER']: self.handler_display_weather,
            GLO_MSG['DISPLAY_DATE']: self.handler_display_date,
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
        self.api_window.display_microphone_enable()

    def handler_display_weather(self):
        pass

    def handler_display_date(self):
        pass

    def handler_display_clock(self):
        self.api_window.display_clock()

    def handler_hide_clock(self):
        self.api_window.hide_clock()

    def run(self):
        Logger.logging.debug("User_Interface thread runs")
        self.init_window()
        self.network_connection()
        while not self.close_thread:
            self.run_api_window()
            self.run_messages_handler()
        Logger.logging.debug("User_Interface thread ends")


if __name__ == "__main__":
    pass
