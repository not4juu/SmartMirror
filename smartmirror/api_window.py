from tkinter import *
from PIL import Image, ImageTk

import cv2
import sys
import Logger

"""
    Aplication Window
"""

class ApiWindow:

    def __init__(self):
        self.tk = Tk()
        self.tk.title("Smart Mirror")
        self.tk.configure(background='black')
        Logger.logging.info("Init ApiWindow object")

        self.appname = Label(
            self.tk, text="Smart Mirror", bg="black",fg="white", font=35
        )
        self.appname.pack(side=TOP, fill=BOTH)

        try:
            self.video = cv2.VideoCapture(0)
            if not self.video.isOpened():
                raise NameError("Camera not connected")
        except cv2.error as e:
            Logger.logging.critical("OpenCV camera hardware problem")
        except Exception as e:
            Logger.logging.critical("Camera hardware is not connected")
            sys.exit(1)
       # self.video.set(cv2.CAP_PROP_FRAME_HEIGHT,720)
       # self.video.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)


        self.videoFrame = Frame (self.tk, background='black', borderwidth=0, width=self.video.get (cv2.CAP_PROP_FRAME_WIDTH),
                                 heigh=self.video.get (cv2.CAP_PROP_FRAME_HEIGHT))
        self.videoFrame.pack (side=TOP, expand=True)

        #self.topFrame = Frame(self.tk, background = 'black')
        #self.bottomFrame = Frame(self.tk, background = 'black')
        #self.topFrame.pack(side = TOP, fill=BOTH, expand = YES)
        #self.bottomFrame.pack(side = BOTTOM, fill=BOTH, expand = YES)

        self.state = False
        self.tk.bind("f", self.toggle_fullscreen)
        self.tk.bind("<Escape>", self.end_fullscreen)
        self.tk.bind("a",self.camera_capture)
        Logger.logging.debug ("ApiWindow Logger has been created successfully")

    def toggle_fullscreen(self, event=None):
        Logger.logging.debug ("ApiWindow full screen enabled")
        self.state = True
        self.tk.attributes("-fullscreen", self.state)
        return

    def end_fullscreen(self, event=None):
        Logger.logging.debug ("ApiWindow full screen disabled")
        self.state = False
        self.tk.attributes("-fullscreen", self.state)
        return

    def camera_capture(self,event=None):
        Logger.logging.debug ("Capture camera image starts")
        self.lmain = Label (self.videoFrame,  borderwidth=0)
        self.lmain.grid(row=0, column =0)

        ret, frame = self.video.read ()

        cv2image = cv2.cvtColor (frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(cv2image)
        imgtk = ImageTk.PhotoImage(image=img)
        self.lmain.imgtk = imgtk
        self.lmain.configure(image=imgtk)

        Logger.logging.debug (
            "Capture camera image ends successfully width:{0} height:{1}".format(
            self.video.get(cv2.CAP_PROP_FRAME_WIDTH), self.video.get(cv2.CAP_PROP_FRAME_HEIGHT) )
        )
        return


if __name__ == "__main__":
    pass
