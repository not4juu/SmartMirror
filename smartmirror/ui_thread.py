from threading import Thread
from glo_messages import GLO_MSG
from glo_messages import GET_MESSAGE
from api_window import ApiWindow
from network import Network

import  Logger
import time
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

    def __get_message(self):
        if not self.__message_queue.empty():
            received_message = self.__message_queue.get()
            Logger.logging.debug("Received : {0}".format(GET_MESSAGE(received_message)))
            self.__message_queue.task_done()
            self.__lock_queue.release()
            self.__handler(GET_MESSAGE(received_message))

    """
        If a message is not handle by this thread it shoudl be send handle for other one
        put it again to queque and sleep for a while - it let pick up the message by  
        proper receiver
        TODO: check if common function can be hold by one module
    """
    def __put_message_again(self,message):
        Logger.logging.debug (
            "Message \"{0}\" no reference handler".format (message))
        self.__send_message(message)
        time.sleep(0.05)

    def __handler(self, message):
        handler = {
            'MICROPHONE_FAILURE': self.__h_microphone_failure,
            'MICROPHONE_INITIALIZED' : self.__h_microphone_initialized,
        }
        call_handler = handler.get (message,
                                    lambda: self.__put_message_again(message))
        return call_handler ()

    def __h_microphone_failure(self):
        self.__close_thread = True
        return

    def __h_microphone_initialized(self):
        return



    def __init_window(self):
        self.__window = ApiWindow()
        Logger.logging.debug ("Command recogniton class state: {0}".format (
            self.__window.get_state_info ()
        ))
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
                Logger.logging.debug ("User_Interface thread ends")
                break
            self.__run_window()
            self.__get_message()




