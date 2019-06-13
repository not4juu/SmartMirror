import unittest
from threading import Lock
from queue import Queue
from smartmirror.glo_messages import GLO_MSG
from smartmirror.messages_handler import MessagesHandler


class TestMessagesHandler(unittest.TestCase):

    def test_class_object(self):
        obj = MessagesHandler(Queue(), Lock())
        self.assertEqual(type(obj), MessagesHandler)

    def test_receiving_message(self):
        obj = MessagesHandler(Queue(), Lock())
        self.assertEqual(obj.get_message(), None)

    def test_sending_message(self):
        obj = MessagesHandler(Queue(), Lock())
        self.assertEqual(obj.send_message(GLO_MSG['NO_ERROR']), None)

    def test_communication_message(self):
        obj = MessagesHandler(Queue(), Lock())
        obj.send_message(GLO_MSG['NO_ERROR'])
        self.assertEqual(obj.get_message(), GLO_MSG['NO_ERROR'])


if __name__ == '__main__':
    unittest.main()
