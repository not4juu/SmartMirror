from tkinter import *
import cv2
import numpy as np
from PIL import Image, ImageTk
import pyttsx3
import speech_recognition as sr


class FullscreenWindow:

    def __init__(self):
        self.tk = Tk()
        self.tk.title("Smart Mirror")
        self.tk.configure(background='black')


        self.appname = Label(self.tk, text="Smart Mirror",bg="black",fg="white", font=35)
        self.appname.pack(side=TOP, fill=BOTH)

        self.video = cv2.VideoCapture(0)
       # self.video.set(cv2.CAP_PROP_FRAME_HEIGHT,720)
       # self.video.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)

        if (self.video.isOpened () == False):
            print ("Error - check if camera is connected")
            return None
        self.videoFrame = Frame (self.tk, background='black', borderwidth=0, width=self.video.get (cv2.CAP_PROP_FRAME_WIDTH),
                                 heigh=self.video.get (cv2.CAP_PROP_FRAME_HEIGHT))
        self.videoFrame.pack (side=TOP, expand=True)

        #self.topFrame = Frame(self.tk, background = 'black')
        #self.bottomFrame = Frame(self.tk, background = 'black')
        #self.topFrame.pack(side = TOP, fill=BOTH, expand = YES)
        #self.bottomFrame.pack(side = BOTTOM, fill=BOTH, expand = YES)

        self.state = False
        self.tk.bind("<Return>", self.toggle_fullscreen)
        self.tk.bind("<Escape>", self.end_fullscreen)
        self.tk.bind("a",self.camera_capture)

    def toggle_fullscreen(self, event=None):
        self.state = not self.state  # Just toggling the boolean
        self.tk.attributes("-fullscreen", self.state)
        return "break"

    def end_fullscreen(self, event=None):
        self.state = False
        self.tk.attributes("-fullscreen", False)
        return "break"

    def camera_capture(self,event=None):

        self.lmain = Label (self.videoFrame,  borderwidth=0)
        self.lmain.grid(row=0, column =0)

        ret, frame = self.video.read ()

        cv2image = cv2.cvtColor (frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(cv2image)
        imgtk = ImageTk.PhotoImage(image=img)
        self.lmain.imgtk = imgtk
        self.lmain.configure(image=imgtk)

        print ("OK" ,self.video.get(cv2.CAP_PROP_FRAME_WIDTH), self.video.get(cv2.CAP_PROP_FRAME_HEIGHT) )
        return None

def camera():
    cap = cv2.VideoCapture (0)
    if (cap.isOpened () == False):
        print ("Error opening video stream or file")

    # Read until video is completed
    while (cap.isOpened ()):
        # Capture frame-by-frame
        ret, frame = cap.read ()
        if ret == True:

            # Display the resulting frame
            cv2.imshow ('Frame', frame)

            # Press Q on keyboard to  exit
            if cv2.waitKey (25) & 0xFF == ord ('q'):
                break

        # Break the loop
        else:
            break

    # When everything done, release the video capture object
    cap.release ()

    # Closes all the frames
    cv2.destroyAllWindows ()


def text_to_speech():
    engine = pyttsx3.init ()
    engine.setProperty ('rate', 100)
    engine.setProperty ('volume', 0.9)
    voices = engine.getProperty ('voices')
    print (voices)
    engine.setProperty ('voice', voices[1].id)
    engine.say ('Welcome in Smart Mirror')
    engine.runAndWait ()

def speak_recognizer():
    r = sr.Recognizer ()
    with sr.Microphone () as source:
        print ("Speak:")
        audio = r.listen (source)

    try:
        print ("You said " + r.recognize_google (audio))
    except sr.UnknownValueError:
        print ("Could not understand audio")
    except sr.RequestError as e:
        print ("Could not request results; {0}".format (e))

if __name__ == "__main__":
    text_to_speech()
    root = FullscreenWindow ()
    root.tk.mainloop ()
    #camera ()
