from smartmirror.glo_messages import GET_MESSAGE
import smartmirror.Logger as Logger
import time
"""
    MessagesHandler class
    - manages program communication based on defined messages,
    - implements some security approaches, 
    - lets only one message to be sends by pipeline (queue) utilizing a lock features 
"""

class MessagesHandler(object):

    def __init__(self, messages_queue, messages_locker):
        self.__messages_queue = messages_queue
        self.__messages_locker =  messages_locker
        Logger.logging.debug("Initialized a Messages Handler object")
    """
        Sends (put) the message into queue and lock the queue until somone will pick up it
    """
    def send_message(self, message_id):
        self.__messages_locker.acquire()
        self.__messages_queue.put(message_id)
        Logger.logging.debug("Sends : {0}".format(GET_MESSAGE(message_id)))
        return None
    """
        Gets message from queue if queue is not empty, release locker for another message which will be adds
        and recives a value of message
        When queue is empty return None value
    """
    def get_message(self):
        if not self.__messages_queue.empty():
            message_id = self.__messages_queue.get()
            Logger.logging.debug("Received : {0}".format(GET_MESSAGE(message_id)))
            self.__messages_queue.task_done()
            self.__messages_locker.release()
            return message_id
        return None
    """
        Due to a user interface thread and user command thread can sends and receives at the same time. 
        There can be case when this same thread recives its message then thread puts it again and 
        runs wait timer to let other thread to pick it up
        
        It is some protection case - does not let program infinite loop
    """
    def send_message_again(self,message_id):
        Logger.logging.debug (
            "Message \"{0}\" no reference handler".format(GET_MESSAGE(message_id)))
        self.send_message(message_id)
        time.sleep(0.05)
        return None

if __name__ == "__main__":
    pass
