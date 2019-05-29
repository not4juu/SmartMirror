from smartmirror.glo_messages import GLO_MSG
from smartmirror.api_state import ApiState
from smartmirror.window.clock import Clock
from smartmirror.window.news import News
from smartmirror.window.connections import Connections
from smartmirror.api_settings import ApiSettings
from tkinter import *
from PIL import Image, ImageTk
import smartmirror.Logger as Logger
import cv2

"""
    Aplication Window
"""

class ApiWindow(ApiState):

    def __init__(self):
        super().__init__()

        self.__camera = None
        self.__tk = Tk()
        self.__tk.title("Smart Mirror")
        self.__tk.configure(background=ApiSettings.Background)

        self.__topFrame = Frame(self.__tk, background=ApiSettings.Background, highlightthickness=1,highlightbackground="red")
        self.__topFrame.pack(side=TOP, fill=BOTH, expand=YES)

        self.__bottomFrame = Frame(self.__tk, background = ApiSettings.Background,
                                 highlightthickness=1,highlightbackground="green")
        self.__bottomFrame.pack(side=BOTTOM, fill=BOTH, expand=NO)

        self.__conections = Connections(self.__bottomFrame)
        self.__conections.pack(side=RIGHT, anchor=SW, padx=ApiSettings.PaddingX, pady=ApiSettings.PaddingY)

        self.api_runs = self.__camera_connection()

        self.__clock = Clock(self.__topFrame)
        self.__clock_enabled = False
        self.__clock.pack(side=LEFT, anchor=N, padx=ApiSettings.PaddingX, pady=ApiSettings.PaddingY)

        self.__camera_frame = Frame(self.__tk, background=ApiSettings.Background, borderwidth=0,
                                 width=self.__camera.get (cv2.CAP_PROP_FRAME_WIDTH),
                                 heigh=self.__camera.get (cv2.CAP_PROP_FRAME_HEIGHT),
                                 highlightthickness=1,highlightbackground="blue")
        self.__camera_frame.pack(side=TOP, expand=YES)

        self.__fullscreen_enabled = False
        self.__tk.bind("f", self.__enable_fullscreen)
        self.__tk.bind("<Escape>", self.__disable_fullscreen)
        self.__tk.bind("a",self.__camera_capture)
        self.__tk.bind ("q", self.__quit)
       # self.video.set(cv2.CAP_PROP_FRAME_HEIGHT,720)
       # self.video.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)

        #self.topFrame = Frame(self.tk, background = 'black')
        #self.topFrame = Frame(self.tk, background = 'black')

        #self.weather = Weather(self.__topFrame)
        #self.weather.pack(side=RIGHT, anchor=N, padx=100, pady=60)


        #self.calender = Calendar(self.bottomFrame)
        #self.calender.pack(side = RIGHT, anchor=S, padx=100, pady=60)
        self.news = None


    def __camera_connection(self):
        Logger.logging.debug("Find camera connection")
        try:
            self.__camera = cv2.VideoCapture(0)
            if not self.__camera.isOpened():
                raise NameError
        except cv2.error as exception:
            Logger.logging.critical("OpenCV camera hardware problem: {0}".format(exception))
            self.api_info =  GLO_MSG['API_CAMERA_CONNECTION_FAILURE']
            return False
        except Exception as exception:
            Logger.logging.critical("Camera hardware is not connected: {0}".format(exception))
            self.api_info = GLO_MSG['API_CAMERA_CONNECTION_FAILURE']
            return False
        self.display_camera_enable()
        self.api_info = GLO_MSG['API_WINDOW_INITIALIZED']
        return True

    def display_clock(self):
        if not self.__clock_enabled:
            self.__clock.pack(side=LEFT, anchor=N, padx=20, pady=10)
            self.__clock_enabled = True
        return

    def hide_clock(self):
        if self.__clock_enabled:
            self.__clock.pack_forget()
            self.__clock_enabled = False
        return

    def display_wifi_enable(self):
        self.__conections.wifi_enable()
        self.news = News(self.__bottomFrame)
        self.news.pack(side=LEFT, anchor=SW, padx=ApiSettings.PaddingX, pady=ApiSettings.PaddingY)

    def display_camera_enable(self):
        self.__conections.camera_enable()

    def display_microphone_enable(self):
        self.__conections.microphone_enable()

    def __enable_fullscreen(self, event=None):
        Logger.logging.debug ("ApiWindow full screen enabled")
        self.__fullscreen_enabled = True
        self.__tk.attributes("-fullscreen", self.__fullscreen_enabled)
        return

    def __disable_fullscreen(self, event=None):
        Logger.logging.debug ("ApiWindow full screen disabled")
        self.__fullscreen_enabled = False
        self.__tk.attributes("-fullscreen", self.__fullscreen_enabled)
        return

    def __quit(self, event=None):
        self.api_runs = False
        self.api_info = GLO_MSG['API_USER_QUIT']
        return

    def __camera_capture(self,event=None):
        Logger.logging.debug ("Capture camera image starts")
        self.lmain = Label (self.__camera_frame,  borderwidth=0)
        self.lmain.grid(row=0, column =0)

        ret, frame = self.__camera.read ()

        cv2image = cv2.cvtColor (frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(cv2image)
        imgtk = ImageTk.PhotoImage(image=img)
        self.lmain.imgtk = imgtk
        self.lmain.configure(image=imgtk)

        Logger.logging.debug (
            "Capture camera image ends successfully width:{0} height:{1}".format(
            self.__camera.get(cv2.CAP_PROP_FRAME_WIDTH), self.__camera.get(cv2.CAP_PROP_FRAME_HEIGHT) )
        )
        return

    def refresh(self):
        self.__tk.update_idletasks()
        self.__tk.update()
        return


if __name__ == "__main__":
    pass
