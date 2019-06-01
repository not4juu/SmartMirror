import requests
import json
from tkinter import *
from PIL import Image, ImageTk
from smartmirror.api_settings import ApiSettings
from smartmirror.network import Network
from smartmirror.icons import icons
import smartmirror.Logger as Logger
"""
    Weather Class
    
    implementation is based on https://darksky.net/dev/docs/forecast, refer to doc to full list of request parameters 
"""


class Weather(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent, bg=ApiSettings.Background)
        self.weather_api_token = ''  # token from https://darksky.net/dev/ account
        self.location_info = None
        self.weather_info = None
        self.weather_lang = 'pl'
        self.weather_unit = 'auto'
        self.weather_icon = None

        self.degree_frame = Frame(self, bg=ApiSettings.Background)
        self.degree_frame.pack(side=TOP, anchor=E)
        self.temperature_label = Label(self.degree_frame, font=(ApiSettings.Font, ApiSettings.HugeTextSize),
                                       fg=ApiSettings.Foreground, bg=ApiSettings.Background)
        self.temperature_label.pack(side=RIGHT, anchor=CENTER)
        self.icon_label = Label(self.degree_frame, bg=ApiSettings.Background)
        self.icon_label.pack(side=LEFT, anchor=NW, padx=ApiSettings.PaddingX)

        self.currently_label = Label(self, font=(ApiSettings.Font, ApiSettings.LargeTextSize - 10),
                                     fg=ApiSettings.Foreground, bg=ApiSettings.Background)
        self.currently_label.pack(side=TOP, anchor=E)
        self.forecast_label = Label(self, font=(ApiSettings.Font, ApiSettings.MediumTextSize, 'normal', 'italic'),
                                    fg=ApiSettings.Foreground, bg=ApiSettings.Background)
        self.forecast_label.pack(side=TOP, anchor=E)
        self.location_label = Label(self, font=(ApiSettings.Font, ApiSettings.SmallTextSize),
                                    fg=ApiSettings.Foreground, bg=ApiSettings.Background)
        self.location_label.pack(side=TOP, anchor=E)

        if not self.weather_api_token:
            Logger.logging.warning("Please define api token for https://darksky.net/dev "
                                   "weather data will not be available")
            return None

        Logger.logging.debug("Initialization of Weather class")
        self.get_weather()

    def get_weather(self):
        location_info = Network.get_location()
        if self.location_info != location_info:
            self.location_info = location_info

        latitude = self.location_info['lat']
        longitude = self.location_info['lon']

        location = "{1} {2}, {0}".format(self.location_info['country'], self.location_info['city'], self.location_info['zip'])

        try:
            weather_req_url = "https://api.darksky.net/forecast/{0}/{1},{2}?lang={3}&units={4}".format(
                self.weather_api_token, latitude, longitude, self.weather_lang, self.weather_unit)
            response = requests.get(weather_req_url)
            weather_info = json.loads(response.text)
            Logger.logging.debug("request: " + str(weather_req_url) + " response: " + str(response)
                                 + " json: " + str(weather_info))
        except Exception as err:
            Logger.logging.critical("Exception: {0}".format(err))
            return None

        if self.weather_info != weather_info:
            self.weather_info = weather_info
            degree_sign = u'\N{DEGREE SIGN}'
            temperature = "{0}{1}".format(str(int(self.weather_info['currently']['temperature'])), degree_sign)
            currently = self.weather_info['currently']['summary']
            forecast = self.weather_info["hourly"]["summary"]

            icon_id = self.weather_info['currently']['icon']
            self.weather_icon = None
            if icon_id in icons:
                self.weather_icon = icons[icon_id]

            if self.weather_icon is not None:
                image = Image.open(self.weather_icon)
                image = image.resize((100, 100), Image.ANTIALIAS)
                image = image.convert('RGB')
                photo = ImageTk.PhotoImage(image)

                self.icon_label.config(image=photo)
                self.icon_label.image = photo
            else:
                self.icon_label.config(image='')

            self.currently_label.config(text=currently)
            self.forecast_label.config(text=forecast)
            self.temperature_label.config(text=temperature)
            self.location_label.config(text=location)

        Logger.logging.info("get_weather")
        # updates every hour
        self.after(60 * 60 * 1000, self.get_weather)

    @staticmethod
    def convert_kelvin_to_fahrenheit(kelvin_temp):
        return 1.8 * (kelvin_temp - 273) + 32


if __name__ == "__main__":
    pass
