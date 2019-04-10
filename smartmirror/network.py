import socket
import Logger

class Network(object):

    def __init__(self):
        self.__network_status ='NO_ERROR'
    """
    Host: 8.8.8.8 (google-public-dns-a.google.com)
    OpenPort: 53/tcp
    Timeout in seconds : 3
    Service: domain (DNS/TCP)
    """
    @classmethod
    def enabled(self):
        try:
            socket.setdefaulttimeout(3)
            socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect(("8.8.8.8", 53))
            self.__network_status = 'NETWORK_CONNECTION_SUCCESS'
            Logger.logging.debug("Internet connection enabled")
            return True
        except socket.error as err:
            self.__network_status = 'NETWORK_CONNECTION_FAILURE'
            Logger.logging.critical("Internet connection disabled : socket.error")
            return False
        except OSError as err:
            self.__network_status = 'NETWORK_CONNECTION_FAILURE'
            Logger.logging.critical("Internet connection disabled : OSError")
            return False
        except Exception as err:
            self.__network_status = 'NETWORK_CONNECTION_FAILURE'
            Logger.logging.critical("Internet connection disabled : Exception")
            return False

    @classmethod
    def get_status(self):
        return self.__network_status

