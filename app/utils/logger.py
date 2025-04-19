import logging
from logging import Logger

def setup_logger(logger_level):
    """setup logger with level
    :param logger_level:
    :type logger_level: String
    """

    logger = logging.getLogger()
    handler = logging.StreamHandler()
    handler.setFormatter(
        logging.Formatter('%(asctime)s %(name)-8s %(levelname)-8s %(message)s [%(filename)s:%(lineno)d]'))
    logger.addHandler(handler)
    logger.setLevel(logger_level)
    return logger
