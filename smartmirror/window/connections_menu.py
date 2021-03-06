from tkinter import Frame, Label
from tkinter import RIGHT, CENTER, SE
from PIL import Image, ImageTk
from smartmirror.api_settings import ApiSettings
from smartmirror.icons import icons
from smartmirror.Logger import Logger
"""
    Connections Class
"""


class ConnectionsMenu(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent, bg=ApiSettings.Background)
        self.resizeX = 20
        self.resizeY = 20

        self.connections_container = Frame(self, bg=ApiSettings.Background)
        self.connections_container.pack(side=RIGHT, anchor=SE)

        """
            Loads menu bar (enable/disable) icons  
        """
        wifi_disable_image = Image.open(icons["wifi_disabled"])
        wifi_enable_image = Image.open(icons["wifi_enabled"])
        self.wifi_disable_icon = ImageTk.PhotoImage(
            wifi_disable_image.resize((self.resizeX, self.resizeY), Image.ANTIALIAS).convert('RGB'))
        self.wifi_enable_icon = ImageTk.PhotoImage(
            wifi_enable_image.resize((self.resizeX, self.resizeY), Image.ANTIALIAS).convert('RGB'))

        camera_disable_image = Image.open(icons["camera_disabled"])
        camera_enable_image = Image.open(icons["camera_enabled"])
        self.camera_disable_icon = ImageTk.PhotoImage(
            camera_disable_image.resize((self.resizeX, self.resizeY), Image.ANTIALIAS).convert('RGB'))
        self.camera_enable_icon = ImageTk.PhotoImage(
            camera_enable_image.resize((self.resizeX, self.resizeY), Image.ANTIALIAS).convert('RGB'))

        microphone_disable_image = Image.open(icons["microphone_disabled"])
        microphone_enable_image = Image.open(icons["microphone_enabled"])
        self.microphone_disable_icon = ImageTk.PhotoImage(
            microphone_disable_image.resize((self.resizeX, self.resizeY), Image.ANTIALIAS).convert('RGB'))
        self.microphone_enable_icon = ImageTk.PhotoImage(
            microphone_enable_image.resize((self.resizeX, self.resizeY), Image.ANTIALIAS).convert('RGB'))

        """
            Creates label of each menu icon  
        """
        self.wifi_label = Label(self.connections_container,
                                bg=ApiSettings.Background, image=self.wifi_disable_icon)
        self.wifi_label.pack(side=RIGHT, anchor=CENTER)

        self.camera_label = Label(self.connections_container,
                                  bg=ApiSettings.Background, image=self.camera_disable_icon)
        self.camera_label.pack(side=RIGHT, anchor=CENTER)

        self.microphone_label = Label(self.connections_container,
                                      bg=ApiSettings.Background, image=self.microphone_disable_icon)
        self.microphone_label.pack(side=RIGHT, anchor=CENTER)

        Logger.debug("Initialization of Connections class")

    def wifi(self, enable):
        self.wifi_label.configure(image=self.wifi_enable_icon) if enable else \
            self.wifi_label.configure(image=self.wifi_disable_icon)
        Logger.debug("Wifi has been enabled" if enable else "Wifi has been disabled")

    def camera(self, enable):
        self.camera_label.configure(image=self.camera_enable_icon) if enable else \
            self.camera_label.configure(image=self.camera_disable_icon)
        Logger.debug("Camera has been enabled" if enable else "Camera has been disabled")

    def microphone(self, enable):
        self.microphone_label.configure(image=self.microphone_enable_icon) if enable else \
            self.microphone_label.configure(image=self.microphone_disable_icon)
        Logger.debug("Microphone has been enabled" if enable else "Microphone has been disabled")


if __name__ == "__main__":
    pass
