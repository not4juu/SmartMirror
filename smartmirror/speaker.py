import pyttsx3
import smartmirror.Logger as Logger


class Speaker:
    def __init__(self):
        try:
            self.engine_speak = pyttsx3.init()
            self.engine_speak.setProperty('rate', 130)
            self.engine_speak.setProperty('volume', 1)
            voices = self.engine_speak.getProperty('voices')
            self.engine_speak.setProperty('voice', voices[0].id)
        except Exception as err:
            Logger.logging.error("Speaker initialization error : {0}".format(err))

    def say(self, text):
        try:
            Logger.logging.info("Speak say : {0}".format(text))
            self.engine_speak.say(text)
            self.engine_speak.runAndWait()
        except Exception as err:
            Logger.logging.error("Speaker error : {0}".format(err))


if __name__ == "__main__":
    pass
