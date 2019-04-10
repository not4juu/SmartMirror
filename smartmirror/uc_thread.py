from threading import Thread
from glo_messages import GET_MESSAGE

import  Logger
"""
    User Command Thread
"""

class UcThread(Thread):

    def __init__(self,queue,lock):
        Thread.__init__(self, name="UC_Thread")
        self.__message_queue = queue
        self.__lock_queue = lock
        self.__close_thread = False

        Logger.logging.debug("Initialized user command thread")

    def __h_api_window_close(self):
        Logger.logging.debug("Close user command thread")
        self.__close_thread = True

    def __handler(self, message):
        handler = {
            'NETWORK_CONNECTION_FAILURE': self.__h_api_window_close,
            'API_CAMERA_CONNECTION_FAILURE' : self.__h_api_window_close,
            'API_USER_QUIT': self.__h_api_window_close,

        }
        call_handler = handler.get(message,
                           lambda : Logger.logging.debug("Message \"{0}\" no reference handler".format(message)))
        return call_handler()

    def __get_message(self):
        received_message = self.__message_queue.get()
        Logger.logging.debug("Received : {0}".format( GET_MESSAGE(received_message)))
        self.__message_queue.task_done()
        self.__lock_queue.release()
        self.__handler(GET_MESSAGE(received_message))


    def run(self):
        Logger.logging.debug("User_Command thread runs")

        while True:
            self.__get_message()
            if self.__close_thread:
                break

