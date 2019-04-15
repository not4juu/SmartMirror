from threading import Thread
from glo_messages import GET_MESSAGE
from glo_messages import GLO_MSG
from command_recognition import  CommandRecognition
import  Logger
import time
"""
    User Command Thread
"""

class UcThread(Thread):

    def __init_command_recognition(self):
        Logger.logging.debug ("Initialize command recogniton class")
        self.__command_recognition = CommandRecognition()
        if not self.__command_recognition.api_state_ok():
            self.__close_thread = True
        Logger.logging.debug ("Command recogniton class state: {0}".format (
            self.__command_recognition.get_state_info ()
        ))
        self.__send_message(self.__command_recognition.get_state_info())

    def __init__(self,queue,lock):
        Thread.__init__(self, name="UC_Thread")
        self.__message_queue = queue
        self.__lock_queue = lock
        self.__close_thread = False

        #self. __init_command_recognition()
        self.__network_initialized = False
        self.__window_initialized = False
        Logger.logging.debug("Initialized user command thread")

    def __send_message(self, send_message):
        self.__lock_queue.acquire()
        self.__message_queue.put(GLO_MSG[send_message])
        Logger.logging.debug("Sends : {0}".format(send_message))

    def __get_message(self):
        if not  self.__message_queue.empty():
            received_message = self.__message_queue.get()
            Logger.logging.debug("Received : {0}".format(GET_MESSAGE(received_message)))
            self.__message_queue.task_done()
            self.__lock_queue.release()
            self.__handler(GET_MESSAGE(received_message))

    """
        If a message is not handle by this thread it shoudl be send handle for other one
        put it again to queque and sleep for a while - it let pick up the message by  
        proper receiver
    """
    def __put_message_again(self,message):
        Logger.logging.debug (
            "Message \"{0}\" no reference handler".format (message))
        self.__send_message(message)
        time.sleep(0.05)

    def __handler(self, message):
        handler = {
            'NETWORK_CONNECTION_FAILURE': self.__h_api_window_close,
            'API_CAMERA_CONNECTION_FAILURE': self.__h_api_window_close,
            'API_USER_QUIT': self.__h_api_window_close,
            'NETWORK_CONNECTION_SUCCESS' : self.__h_network_success,
            'API_WINDOW_INITIALIZED' : self.__h_window_success,
        }
        call_handler = handler.get (message,
                                    lambda: self.__put_message_again(message))
        return call_handler ()

    def __h_network_success(self):
        self.__network_initialized = True
        return
    def __h_window_success(self):
        self.__window_initialized = True
        return

    def __h_api_window_close(self):
        Logger.logging.debug("Close user command thread")
        self.__close_thread = True
        return

    def __wait_for_init(self):
        Logger.logging.debug ("Wait for init network and window")
        while not self.__window_initialized or not self.__network_initialized:
            self.__get_message()
            if self.__close_thread:
                break
        if  self.__window_initialized and self.__network_initialized:
            self.__init_command_recognition()

    def run(self):
        Logger.logging.debug("User_Command thread runs")
        self.__wait_for_init()
        while True:
            self.__get_message()
            if self.__close_thread:
                Logger.logging.debug ("User_Command thread ends")
                break

