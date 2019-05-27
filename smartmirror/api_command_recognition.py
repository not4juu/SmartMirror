from smartmirror.glo_messages import GLO_MSG
from smartmirror.glo_commands import GLO_CMD
from smartmirror.glo_commands import GET_COMMAND
from smartmirror.api_state import ApiState
import smartmirror.Logger as Logger
import speech_recognition

class CommandRecognition(ApiState):

    def __init__(self):
        super().__init__ ()
        self.__command = self.__command_detected = False
        self.__listen_thread = None

        try:
            self.__recognizer = speech_recognition.Recognizer()
            self.__microphone = speech_recognition.Microphone()
            """
                adjust the recognizer sensitivity to ambient noise and record audio
                from the microphone
            """
            with self.__microphone as source:
                self.__recognizer.adjust_for_ambient_noise(source)

        except OSError as err:
            Logger.logging.critical("OSError: {0}".format(err))
            self.api_runs = False
            self.api_info = GLO_MSG['MICROPHONE_FAILURE']
            return
        except Exception as err:
            Logger.logging.critical("Exception: {0}".format(err))
            self.api_runs = False
            self.api_info = GLO_MSG['MICROPHONE_FAILURE']
            return
        self.api_info = GLO_MSG['MICROPHONE_INITIALIZED']

    def __validate_command(self, command):
        if command.lower() in GLO_CMD.values():
            self.__command_detected = True
            self.__command = GET_COMMAND(command.lower())
            Logger.logging.info("GLO_CMD command available -> {0}".format(command.lower()))
        else:
            Logger.logging.info("Detected command: {0}".format(command.lower()))
        return

    def __callback_recognition(self, recognizer, audio):
        try:
            command = self.__recognizer.recognize_google(audio, language="pl-PL")
            self.__validate_command(command)
        except UnboundLocalError as err:
            Logger.logging.warning("UnboundLocalError : {0} ".format(err))
        except speech_recognition.RequestError as err:
            Logger.logging.warning("RequestError : {0} ".format(err))
        except speech_recognition.UnknownValueError as err:
            Logger.logging.warning("UnknownValueError : {0} ".format(err))
        return

    def get_command(self):
        return self.__command

    def command_detected(self):
        return self.__command_detected

    def clear(self):
        self.__command = self.__command_detected = False

    def background_listen(self):
        self.__listen_thread = self.__recognizer.listen_in_background(self.__microphone, self.__callback_recognition)


if __name__ == "__main__":
    pass

