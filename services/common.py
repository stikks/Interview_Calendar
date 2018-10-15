import logging
from logging.handlers import RotatingFileHandler
import random
import string
import json
from datetime import datetime, date, time

from flask import jsonify


class InvalidUsage(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        # rv['message'] = self.message
        rv["errors"] = [dict(status=self.status_code, detail=self.message)]
        return rv


class DateTimeEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime) or isinstance(o, date) or isinstance(o, time):
            return o.isoformat()

        return json.JSONEncoder.default(self, o)


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


def success_response(message, status_code):
    """
    return json response
    :param message
    :param status_code
    """
    response = jsonify(message)
    response.status_code = status_code
    return response


def populate_object(obj, **kwargs):
    """
    populate object with matching data from kwargs
    :param obj
    :param kwargs
    :return:
    """
    for k, v in kwargs.items():
        if hasattr(obj, k) and v is not None:
            setattr(obj, k, v)

    return obj


