from argparse import ArgumentParser
from threading import Lock
from queue import Queue
from smartmirror.messages_handler import MessagesHandler
from smartmirror.ui_thread import UiThread
from smartmirror.uc_thread import UcThread
import smartmirror.Logger as Logger

"""
    Init program properties
    - set args parameters
    - init Logger buffer into file and std output
"""


def init_properties():
    parser = ArgumentParser(
        prog='smartmirror',
        description='Smart Mirror program',
        epilog='more detailed information in README.md file https://github.com/not4juu/SmartMirror'
    )
    parser.add_argument('-v', '--verbose', action='count', help='show verbose logs on console')
    parser.add_argument('--version', action='version', version='%(prog)s 1.0.0')
    args = parser.parse_args()

    Logger.init_logger(logs_to_file=True, verbose=args.verbose)
    Logger.logging.debug('Init properties finish successfully')


"""
    Init program threads:
    - user interface thread
    - user command thread
"""


def init_program_threads():
    message_queue = Queue()
    message_locker = Lock()
    message_handler = MessagesHandler(messages_queue=message_queue, messages_locker=message_locker)

    main_ui_thread = UiThread(messages_handler=message_handler)
    main_ui_thread.start()
    main_uc_thread = UcThread(messages_handler=message_handler)
    main_uc_thread.start()

    message_queue.join()
    Logger.logging.debug('Threads starts successfully')


"""
    Main function calls by program
"""


def main():
    init_properties()
    init_program_threads()


if __name__ == "__main__":
    main()
    Logger.logging.info(__name__ + " ends")
