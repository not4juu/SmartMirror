from threading import Thread
from  glo_messages import GLO_MSG
import  Logger

from api_window import ApiWindow
"""
    User Interface Thread
"""

class UiThread(Thread):

    def __init__(self,queue,lock):
        Thread.__init__(self, name="UI_Thread")
        self.__queue = queue
        self.__lock = lock

        self.__window_initialized = False
        self.__api_window = None

        Logger.logging.debug("Initialized user interface thread")

    def __put_queue(self, send_message):
        self.__lock.acquire()
        self.__queue.put(GLO_MSG[send_message])
        Logger.logging.debug("Sends : {0}".format(send_message))

    def __run_api_window(self):
        if not self.__window_initialized:
            self.__api_window = ApiWindow()
            self.__window_initialized = True
            self.__put_queue('API_WINDOW_INITIALIZED')

        self.__api_window.tk.update_idletasks()
        self.__api_window.tk.update()

    def run(self):
        Logger.logging.debug("User_Interface thread runs")

        for i in range(100):
            self.__put_queue('AUTHORIZATION_COMPLETE')
            self.__run_api_window()

def video_collector(root):
    Logger.logging.info("video_collector")
