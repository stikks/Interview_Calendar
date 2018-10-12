import logging

from .common import create_log_file


# create logs for info and error log levels
info_log = create_log_file('rotating_info.log', logging.INFO)
error_log = create_log_file('rotating_error.log', logging.ERROR)
