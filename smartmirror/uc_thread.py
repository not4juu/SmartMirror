from threading import Thread
from glo_messages import GET_MESSAGE
import  Logger

import time
"""
    User Command Thread
"""

class UcThread(Thread):

    def __init__(self,queue,lock):
        Thread.__init__(self, name="UC_Thread")
        self.__queue = queue
        self.__lock = lock
        Logger.logging.debug("Initialized user command thread")

    def __get_queue(self):
        receive_message = self.__queue.get()
        Logger.logging.debug("Receives : {0}".format( GET_MESSAGE(receive_message)))
        self.__queue.task_done()
        self.__lock.release()


    def run(self):
        Logger.logging.debug("User_Command thread runs")

        while True:
            time.sleep(0.1)
            self.__get_queue()