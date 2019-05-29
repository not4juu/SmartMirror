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


import requests
import json

icon_lookup = {
    'clear-day': "Newspaper.png",  # clear sky day
    'wind': "Newspaper.png",   #wind
    'cloudy': "Newspaper.png",  # cloudy day
    'partly-cloudy-day': "Newspaper.png",  # partly cloudy day
    'rain': "Newspaper.png",  # rain day
    'snow': "Newspaper.png",  # snow day
    'snow-thin': "Newspaper.png",  # sleet day
    'fog': "Newspaper.png",  # fog day
    'clear-night': "Newspaper.png",  # clear sky night
    'partly-cloudy-night': "Newspaper.png",  # scattered clouds night
    'thunderstorm': "Newspaper.png",  # thunderstorm
    'tornado': "Newspaper.png",    # tornado
    'hail': "Newspaper.png"  # hail
}

weather_lang = 'en' # see https://darksky.net/dev/docs/forecast for full list of language parameters values
weather_unit = 'us' # see https://darksky.net/dev/docs/forecast for full list of unit parameters values
latitude = None # Set this if IP location lookup does not work for you (must be a string)
longitude = None # Set this if IP location lookup does not work for you (must be a string)
xlarge_text_size = 94
large_text_size = 48
medium_text_size = 28
small_text_size = 18
weather_api_token = 'c6da61aaa99fb6c6e4d0dc5276b488ec' # create account at https://darksky.net/dev/

class Weather(Frame):
    def __init__(self, parent, *args, **kwargs):
        Frame.__init__(self, parent, bg='black')
        self.temperature = ''
        self.forecast = ''
        self.location = ''
        self.currently = ''
        self.icon = ''
        self.degreeFrm = Frame(self, bg="black")
        self.degreeFrm.pack(side=TOP, anchor=W)
        self.temperatureLbl = Label(self.degreeFrm, font=('Helvetica', xlarge_text_size), fg="white", bg="black")
        self.temperatureLbl.pack(side=LEFT, anchor=N)
        self.iconLbl = Label(self.degreeFrm, bg="black")
        self.iconLbl.pack(side=LEFT, anchor=N, padx=20)
        self.currentlyLbl = Label(self, font=('Helvetica', medium_text_size), fg="white", bg="black")
        self.currentlyLbl.pack(side=TOP, anchor=W)
        self.forecastLbl = Label(self, font=('Helvetica', small_text_size), fg="white", bg="black")
        self.forecastLbl.pack(side=TOP, anchor=W)
        self.locationLbl = Label(self, font=('Helvetica', small_text_size), fg="white", bg="black")
        self.locationLbl.pack(side=TOP, anchor=W)
        self.get_weather()

    def get_ip(self):
        try:
            ip_url = "http://jsonip.com/"
            req = requests.get(ip_url)
            ip_json = json.loads(req.text)
            return ip_json['ip']
        except Exception as err:
            Logger.logging.critical("Exception: {0}".format(err))

    def get_weather(self):
        try:

            if latitude is None and longitude is None:
                # get location
                location_req_url = "http://freegeoip.net/json/%s" % self.get_ip()
                r = requests.get(location_req_url)
                location_obj = json.loads(r.text)

                lat = location_obj['latitude']
                lon = location_obj['longitude']

                location2 = "%s, %s" % (location_obj['city'], location_obj['region_code'])

                # get weather
                weather_req_url = "https://api.darksky.net/forecast/%s/%s,%s?lang=%s&units=%s" % (weather_api_token, lat,lon,weather_lang,weather_unit)
            else:
                location2 = ""
                # get weather
                weather_req_url = "https://api.darksky.net/forecast/%s/%s,%s?lang=%s&units=%s" % (weather_api_token, latitude, longitude, weather_lang, weather_unit)

            r = requests.get(weather_req_url)
            weather_obj = json.loads(r.text)

            degree_sign= u'\N{DEGREE SIGN}'
            temperature2 = "%s%s" % (str(int(weather_obj['currently']['temperature'])), degree_sign)
            currently2 = weather_obj['currently']['summary']
            forecast2 = weather_obj["hourly"]["summary"]

            icon_id = weather_obj['currently']['icon']
            icon2 = None

            if icon_id in icon_lookup:
                icon2 = icon_lookup[icon_id]

            if icon2 is not None:
                if self.icon != icon2:
                    self.icon = icon2
                    image = Image.open(icon2)
                    image = image.resize((100, 100), Image.ANTIALIAS)
                    image = image.convert('RGB')
                    photo = ImageTk.PhotoImage(image)

                    self.iconLbl.config(image=photo)
                    self.iconLbl.image = photo
            else:
                # remove image
                self.iconLbl.config(image='')

            if self.currently != currently2:
                self.currently = currently2
                self.currentlyLbl.config(text=currently2)
            if self.forecast != forecast2:
                self.forecast = forecast2
                self.forecastLbl.config(text=forecast2)
            if self.temperature != temperature2:
                self.temperature = temperature2
                self.temperatureLbl.config(text=temperature2)
            if self.location != location2:
                if location2 == ", ":
                    self.location = "Cannot Pinpoint Location"
                    self.locationLbl.config(text="Cannot Pinpoint Location")
                else:
                    self.location = location2
                    self.locationLbl.config(text=location2)
        except Exception as err:
            Logger.logging.critical("Exception: {0}".format(err))

        self.after(600000, self.get_weather)

    @staticmethod
    def convert_kelvin_to_fahrenheit(kelvin_temp):
        return 1.8 * (kelvin_temp - 273) + 32



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
