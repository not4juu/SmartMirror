from enum import Enum
from speech_recognition import Recognizer, Microphone
from speech_recognition import RequestError, UnknownValueError
from smartmirror.glo_messages import GLO_MSG
from smartmirror.glo_commands import GLO_CMD
from smartmirror.glo_commands import GET_COMMAND
from smartmirror.api_state import ApiState
from smartmirror.Logger import Logger
"""
    Interface for Api Speech Recognition Options 
"""


class ApiOption(Enum):
    GOOGLE = 1          # ENG, PL supported
    GOOGLE_CLOUD = 2    # ENG, PL supported, account required
    SPHINX = 3          # ENG, other
    WIT = 4             # ENG, PL supported, account required
    AZURE_BING = 5      # ENG, PL supported, account required
    LEX = 6             # only ENG
    HOUNDIFY = 7        # only ENG, account required
    IBM = 8             # ENG, PL supported, account required


"""
    Command Recognition Class
"""


class CommandsRecognition(ApiState):
    def __init__(self, callback, language="pl-PL", api_option=ApiOption.GOOGLE):
        super().__init__()
        self.callback_command_detected = callback
        self.api_option = api_option
        self.language = language
        self.listen_thread = None
        self.phrase_time_limit = 3

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
            Logger.critical("OSError: {0}".format(ose_err))
            self.api_runs = False
            self.api_info = GLO_MSG['MICROPHONE_FAILURE']
            return
        except Exception as err:
            Logger.critical("Exception: {0}".format(err))
            self.api_runs = False
            self.api_info = GLO_MSG['MICROPHONE_FAILURE']
            return
        Logger.debug("Initialization of CommandsRecognition class")
        self.api_info = GLO_MSG['MICROPHONE_INITIALIZED']

    def validate_command(self, command):
        if command.lower() in GLO_CMD.values():
            detected_command_id = GET_COMMAND(command.lower())
            Logger.info("GLO_CMD command available -> {0}".format(command.lower()))
            self.callback_command_detected(detected_command_id)
        else:
            Logger.info("Detected command: {0}".format(command.lower()))

    def callback_recognition(self, recognizer, audio):
        try:
            command = self._api_recognition(audio)
            self.validate_command(command)
        except UnboundLocalError as err:
            Logger.warning("UnboundLocalError : {0} ".format(err))
        except RequestError as err:
            Logger.warning("RequestError : {0} ".format(err))
        except UnknownValueError as err:
            Logger.debug("UnknownValueError : {0} ".format(err))

    def background_listen(self):
        self.listen_thread = self.recognizer.listen_in_background(
            source=self.microphone, callback=self.callback_recognition, phrase_time_limit=self.phrase_time_limit)

    def _api_recognition(self, audio):
        if self.api_option is ApiOption.GOOGLE:
            return self.recognizer.recognize_google(audio, language=self.language)
        elif self.api_option is ApiOption.GOOGLE_CLOUD:
            # Support languages: https://cloud.google.com/speech-to-text/docs/languages
            return self.recognizer.recognize_google_cloud(audio, credentials_json='', language=self.language)
        elif self.api_option is ApiOption.SPHINX:
            # Support languages : https://sourceforge.net/projects/cmusphinx/files/Acoustic%20and%20Language%20Models/
            return self.recognizer.recognize_sphinx(audio, language=self.language)
        elif self.api_option is ApiOption.WIT:
            # Support languages : https://wit.ai/faq, login required
            return self.recognizer.recognize_wit(audio, key='',)
        elif self.api_option is ApiOption.AZURE_BING:
            # Support languages : https://docs.microsoft.com/en-us/azure/cognitive-services/bing-web-search/language-support, login required
            self.recognizer.recognize_bing(audio, key='', language=self.language)
        elif self.api_option is ApiOption.LEX:
            # Support languages: ONLY ENG -> https://docs.aws.amazon.com/lex/latest/dg/gl-limits.html
            return self.recognizer.recognize_lex(audio)
        elif self.api_option is ApiOption.HOUNDIFY:
            # Support languages: ONLY ENG, login required
            return self.recognizer.recognize_houndify(audio, client_id='', client_key='')
        elif self.api_option is ApiOption.IBM:
            # Support languages : https://www.ibm.com/watson/services/language-translator/, login required
            return self.recognizer.recognize_ibm(audio, username='', password='', language=self.language)
        else:
            Logger.error("Api recognition option is not defined")


if __name__ == "__main__":
    pass
