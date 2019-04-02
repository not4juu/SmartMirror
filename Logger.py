import logging as syslogger
import sys

"""Creates a singleton instance for program Logger buffer

Parameters
----------

Returns
-------

"""

initialized = False

def init_logger(outIntoFile=True):

    global logging
    global initialized

    if initialized:
        logging.warning("Logger instance exist!")
        return -1

    logging = syslogger.getLogger(name="SmartMirror_Logger")
    logging.setLevel(level=syslogger.DEBUG)
    logger_formatter = syslogger.Formatter(
        '[%(asctime)s:%(module)s:%(lineno)s:%(levelname)s] %(message)s'
    )

    logger_consolehandler = syslogger.StreamHandler(sys.stdout)
    logger_consolehandler.setLevel(level=syslogger.INFO)
    logger_consolehandler.setFormatter(logger_formatter)
    logging.addHandler(logger_consolehandler)

    if outIntoFile:
        logger_filehandler =  syslogger.FileHandler(filename="smartmirror_logger.log", mode="w")
        logger_filehandler .setLevel(level=syslogger.DEBUG)
        logger_filehandler.setFormatter(logger_formatter)
        logging.addHandler(logger_filehandler)

    initialized = True
    logging.debug("Logger have been created successfully")

    return 0

if __name__ == "__main__":
    pass