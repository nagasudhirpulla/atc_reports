import logging
from logging import Logger

appLogger: Logger = logging.getLogger()


def initAppLogger() -> Logger:
    global appLogger
    # set app logger name and minimum logging level
    appLogger = logging.getLogger()
    appLogger.setLevel(logging.INFO)

    # configure console logging
    streamHandler = logging.StreamHandler()
    appLogger.addHandler(streamHandler)
    return appLogger


def getAppLogger() -> Logger:
    global appLogger
    return appLogger
