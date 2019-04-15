from threading import Thread
from api_window import ApiWindow
from network import Network
import  Logger
"""
    User Interface Thread
"""

class UiThread(Thread):

    def __init__(self,messages_handler):
        Thread.__init__(self, name="UI_Thread")
        self.__MessagesHandler = messages_handler

        self.__close_thread = not Network.enabled()
        self.__MessagesHandler.send_message(Network.get_status())

        self.__window = None
        Logger.logging.debug("Initialized user interface thread")

    def __run_messages_handler(self):
        handler = {
            'MICROPHONE_FAILURE': self.__h_microphone_failure,
            'MICROPHONE_INITIALIZED': self.__h_microphone_initialized,
        }
        message = self.__MessagesHandler.get_message()
        if message is None:
            return message
        call_handler = handler.get(message,
                                    lambda: self.__MessagesHandler.send_message_again(message))
        call_handler()

    def __h_microphone_failure(self):
        self.__close_thread = True
        return

    def __h_microphone_initialized(self):
        return


    def __init_window(self):
        self.__window = ApiWindow()
        Logger.logging.debug ("Command recogniton class state: {0}".format(
            self.__window.get_state_info()
        ))
        self.__MessagesHandler.send_message(self.__window.get_state_info())
        return

    def __run_window(self):
        if not self.__window.api_state_ok():
            self.__close_thread = True
            Logger.logging.debug("Close user interface thread : \"{0}\"".format(
                self.__window.get_state_info())
            )
            self.__MessagesHandler.send_message(self.__window.get_state_info())
        self.__window.refresh()
        return

    def run(self):
        Logger.logging.debug("User_Interface thread runs")
        self.__init_window()

        while not self.__close_thread:
            self.__run_window()
            self.__run_messages_handler()

        Logger.logging.debug ("User_Interface thread ends")


