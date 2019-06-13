from tkinter import *
from smartmirror.api_settings import ApiSettings
from smartmirror.Logger import Logger
"""
    PulseText - generates pulse text animation based on Canvas utilities
"""


class PulseText:
    def __init__(self, parent):
        self.canvas = Canvas(parent, bg=ApiSettings.Background, highlightthickness=0)
        width = int(self.canvas.cget("width")) / 2
        height = int(self.canvas.cget("height")) / 2
        self.text = self.canvas.create_text(width, height, fill=ApiSettings.Foreground,
                                            font=(ApiSettings.Font, ApiSettings.LargeTextSize), text="no text")

        self.run = False
        self.color = 0
        self.brighten = True

        Logger.debug("Initialization of PulseText class")

    def _animation(self):
        pulse_color = "#{:02x}{:02x}{:02x}".format(self.color, self.color, self.color)

        if self.color == 0:
            self.brighten = True

        if self.color == 255:
            self.brighten = False

        if self.brighten:
            self.color += 5
        else:
            self.color -= 5
        self.canvas.itemconfig(self.text, fill=pulse_color)

        if self.run:
            self.canvas.after(15, self._animation)

    def set_text(self, text):
        self.canvas.itemconfig(self.text, text=text)
        Logger.debug("Set pulse text animation: {0}".format(text))

    def start_animation(self):
        self.canvas.pack()
        self.run = True
        self._animation()
        Logger.debug("Start pulse text animation")

    def stop_animation(self):
        self.run = False
        self.canvas.pack_forget()
        Logger.debug("Stop pulse text animation")


if __name__ == "__main__":
    tk = Tk()
    center_frame = Frame(tk, background=ApiSettings.Background)
    center_frame.pack(side=TOP, fill=BOTH, expand=YES)
    pulse = PulseText(center_frame)
    pulse.set_text("Authorization")
    pulse.start_animation()
    tk.mainloop()