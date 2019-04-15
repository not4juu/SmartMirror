import speech_recognition
import Logger

class CommandRecognition(object):

    def __init__(self):
        self.__api_state = True
        self.__api_state_info = 'NO_ERROR'

        try:
            self.__recognizer = speech_recognition.Recognizer()
            self.__microphone = speech_recognition.Microphone()
        except OSError as err:
            Logger.logging.critical("OSError: {0}".format(err))
            self.__api_state = False
            self.__api_state_info = 'MICROPHONE_FAILURE'
            return
        except Exception as err:
            Logger.logging.critical("Exception: {0}".format(err))
            self.__api_state = False
            self.__api_state_info = 'MICROPHONE_FAILURE'
            return
        self.__api_state_info = 'MICROPHONE_INITIALIZED'

    def api_state_ok(self):
        return self.__api_state

    def get_state_info(self):
        return  self.__api_state_info

if __name__ == "__main__":
    pass

