from tkinter import *
from PIL import Image, ImageTk
from smartmirror.api_settings import ApiSettings
from smartmirror.icons import icons
from smartmirror.Logger import Logger


class User(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent, bg=ApiSettings.Background)

        image = Image.open(icons["user_logged"])
        image = image.resize((20, 20), Image.ANTIALIAS)
        image = image.convert('RGB')
        self.photo = ImageTk.PhotoImage(image)

        self.user_icon_label = Label(self, bg=ApiSettings.Background, image=self.photo)
        self.user_icon_label.pack(side=LEFT, anchor=N)

        self.user_name = "Log In"
        self.user_name_label = Label(self, text=self.user_name, font=(ApiSettings.Font, ApiSettings.SmallTextSize),
                                     fg=ApiSettings.Foreground, bg=ApiSettings.Background)
        self.user_name_label.pack(side=LEFT, anchor=N)

        Logger.debug("Initialization of User class")

    def set_user_name(self, name):
        self.user_name = str(name)
        self.user_name_label.config(text=self.user_name)
        Logger.debug("set user name : {0}".format(self.user_name))


if __name__ == "__main__":
    pass
