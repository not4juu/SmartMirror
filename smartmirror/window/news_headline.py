from tkinter import *
from PIL import Image, ImageTk
from smartmirror.api_settings import ApiSettings
import smartmirror.Logger as Logger
"""
    News Headline Class
"""


class NewsHeadline(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent, bg=ApiSettings.Background)

        image = Image.open("icons/news.png")
        image = image.resize((20, 20), Image.ANTIALIAS)
        image = image.convert('RGB')
        photo = ImageTk.PhotoImage(image)

        self.icon_label = Label(self, bg=ApiSettings.Background, image=photo)
        self.icon_label.image = photo
        self.icon_label.pack(side=LEFT, anchor=N)

        self.headline_text = ""
        self.headline_text_label = Label(self, text=self.headline_text,
                                         font=(ApiSettings.Font, ApiSettings.SmallTextSize),
                                         fg=ApiSettings.Foreground, bg=ApiSettings.Background)
        self.headline_text_label.pack(side=LEFT, anchor=N)
        Logger.logging.debug("Initialization of News Headline class")

    def update_headline(self, headline_text=""):
        self.headline_text = headline_text
        self.headline_text_label.config(text=self.headline_text)


if __name__ == '__main__':
    pass
