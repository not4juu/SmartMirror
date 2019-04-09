from threading import Lock
from queue import Queue
import argparse
import Logger
from ui_thread import UiThread
from uc_thread import UcThread

"""
    Init program properties
    - set args parameters
    - init Logger buffer into file and std output
"""
def init_properties():
    parser = argparse.ArgumentParser (
        prog = 'smartmirror',
        description = 'Smart Mirror program',
        epilog =  'more detailed information in README.md file https://github.com/not4juu/SmartMirror'
    )
    parser.add_argument("-v", "--verbose", action='count', help='show verbose logs on console')
    parser.add_argument ('--version', action='version', version='%(prog)s 1.0.0')
    args = parser.parse_args()

    Logger.init_logger(outIntoFile=True, verbose=args.verbose)
    Logger.logging.debug('Init properties finish successfully')

"""
    Init program threads:
    - user interface thread
    - user command thread
"""
def init_program_threads():
    program_queue = Queue()
    message_lock = Lock()

    main_ui_thread = UiThread(queue = program_queue, lock = message_lock)
    main_ui_thread.start()
    main_uc_thread = UcThread(queue = program_queue, lock = message_lock)
    main_uc_thread.start()

    program_queue.join()
    Logger.logging.debug('Threads starts successfully')

"""
    Main function calls by program
"""
def main():
    init_properties()
    init_program_threads()

if __name__ == "__main__":
    main()
    Logger.logging.debug('__main__ Ends')
