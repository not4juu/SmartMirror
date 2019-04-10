from threading import Thread
from glo_messages import GLO_MSG
from api_window import ApiWindow
from network import Network

import  Logger
"""
    User Interface Thread
"""

class UiThread(Thread):

    def __init__(self,queue,lock):
        Thread.__init__(self, name="UI_Thread")
        self.__message_queue = queue
        self.__lock_queue = lock

        self.__close_thread = not Network.enabled()
        self.__send_message(Network.get_status())

        self.__window = None

        Logger.logging.debug("Initialized user interface thread")

    def __send_message(self, send_message):
        self.__lock_queue.acquire()
        self.__message_queue.put(GLO_MSG[send_message])
        Logger.logging.debug("Sends : {0}".format(send_message))

    def __init_window(self):
        self.__window = ApiWindow()
        self.__send_message(self.__window.get_state_info())
        return

    def __run_window(self):
        if not self.__window.api_state_ok():
            Logger.logging.debug("Close user interface thread : \"{0}\"".format(self.__window.get_state_info()))
            self.__close_thread = True
            self.__send_message(self.__window.get_state_info())
        self.__window.refresh()
        return

    def run(self):
        Logger.logging.debug("User_Interface thread runs")
        self.__init_window()

        while True:
            if self.__close_thread:
                break

            self.__run_window()



