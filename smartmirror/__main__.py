import argparse

import Logger
from api_window import ApiWindow

"""
    Init program properties
    - set args parameters
    - init Logger buffer into file and std output
"""
def init_properties():
    parser = argparse.ArgumentParser (
        prog = 'smartmirror',
        description = 'Smart Mirror program',
        epilog =  'more detalied information in README.md file https://github.com/not4juu/SmartMirror'
    )
    parser.add_argument("-v", "--verbose", action='count', help='show verbose logs on console')
    parser.add_argument ('--version', action='version', version='%(prog)s 1.0.0')
    args = parser.parse_args()

    Logger.init_logger(outIntoFile=True, verbose=args.verbose)
    Logger.logging.info('Run main')

"""
    Main function calls by program
"""
def main():
    init_properties()
    root = ApiWindow()
    root.tk.mainloop()


if __name__ == "__main__":
    main()
