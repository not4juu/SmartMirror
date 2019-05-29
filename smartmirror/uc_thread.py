from threading import Thread
from smartmirror.glo_messages import GLO_MSG
from smartmirror.glo_messages import GET_MESSAGE
from smartmirror.commands_recognition import CommandsRecognition
import smartmirror.Logger as Logger
"""
    User Command Thread
"""


class UcThread(Thread):

    def __init__(self, messages_handler):
        Thread.__init__(self, name="UC_Thread")
        self.MessagesHandler = messages_handler
        self.close_thread = False
        self.network_enabled = False
        self.window_enabled = False
        self.command_recognition = None
        Logger.logging.debug("Initialization of User Command Thread class")

    def wait_for_ui_init(self):
        Logger.logging.debug("Wait for init network and window")

        def ui_initialized():
            return self.window_enabled and self.network_enabled

        while not (ui_initialized() or self.close_thread):
            self.run_messages_handler()

        if ui_initialized():
            self.init_command_recognition()

    def init_command_recognition(self):
        Logger.logging.debug("Init command recognition")
        self.command_recognition = CommandsRecognition()
        if self.command_recognition.api_runs:
            self.command_recognition.background_listen()
        else:
            self.close_thread = True

        Logger.logging.debug("Command recognition class state: {0}".format(
            GET_MESSAGE(self.command_recognition.api_info)
        ))
        self.MessagesHandler.send_message(self.command_recognition.api_info)

    def run_command_detection(self):
        if self.command_recognition.is_command_detected():
            self.MessagesHandler.send_message(self.command_recognition.get_command())
            self.command_recognition.clear()

    def run_messages_handler(self):
        handler = {
            GLO_MSG['NETWORK_CONNECTION_FAILURE']: self.handler_api_window_close,
            GLO_MSG['API_CAMERA_CONNECTION_FAILURE']: self.handler_api_window_close,
            GLO_MSG['API_USER_QUIT']: self.handler_api_window_close,
            GLO_MSG['NETWORK_CONNECTION_SUCCESS']: self.handler_network_success,
            GLO_MSG['API_WINDOW_INITIALIZED']: self.handler_window_success,
        }
        message_id = self.MessagesHandler.get_message()
        if message_id is None:
            return message_id
        call_handler = handler.get(
            message_id, lambda: self.MessagesHandler.send_message_again(message_id))
        call_handler()

    def handler_network_success(self):
        self.network_enabled = True
        return

    def handler_window_success(self):
        self.window_enabled = True
        return

    def handler_api_window_close(self):
        Logger.logging.debug("Close user command thread")
        self.close_thread = True
        return

    def run(self):
        Logger.logging.debug("User_Command thread runs")
        self.wait_for_ui_init()
        while not self.close_thread:
            self.run_command_detection()
            self.run_messages_handler()
        Logger.logging.debug("User_Command thread ends")


if __name__ == "__main__":
    pass
