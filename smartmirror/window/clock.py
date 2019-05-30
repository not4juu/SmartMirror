from contextlib import contextmanager
from tkinter import *
from threading import Lock
import locale
from time import strftime
from smartmirror.api_settings import ApiSettings
import smartmirror.Logger as Logger

CLOCK_LOCKER = Lock()
@contextmanager
def setlocale(name): #thread proof function to work with locale
    with CLOCK_LOCKER:
        saved = locale.setlocale(locale.LC_ALL)
        try:
            yield locale.setlocale(locale.LC_ALL, name)
        finally:
            locale.setlocale(locale.LC_ALL, saved)


"""
    Clock Class
"""


class Clock(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent, bg=ApiSettings.Background)
        self.time_format = 24
        self.date_format = "  %A : %d %B %Y"

        self.time = ''
        self.time_label = Label(self, font=(ApiSettings.Font, ApiSettings.LargeTextSize),
                                fg=ApiSettings.Foreground, bg=ApiSettings.Background)
        self.time_label.pack(side=TOP, anchor=W)

        self.date = ''
        self.date_label = Label(self, text=self.date, font=(ApiSettings.Font, ApiSettings.MediumTextSize),
                                fg=ApiSettings.Foreground, bg=ApiSettings.Background)
        self.date_label.pack(side=TOP, anchor=W)

        Logger.logging.debug("Initialization of Clock class")
        self.tick()

    def tick(self):
        with setlocale(""):
            current_time = strftime('%I:%M:%S %p') if self.time_format == 12 else strftime('%H:%M:%S')
            current_date = strftime(self.date_format)

            if current_time != self.time:
                self.time = current_time
                self.time_label.config(text=self.time)
            if current_date != self.date:
                self.date = current_date
                self.date_label.config(text=self.date)
            self.time_label.after(500, self.tick)


if __name__ == "__main__":
    pass
