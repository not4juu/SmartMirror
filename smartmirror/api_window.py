from tkinter import *
from PIL import Image, ImageTk

import cv2
import sys
import Logger

"""
    Aplication Window
"""

class ApiWindow:

    def __camera_connection(self):
        Logger.logging.debug("Find camera connection")
        try:
            self.__camera = cv2.VideoCapture(0)
            if not self.__camera.isOpened():
                raise NameError
        except cv2.error as exception:
            Logger.logging.critical("OpenCV camera hardware problem: {0}".format(exception))
            self.__api_state_info =  'API_CAMERA_CONNECTION_FAILURE'
            return False
        except Exception as exception:
            Logger.logging.critical("Camera hardware is not connected: {0}".format(exception))
            self.__api_state_info = 'API_CAMERA_CONNECTION_FAILURE'
            return False
        self.__api_state_info = 'API_WINDOW_INITIALIZED'
        return True

    def __init__(self):
        Logger.logging.info("Init ApiWindow object")
        self.__camera = None
        self.__tk = Tk()
        self.__tk.title("Smart Mirror")
        self.__tk.configure(background='black')

        self.__api_state_info = 'NO_ERROR'
        self.__api_state = self.__camera_connection()

        api_name = Label(
            self.__tk, text="Smart Mirror", bg="black",fg="white", font=35
        )
        api_name.pack(side=TOP, fill=BOTH)
        self.__camera_frame = Frame(self.__tk, background='black', borderwidth=0,
                                 width=self.__camera.get (cv2.CAP_PROP_FRAME_WIDTH),
                                 heigh=self.__camera.get (cv2.CAP_PROP_FRAME_HEIGHT))
        self.__camera_frame.pack(side=TOP, expand=True)

        self.__fullscreen_enabled = False
        self.__tk.bind("f", self.__enable_fullscreen)
        self.__tk.bind("<Escape>", self.__disable_fullscreen)
        self.__tk.bind("a",self.__camera_capture)
        self.__tk.bind ("q", self.__quit)
       # self.video.set(cv2.CAP_PROP_FRAME_HEIGHT,720)
       # self.video.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)

        #self.topFrame = Frame(self.tk, background = 'black')
        #self.bottomFrame = Frame(self.tk, background = 'black')
        #self.topFrame.pack(side = TOP, fill=BOTH, expand = YES)
        #self.bottomFrame.pack(side = BOTTOM, fill=BOTH, expand = YES)


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
        self.__api_state = False
        self.__api_state_info = 'API_USER_QUIT'
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


    def api_state_ok(self):
        return self.__api_state

    def get_state_info(self):
        return self.__api_state_info

    def refresh(self):
        self.__tk.update_idletasks()
        self.__tk.update()
        return


if __name__ == "__main__":
    pass
