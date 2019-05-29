from smartmirror.glo_messages import GLO_MSG
from smartmirror.glo_messages import GET_MESSAGE
from smartmirror.api_window import ApiWindow
from smartmirror.network import Network
from threading import Thread
import smartmirror.Logger as Logger
"""
    User Interface Thread
"""

class UiThread(Thread):

    def __init__(self,messages_handler):
        Thread.__init__(self, name="UI_Thread")
        self.__MessagesHandler = messages_handler

        self.__close_thread = False
        self.__window = None
        Logger.logging.debug("Initialized user interface thread")

    def __run_messages_handler(self):
        handler = {
            GLO_MSG['MICROPHONE_FAILURE']: self.__h_microphone_failure,
            GLO_MSG['MICROPHONE_INITIALIZED']: self.__h_microphone_initialized,
            GLO_MSG['DISPLAY_WEATHER']: self.__h_display_weather,
            GLO_MSG['DISPLAY_DATE']: self.__h_display_date,
            GLO_MSG['DISPLAY_CLOCK']: self.__h_display_clock,
            GLO_MSG['HIDE_CLOCK']: self.__h_hide_clock,
        }
        message_id = self.__MessagesHandler.get_message()
        if message_id is None:
            return None
        call_handler = handler.get(message_id,
                                    lambda: self.__MessagesHandler.send_message_again(message_id))
        call_handler()

    def __h_microphone_failure(self):
        self.__close_thread = True
        return

    def __h_microphone_initialized(self):
        self.__window.display_microphone_enable()
        return

    def __h_display_weather(self):
        return

    def __h_display_date(self):
        return

    def __h_display_clock(self):
        self.__window.display_clock();
        return

    def __h_hide_clock(self):
        self.__window.hide_clock();
        return

    def __init_window(self):
        self.__window = ApiWindow()
        Logger.logging.debug("Command recogniton class state: {0}".format(
            GET_MESSAGE(self.__window.api_info)
        ))
        self.__MessagesHandler.send_message(self.__window.api_info)
        return

    def __network_connection(self):
        if Network.enabled():
            self.__window.display_wifi_enable()
        else:
            self.__close_thread = False
        self.__MessagesHandler.send_message(Network.get_status())
        return

    def __run_window(self):
        if not self.__window.api_runs:
            self.__close_thread = True
            Logger.logging.debug("Close user interface thread : \"{0}\"".format(
                GET_MESSAGE(self.__window.api_info))
            )
            self.__MessagesHandler.send_message(self.__window.api_info)
        self.__window.refresh()
        return

    def run(self):
        Logger.logging.debug("User_Interface thread runs")
        self.__init_window()
        self.__network_connection()

        while not self.__close_thread:
            self.__run_window()
            self.__run_messages_handler()

        Logger.logging.debug("User_Interface thread ends")


if __name__ == "__main__":
    pass
