import socket
from smartmirror.glo_messages import GLO_MSG
import smartmirror.Logger as Logger
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
            Logger.logging.debug("Internet connection enabled")
            return True
        except socket.error as socket_error:
            network_status = GLO_MSG['NETWORK_CONNECTION_FAILURE']
            Logger.logging.critical("Internet connection disabled socket.error : {0}".format(socket_error))
            return False
        except OSError as ose_error:
            network_status = GLO_MSG['NETWORK_CONNECTION_FAILURE']
            Logger.logging.critical("Internet connection disabled OSError : {0}".format(ose_error))
            return False
        except Exception as err:
            network_status = GLO_MSG['NETWORK_CONNECTION_FAILURE']
            Logger.logging.critical("Internet connection disabled exception : {0}".format(err))
            return False

    @staticmethod
    def get_status():
        return network_status


if __name__ == "__main__":
    pass
