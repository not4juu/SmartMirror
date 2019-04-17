from smartmirror.glo_messages import GLO_MSG
from smartmirror.glo_messages import GET_MESSAGE
from smartmirror.api_command_recognition import  CommandRecognition
from threading import Thread
import Logger
"""
    User Command Thread
"""

class UcThread(Thread):

    def __init__(self,messages_handler):
        Thread.__init__(self, name="UC_Thread")
        self.__MessagesHandler = messages_handler
        self.__close_thread = False

        self.__network_initialized = False
        self.__window_initialized = False
        Logger.logging.debug("Initialized user command thread")

    def __init_command_recognition(self):
        Logger.logging.debug ("Initialize command recogniton class")
        self.__command_recognition = CommandRecognition()
        if not self.__command_recognition.api_runs:
            self.__close_thread = True

        Logger.logging.debug ("Command recogniton class state: {0}".format (
            GET_MESSAGE(self.__command_recognition.api_info)
        ))
        self.__MessagesHandler.send_message(self.__command_recognition.api_info)


    def __run_messages_handler(self):
        handler = {
            GLO_MSG['NETWORK_CONNECTION_FAILURE']: self.__h_api_window_close,
            GLO_MSG['API_CAMERA_CONNECTION_FAILURE']: self.__h_api_window_close,
            GLO_MSG['API_USER_QUIT']: self.__h_api_window_close,
            GLO_MSG['NETWORK_CONNECTION_SUCCESS']: self.__h_network_success,
            GLO_MSG['API_WINDOW_INITIALIZED']: self.__h_window_success,
        }
        message_id = self.__MessagesHandler.get_message()
        if message_id is None:
            return message_id
        call_handler = handler.get(message_id,
                                    lambda: self.__MessagesHandler.send_message_again(message_id))
        call_handler()

    def __h_network_success(self):
        self.__network_initialized = True
        return
    def __h_window_success(self):
        self.__window_initialized = True
        return

    def __h_api_window_close(self):
        Logger.logging.debug("Close user command thread")
        self.__close_thread = True
        return


    def __wait_for_ui_init(self):
        Logger.logging.debug ("Wait for init network and window")
        def ui_initialized():
            return self.__window_initialized and self.__network_initialized

        while not (ui_initialized() or self.__close_thread):
            self.__run_messages_handler()

        if ui_initialized():
            self.__init_command_recognition()

    def run(self):
        Logger.logging.debug("User_Command thread runs")
        self.__wait_for_ui_init()
        while not self.__close_thread:
            self.__run_messages_handler()
        Logger.logging.debug ("User_Command thread ends")

if __name__ == "__main__":
    pass