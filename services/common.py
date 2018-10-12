import logging
from logging.handlers import RotatingFileHandler
import random
import string


def create_log_file(log_name, log_level):
    """
    creates a rotating log file
    :param log_name:
    :param log_level:
    :return:
    """
    logger = logging.getLogger("Rotating log")
    logger.setLevel(log_level)

    # add a rotating file handler
    handler = RotatingFileHandler(log_name, maxBytes=15000, backupCount=2)
    logger.addHandler(handler)

    return logger


def generate_random_code(length=8):
    """
    generate random characters of length matching input length
    :param length:
    :return:
    """
    return ''.join(random.choice(string.ascii_uppercase + string.digits + string.punctuation) for _ in range(length))

