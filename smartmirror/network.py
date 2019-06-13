import socket
import requests
import json
from smartmirror.glo_messages import GLO_MSG
from smartmirror.Logger import Logger
"""
    Network Class
"""


class Network(object):
    """
    Host: 8.8.8.8 (google-public-dns-a.google.com)
    OpenPort: 53/tcp
    Timeout in seconds : 3
    Service: domain (DNS/TCP)

    Class find out a accessibility to network by Google's public DNS servers
    """
    network_status = GLO_MSG['NO_ERROR']

    def __init__(self):
        pass

    @staticmethod
    def enabled():
        global network_status
        try:
            socket.setdefaulttimeout(3)
            socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect(("8.8.8.8", 53))
            network_status = GLO_MSG['NETWORK_CONNECTION_SUCCESS']
            Logger.debug("Internet connection enabled")
            return True
        except socket.error as socket_error:
            network_status = GLO_MSG['NETWORK_CONNECTION_FAILURE']
            Logger.critical("Internet connection disabled socket.error : {0}".format(socket_error))
            return False
        except OSError as ose_error:
            network_status = GLO_MSG['NETWORK_CONNECTION_FAILURE']
            Logger.critical("Internet connection disabled OSError : {0}".format(ose_error))
            return False
        except Exception as err:
            network_status = GLO_MSG['NETWORK_CONNECTION_FAILURE']
            Logger.critical("Internet connection disabled exception : {0}".format(err))
            return False

    @staticmethod
    def get_status():
        return network_status

    @staticmethod
    def get_ip():
        try:
            ip_reg_url = "http://jsonip.com/"
            response = requests.get(ip_reg_url)
            ip_json = json.loads(response.text)
            Logger.debug("request: " + str(ip_reg_url) + " response: " + str(response)
                                 + " json: " + str(ip_json))
            return ip_json['ip']
        except Exception as err:
            Logger.critical("Exception: {0}".format(err))
            return None

    @staticmethod
    def get_location():
        try:
            location_req_url = "http://ip-api.com/json/{0}".format(Network.get_ip())
            response = requests.get(location_req_url)
            location_json = json.loads(response.text)
            Logger.debug("request: " + str(location_req_url) + " response: " + str(response)
                                 + " json: " + str(location_json))
            return location_json
        except Exception as err:
            Logger.critical("Exception: {0}".format(err))
            return None


if __name__ == "__main__":
    pass
