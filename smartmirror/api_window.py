from tkinter import Tk, Frame
from tkinter import LEFT, RIGHT, TOP, BOTH
from tkinter import YES
from tkinter import N, NE, SW
from smartmirror.glo_messages import GLO_MSG
from smartmirror.api_state import ApiState
from smartmirror.window.clock import Clock
from smartmirror.window.news import News
from smartmirror.window.weather import Weather
from smartmirror.window.user import User
from smartmirror.window.connections_menu import ConnectionsMenu
from smartmirror.window.pulse_text import PulseText
from smartmirror.api_settings import ApiSettings
from smartmirror.Logger import Logger
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

        self.api_full_screen = True
        self.tk.attributes("-fullscreen", self.api_full_screen)
        self.tk.bind("q", self.quit_api)
        self.tk.bind("f", self.full_screen)

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

        self.clock = Clock(self.top_frame)
        self.clock_displayed = False
        self.clock_view(display=True)

        self.right_top_corner = Frame(self.top_frame, background=ApiSettings.Background)
        self.right_top_corner.pack(side=TOP, fill=BOTH, expand=YES)

        self.user_logged = User(self.right_top_corner)
        self.user_displayed = False

        self.pulse_text = PulseText(self.center_frame)

        self.weather = None
        self.weather_displayed = False

        self.news = None
        self.news_displayed = False

        self.api_info = GLO_MSG['API_WINDOW_INITIALIZED']
        self.api_runs = True
        Logger.debug("Initialization of Application Window class")

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
        Logger.debug("ApiWindow full screen has been enabled"
                             if self.api_full_screen else "ApiWindow full screen has been disabled")
        self.api_full_screen = not self.api_full_screen
        self.tk.attributes("-fullscreen", self.api_full_screen)

    """
        Pulse text functions
    """
    def start_pulse_text(self, text):
        self.pulse_text.set_text(text)
        self.pulse_text.start_animation()

    def stop_pulse_text(self):
        self.pulse_text.stop_animation()

    """
        Initialization of classes with network dependency
    """
    def init_network_dependency(self):
        if self.weather is None:
            self.weather = Weather(self.right_top_corner)

        if self.news is None:
            self.news = News(self.bottom_frame)

    """
        Api icons menu bar enabler
    """
    def display_wifi(self, enable_wifi):
        self.connections_menu.wifi(enable_wifi)

    def display_camera(self, enable_camera):
        self.connections_menu.camera(enable_camera)

    def display_microphone(self, enable_microphone):
        self.connections_menu.microphone(enable_microphone)

    """
        Displays an api features interface
    """
    def clock_view(self, display):
        if self.clock_displayed != display:
            self.clock.pack(side=LEFT, anchor=N, padx=ApiSettings.PaddingX, pady=ApiSettings.PaddingY) \
                if display else self.clock.pack_forget()
            self.clock_displayed = not self.clock_displayed

    def news_view(self, display):
        if self.news_displayed != display:
            self.news.pack(side=LEFT, anchor=SW, padx=ApiSettings.PaddingX, pady=ApiSettings.PaddingY) \
                if display else self.news.pack_forget()
            self.news_displayed = not self.news_displayed

    def weather_view(self, display):
        if self.weather_displayed != display:
            self.weather.pack(side=TOP, anchor=NE, padx=ApiSettings.PaddingX, pady=ApiSettings.PaddingY) \
                if display else self.weather.pack_forget()
            self.weather_displayed = not self.weather_displayed

    def user_view(self, name, display):
        if self.user_displayed != display:
            self.user_logged.set_user_name(name)
            self.user_logged.pack(side=TOP, anchor=NE, padx=ApiSettings.PaddingX, pady=ApiSettings.PaddingY) \
                if display else self.user_logged.pack_forget()
            self.user_displayed = not self.user_displayed


if __name__ == "__main__":
    pass
