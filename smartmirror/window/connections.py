from smartmirror.api_settings import ApiSettings
import smartmirror.Logger as Logger
from tkinter import *
from PIL import Image, ImageTk

class Connections(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent, bg=ApiSettings.Background)
        self.__resizeX = 20
        self.__resizeY = 20

        self.__connections_container = Frame(self, bg=ApiSettings.Background, highlightthickness=1,highlightbackground="yellow")
        self.__connections_container.pack(side=RIGHT, anchor=SE)

        wifi_disable_image = Image.open("icons/wifi_disable.png")
        wifi_enable_image = Image.open("icons/wifi_enable.png")
        self.__wifi_disable_icon = ImageTk.PhotoImage(wifi_disable_image.resize((self.__resizeX, self.__resizeY), Image.ANTIALIAS).convert('RGB'))
        self.__wifi_enable_icon = ImageTk.PhotoImage(wifi_enable_image.resize((self.__resizeX, self.__resizeY), Image.ANTIALIAS).convert('RGB'))

        camera_disable_image = Image.open("icons/camera_disable.png")
        camera_enable_image = Image.open("icons/camera_enable.png")
        self.__camera_disable_icon = ImageTk.PhotoImage(camera_disable_image.resize((self.__resizeX, self.__resizeY), Image.ANTIALIAS).convert('RGB'))
        self.__camera_enable_icon = ImageTk.PhotoImage(camera_enable_image.resize((self.__resizeX, self.__resizeY), Image.ANTIALIAS).convert('RGB'))

        microphone_disable_image = Image.open("icons/microphone_disable.png")
        microphone_enable_image = Image.open("icons/microphone_enabled.png")
        self.__microphone_disable_icon = ImageTk.PhotoImage(microphone_disable_image.resize((self.__resizeX, self.__resizeY), Image.ANTIALIAS).convert('RGB'))
        self.__microphone_enable_icon = ImageTk.PhotoImage(microphone_enable_image.resize((self.__resizeX, self.__resizeY), Image.ANTIALIAS).convert('RGB'))

        self.__wifi_label = Label(self.__connections_container, bg=ApiSettings.Background, image=self.__wifi_disable_icon)
        self.__wifi_label.pack(side=RIGHT, anchor=CENTER)

        self.__camera_label = Label(self.__connections_container, bg=ApiSettings.Background, image=self.__camera_disable_icon)
        self.__camera_label.pack(side=RIGHT, anchor=CENTER)

        self.__microphone_label = Label(self.__connections_container, bg=ApiSettings.Background, image=self.__microphone_disable_icon)
        self.__microphone_label.pack(side=RIGHT, anchor=CENTER)

        Logger.logging.debug("Initialization of Connections class")

    def wifi_enable(self):
        self.__wifi_label.configure(image=self.__wifi_enable_icon)
        Logger.logging.debug("Wifi has been enabled")

    def camera_enable(self):
        self.__camera_label.configure(image=self.__camera_enable_icon)
        Logger.logging.debug("Camera has been enabled")

    def microphone_enable(self):
        self.__microphone_label.configure(image=self.__microphone_enable_icon)
        Logger.logging.debug("Microphone has been enabled")

if __name__ == '__main__':
    pass