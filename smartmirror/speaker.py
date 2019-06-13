import pyttsx3
from smartmirror.Logger import Logger


class Speaker:
    def __init__(self):
        try:
            self.engine_speak = pyttsx3.init()
            self.engine_speak.setProperty('rate', 130)
            self.engine_speak.setProperty('volume', 1)
            voices = self.engine_speak.getProperty('voices')
            self.engine_speak.setProperty('voice', voices[0].id)
            Logger.debug("Speaker Class initialized correctly")

        except Exception as err:
            Logger.error("Speaker initialization error : {0}".format(err))

    def say(self, text):
        try:
            Logger.info("Speaker say : {0}".format(text))
            self.engine_speak.say(text)
            self.engine_speak.runAndWait()
        except Exception as err:
            Logger.error("Speaker error : {0}".format(err))


if __name__ == "__main__":
    pass
