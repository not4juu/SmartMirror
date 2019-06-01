import cv2
from tkinter import *
from PIL import Image, ImageTk
from smartmirror.glo_messages import GLO_MSG
from smartmirror.api_state import ApiState
from smartmirror.window.clock import Clock
from smartmirror.window.news import News
from smartmirror.window.weather import Weather
from smartmirror.window.connections_menu import ConnectionsMenu
from smartmirror.api_settings import ApiSettings
import smartmirror.Logger as Logger
"""
    Application Window Class
    
"""


class ApiWindow(ApiState):
    def __init__(self):
        super().__init__()
        """
            Initialization of Tkinter api window
        """
        self.tk = Tk()
        self.tk.title("Smart Mirror")
        self.tk.configure(background=ApiSettings.Background)

        self.tk.bind("q", self.quit_api)
        self.tk.bind("f", self.full_screen)
        self.tk.bind("a", self.camera_capture)  # debug purpose

        """
            Initialization of camera connections
        """
        self.camera = None
        self.api_runs = self.camera_connection()
        self.api_full_screen = False

        """
            Initialization of frames layout
        """
        self.top_frame = Frame(self.tk, background=ApiSettings.Background)
        self.top_frame.pack(side=TOP, fill=BOTH, expand=YES)

        self.center_frame = Frame(self.tk, background=ApiSettings.Background)
        self.center_frame.pack(side=TOP, fill=BOTH, expand=YES)

        self.bottom_frame = Frame(self.tk, background=ApiSettings.Background)
        self.bottom_frame.pack(side=TOP, fill=BOTH, expand=YES)

        """
            Initialization of api window features
        """
        self.connections_menu = ConnectionsMenu(self.bottom_frame)
        self.connections_menu.pack(side=RIGHT, anchor=SW, padx=ApiSettings.PaddingX, pady=ApiSettings.PaddingY)

        if self.api_runs:
            self.display_camera(enable_camera=True)

        self.clock = Clock(self.top_frame)
        self.clock.pack(side=LEFT, anchor=N, padx=ApiSettings.PaddingX, pady=ApiSettings.PaddingY)
        self.clock_enabled = False

        self.weather = Weather(self.top_frame)
        self.weather.pack(side=RIGHT, anchor=NE, padx=ApiSettings.PaddingX, pady=ApiSettings.PaddingY)

        self.camera_frame = Frame(self.center_frame, background=ApiSettings.Background,
                                  width=self.camera.get(cv2.CAP_PROP_FRAME_WIDTH),
                                  heigh=self.camera.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.camera_frame.pack(side=TOP, expand=YES)
        self.camera_label = Label(self.camera_frame, borderwidth=0)

        self.news = None

    def camera_connection(self):
        Logger.logging.debug("Find camera connection")
        try:
            self.camera = cv2.VideoCapture(0)
            if not self.camera.isOpened():
                raise NameError
        except cv2.error as exception:
            Logger.logging.critical("OpenCV camera hardware problem: {0}".format(exception))
            self.api_info = GLO_MSG['API_CAMERA_CONNECTION_FAILURE']
            return False
        except Exception as exception:
            Logger.logging.critical("Camera hardware is not connected: {0}".format(exception))
            self.api_info = GLO_MSG['API_CAMERA_CONNECTION_FAILURE']
            return False
        self.api_info = GLO_MSG['API_WINDOW_INITIALIZED']
        return True

    """
        Tkinter refresh function
    """
    def refresh(self):
        self.tk.update_idletasks()
        self.tk.update()
        return None

    """
        Key callback functions
    """
    def quit_api(self, event=None):
        self.api_runs = False
        self.api_info = GLO_MSG['API_USER_QUIT']

    def full_screen(self, event=None):
        Logger.logging.debug("ApiWindow full screen  has been enabled"
                             if self.api_full_screen else "ApiWindow full screen has been disabled")
        self.api_full_screen = not self.api_full_screen
        self.tk.attributes("-fullscreen", self.api_full_screen)

    def camera_capture(self, event=None):
        Logger.logging.debug("Capture camera image starts")
        self.camera_label.grid(row=0, column=0)
        response, frame = self.camera.read()
        if response:
            cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(cv2image)
            imgtk = ImageTk.PhotoImage(image=img)
            self.camera_label.imgtk = imgtk
            self.camera_label.configure(image=imgtk)
            Logger.logging.debug("Capture camera image ends successfully width:{0} height:{1}".format(
                self.camera.get(cv2.CAP_PROP_FRAME_WIDTH), self.camera.get(cv2.CAP_PROP_FRAME_HEIGHT)))

    """
        Api icons menu bar enabler
    """
    def display_wifi(self, enable_wifi):
        self.connections_menu.wifi(enable_wifi)
        self.news = News(self.bottom_frame)
        self.news.pack(side=LEFT, anchor=SW, padx=ApiSettings.PaddingX, pady=ApiSettings.PaddingY)

    def display_camera(self, enable_camera):
        self.connections_menu.camera(enable_camera)

    def display_microphone(self, enable_microphone):
        self.connections_menu.microphone(enable_microphone)

    """
        Clock enabler/disabler
    """
    def display_clock(self):
        if not self.clock_enabled:
            self.clock.pack(side=LEFT, anchor=N, padx=20, pady=10)
            self.clock_enabled = True

    def hide_clock(self):
        if self.clock_enabled:
            self.clock.pack_forget()
            self.clock_enabled = False


if __name__ == "__main__":
    pass
