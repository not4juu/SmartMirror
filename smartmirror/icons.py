import os
import sys

PATH = os.path.dirname(os.path.realpath(__file__))
if sys.platform != 'linux':
    PATH = PATH.replace("\\", '/')

"""
    Icons dictionary definition

    icons have been downloaded from: https://icons8.com/
"""

icons = {
    # Api menu icons
    "news": PATH + "/icons/news.png",
    "camera_disabled": PATH + "/icons/camera_disabled.png",
    "camera_enabled": PATH + "/icons/camera_enabled.png",
    "microphone_disabled": PATH + "/icons/microphone_disabled.png",
    "microphone_enabled": PATH + "/icons/microphone_enabled.png",
    "wifi_disabled": PATH + "/icons/wifi_disabled.png",
    "wifi_enabled": PATH + "/icons/wifi_enabled.png",
    # Weather icons
    "clear-day": PATH + "/icons/weather/clear_day.png",
    "clear-night": PATH + "/icons/weather/clear_night.png",
    "rain": PATH + "/icons/weather/rain.png",
    "snow": PATH + "/icons/weather/snow.png",
    "sleet": PATH + "/icons/weather/sleet.png",
    "wind": PATH + "/icons/weather/wind.png",
    "fog": PATH + "/icons/weather/fog.png",
    "cloudy": PATH + "/icons/weather/cloudy.png",
    "partly-cloudy-day": PATH + "/icons/weather/partly_cloudy_day.png",
    "partly-cloudy-night": PATH + "/icons/weather/partly_cloudy_night.png",
    "hail": PATH + "/icons/weather/hail.png",
    "thunderstorm": PATH + "/icons/weather/thunderstorm.png",
    "tornado": PATH + "/icons/weather/tornado.png"
}
