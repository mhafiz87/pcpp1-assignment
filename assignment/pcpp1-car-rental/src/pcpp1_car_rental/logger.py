import logging
import re
import sys
from pathlib import Path

from colored import Fore, Style

from .singleton import Singleton

LOG_FILE = Path(__file__).parent.joinpath("logger.log")
LOG_FILE_ERROR = Path(__file__).parent.joinpath("logger_error.log")
LOG_FORMAT_1 = "%(asctime)s | %(levelname)s | %(name)s - %(filename)s - %(lineno)s - %(funcName)s | %(process)d >>> %(message)s"
LOG_FORMAT_2 = "%(asctime)s | %(levelname)s | %(filename)s >>> %(message)s"
DATE_FORMAT = "%Y-%m-%dT%H:%M:%SZ"


# https://stackoverflow.com/questions/48782529/exclude-ansi-escape-sequences-from-output-log-file
# Custom Logging Formatter To Remove ANSI Escape Characters
class TermEscapeCodeFormatter(logging.Formatter, metaclass=Singleton):
    """A class to strip the escape codes from the"""

    def __init__(self, fmt=None, datefmt=None, style="%", validate=True):
        super().__init__(fmt, datefmt, style, validate)

    def format(self, record):
        escape_re = re.compile(r"\x1b\[[0-9;]*m")
        record.msg = re.sub(escape_re, "", str(record.msg))
        return super().format(record)

# Define Logger Format
stream_handler_format = logging.Formatter(fmt=LOG_FORMAT_2, datefmt=DATE_FORMAT)
file_handler_format = TermEscapeCodeFormatter(fmt=LOG_FORMAT_2, datefmt=DATE_FORMAT)

# Setting up handler which logs to a stdout even debug level messages
stdout_handler_all = logging.StreamHandler(sys.stdout)
stdout_handler_all.setLevel(logging.DEBUG)
stdout_handler_all.setFormatter(stream_handler_format)

# Setting up handler which logs to a file even debug level messages
file_handler_all = logging.FileHandler(LOG_FILE)
file_handler_all.setLevel(logging.DEBUG)
file_handler_all.setFormatter(file_handler_format)

# Setting up handler which logs to a file from error level messages
file_handler_error = logging.FileHandler(LOG_FILE_ERROR)
file_handler_error.setLevel(logging.WARNING)
file_handler_error.setFormatter(file_handler_format)

# Create Logger
logger = logging.getLogger("logger_learn")
logger.setLevel(level=logging.WARNING)

# Adding Handler To Logger
logger.addHandler(stdout_handler_all)
logger.addHandler(file_handler_all)
logger.addHandler(file_handler_error)