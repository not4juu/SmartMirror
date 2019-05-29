from speech_recognition import Recognizer, Microphone
from speech_recognition import RequestError, UnknownValueError
from smartmirror.glo_messages import GLO_MSG
from smartmirror.glo_commands import GLO_CMD
from smartmirror.glo_commands import GET_COMMAND
from smartmirror.api_state import ApiState
import smartmirror.Logger as Logger
"""
    Command Recognition Class
"""


class CommandsRecognition(ApiState):

    def __init__(self):
        super().__init__()
        self.command = None
        self.command_detected = False
        self.listen_thread = None
        self.language = "pl-PL"

        try:
            self.recognizer = Recognizer()
            self.microphone = Microphone()
            """
                adjust the recognizer sensitivity to ambient noise and record audio
                from the microphone
            """
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source)

        except OSError as ose_err:
            Logger.logging.critical("OSError: {0}".format(ose_err))
            self.api_runs = False
            self.api_info = GLO_MSG['MICROPHONE_FAILURE']
            return
        except Exception as err:
            Logger.logging.critical("Exception: {0}".format(err))
            self.api_runs = False
            self.api_info = GLO_MSG['MICROPHONE_FAILURE']
            return
        self.api_info = GLO_MSG['MICROPHONE_INITIALIZED']

    def get_command(self):
        return self.command

    def is_command_detected(self):
        return self.command_detected

    def clear(self):
        self.command = None
        self.command_detected = False

    def validate_command(self, command):
        if command.lower() in GLO_CMD.values():
            self.command = GET_COMMAND(command.lower())
            self.command_detected = True
            Logger.logging.info("GLO_CMD command available -> {0}".format(command.lower()))
        else:
            Logger.logging.info("Detected command: {0}".format(command.lower()))
        return

    def callback_recognition(self, recognizer, audio):
        try:
            command = self.recognizer.recognize_google(audio, language=self.language)
            self.validate_command(command)
        except UnboundLocalError as err:
            Logger.logging.warning("UnboundLocalError : {0} ".format(err))
        except RequestError as err:
            Logger.logging.warning("RequestError : {0} ".format(err))
        except UnknownValueError as err:
            Logger.logging.warning("UnknownValueError : {0} ".format(err))
        return

    def background_listen(self):
        self.listen_thread = self.recognizer.listen_in_background(
            source=self.microphone, callback=self.callback_recognition, phrase_time_limit=5)


if __name__ == "__main__":
    pass
