from glo_messages import GLO_MSG
from glo_commands import GLO_CMD
import speech_recognition
import Logger

class CommandRecognition(object):

    def __init__(self):
        self.__api_state = True
        self.__api_state_info = GLO_MSG['NO_ERROR']

        self.__command_detected = False

        try:
            self.__recognizer = speech_recognition.Recognizer()
            self.__microphone = speech_recognition.Microphone()
        except OSError as err:
            Logger.logging.critical("OSError: {0}".format(err))
            self.__api_state = False
            self.__api_state_info = GLO_MSG['MICROPHONE_FAILURE']
            return
        except Exception as err:
            Logger.logging.critical("Exception: {0}".format(err))
            self.__api_state = False
            self.__api_state_info = GLO_MSG['MICROPHONE_FAILURE']
            return
        self.__api_state_info = GLO_MSG['MICROPHONE_INITIALIZED']

    def api_state_ok(self):
        return self.__api_state

    def get_state_info(self):
        return self.__api_state_info

    def get_command_detected(self):
        return self.__command_detected

    def __validate_command(self, command):
        available_commands = [
            'pokaż kalendarz' , 'pokaż pogodę'
        ]
        if command.lower() in available_commands:
            Logger.logging.debug("Available command: index : {0} command: {1}".format(
                available_commands.index(command.lower()), command.lower())
            )
        return

    def run_command_rec(self):
        """
            adjust the recognizer sensitivity to ambient noise and record audio
            from the microphone
        """
        with self.__microphone as source:
            self.__recognizer.adjust_for_ambient_noise(source)
            audio = self.__recognizer.listen(source,timeout=3)
        try:
            command =  self.__recognizer.recognize_google(audio, language = "pl-PL")
            Logger.logging.debug("Recognized command : {0}".format(command))
        except speech_recognition.RequestError as err:
            Logger.logging.critical("RequestError : {0} ".format(err))
        except speech_recognition.UnknownValueError as err:
            Logger.logging.critical ("UnknownValueError : {0} ".format (err))

        self.__validate_command(command)
        return


if __name__ == "__main__":
    Logger.init_logger (outIntoFile=False, verbose=True)
    r = CommandRecognition()
    r.run_command_rec()
    pass

