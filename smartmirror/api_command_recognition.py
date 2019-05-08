from smartmirror.glo_messages import GLO_MSG
from smartmirror.glo_commands import GLO_CMD
from smartmirror.glo_commands import GET_COMMAND
from smartmirror.api_state import ApiState
import Logger
import speech_recognition

class CommandRecognition(ApiState):

    def __init__(self):
        super().__init__ ()
        self.__command_detected = False

        try:
            self.__recognizer = speech_recognition.Recognizer()
            self.__microphone = speech_recognition.Microphone()
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

    def get_command_detected(self):
        return self.__command_detected

    def __validate_command(self, command):
        if command.lower() in GLO_CMD.values():
            Logger.logging.debug("Available GLO_CMD command : {0} -> {1}".format(
                GET_COMMAND(command.lower()), command.lower())
            )
        else:
            Logger.logging.debug("Not available GLO_CMD command : {0}".format(command.lower ()))
        return

    def listen_command(self):
        """
            adjust the recognizer sensitivity to ambient noise and record audio
            from the microphone
        """
        with self.__microphone as source:
            try:
                self.__recognizer.adjust_for_ambient_noise(source)
                audio = self.__recognizer.listen(source,timeout=3)
            except speech_recognition.WaitTimeoutError as err:
                Logger.logging.warning("WaitTimeoutError : {0} ".format (err))
                return

        try:
            command = self.__recognizer.recognize_google(audio, language = "pl-PL")
            Logger.logging.debug("Recognized command : {0}".format(command))
            self.__validate_command(command)

        except UnboundLocalError as err:
            Logger.logging.error("UnboundLocalError : {0} ".format(err))
        except speech_recognition.RequestError as err:
            Logger.logging.error("RequestError : {0} ".format(err))
        except speech_recognition.UnknownValueError as err:
            Logger.logging.error ("UnknownValueError : {0} ".format (err))
        return


if __name__ == "__main__":
    Logger.init_logger(outIntoFile=False, verbose=True)
    r = CommandRecognition()
    r.listen_command()
    pass

