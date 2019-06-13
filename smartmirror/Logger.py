import logging as sys_logging
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

    logging = sys_logging.getLogger(name="smartmirror.logger")
    logging.setLevel(level=sys_logging.DEBUG)
    logger_formatter = sys_logging.Formatter(
        '[%(asctime)s:%(threadName)s:%(module)s:%(lineno)s:%(levelname)s] %(message)s')

    logger_console_handler = sys_logging.StreamHandler(sys.stdout)
    logger_console_handler.setLevel(
        level=sys_logging.DEBUG if verbose else sys_logging.INFO)

    logger_console_handler.setFormatter(logger_formatter)
    logging.addHandler(logger_console_handler)

    if logs_to_file:
        logger_file_handler = sys_logging.FileHandler(filename="smartmirror_logger.log", mode="w", encoding='utf-8')
        logger_file_handler.setLevel(level=sys_logging.DEBUG)
        logger_file_handler.setFormatter(logger_formatter)
        logging.addHandler(logger_file_handler)

    initialized = True
    logging.info("Logger has been created successfully outfile: {0} verbose: {1}".format(
        logs_to_file, verbose))

    return 0


Logger = sys_logging.getLogger(name="smartmirror.logger")  # Define Global Logger variable


if __name__ == "__main__":
    pass
