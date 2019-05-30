import logging as syslogger
import sys

"""
Creates a singleton instance for program Logger buffer
"""
initialized = False


def init_logger(logs_to_file=True, verbose=False):

    global logging
    global initialized

    if initialized:
        logging.warning("Logger instance exist!")
        return -1

    logging = syslogger.getLogger(name="SmartMirror_Logger")
    logging.setLevel(level=syslogger.DEBUG)
    logger_formatter = syslogger.Formatter(
        '[%(asctime)s:%(threadName)s:%(module)s:%(lineno)s:%(levelname)s] %(message)s')

    logger_console_handler = syslogger.StreamHandler(sys.stdout)
    logger_console_handler.setLevel(
        level=syslogger.DEBUG if verbose else syslogger.INFO)

    logger_console_handler.setFormatter(logger_formatter)
    logging.addHandler(logger_console_handler)

    if logs_to_file:
        logger_file_handler = syslogger.FileHandler(filename="smartmirror_logger.log", mode="w", encoding='utf-8')
        logger_file_handler.setLevel(level=syslogger.DEBUG)
        logger_file_handler.setFormatter(logger_formatter)
        logging.addHandler(logger_file_handler)

    initialized = True
    logging.info("Logger has been created successfully outfile: {0} verbose: {1}".format(
        logs_to_file, verbose))

    return 0


if __name__ == "__main__":
    pass
