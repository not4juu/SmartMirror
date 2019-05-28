from smartmirror.api_settings import ApiSettings
import smartmirror.Logger as Logger
from contextlib import contextmanager
from tkinter import *
import threading
import locale
import time

CLOCK_LOCKER = threading.Lock()
@contextmanager
def setlocale(name): #thread proof function to work with locale
    with CLOCK_LOCKER:
        saved = locale.setlocale(locale.LC_ALL)
        try:
            yield locale.setlocale(locale.LC_ALL, name)
        finally:
            locale.setlocale(locale.LC_ALL, saved)

class Clock(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent, bg=ApiSettings.Background)
        self.__time_format = 24
        self.__date_format = "%A : %d %B %Y"
        # initialize time label
        self.__time = ''
        self.__time_label = Label(self, font=(ApiSettings.Font, ApiSettings.LargeTextSize),
                               fg=ApiSettings.Foreground, bg=ApiSettings.Background)
        self.__time_label.pack(side=TOP, anchor=E)

        self.__date = ''
        self.__date_label = Label(self, text=self.__date, font=(ApiSettings.Font, ApiSettings.SmallTextSize),
                               fg=ApiSettings.Foreground, bg=ApiSettings.Background)
        self.__date_label.pack(side=TOP, anchor=E)

        Logger.logging.debug("Initialization of Clock class")
        self.__tick()

    def __tick(self):
        with setlocale(""):
            current_time = time.strftime('%I:%M:%S %p') if self.__time_format == 12 else time.strftime('%H:%M:%S')
            current_date = time.strftime(self.__date_format)
            # if time string has changed, update it
            if current_time != self.__time:
                self.__time = current_time
                self.__time_label.config(text=current_time)
            if current_date != self.__date:
                self.__date = current_date
                self.__date_label.config(text=current_date)
            self.__time_label.after(500, self.__tick)

if __name__ == '__main__':
    pass