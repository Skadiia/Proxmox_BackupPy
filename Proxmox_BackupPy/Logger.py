#!/usr/bin/env python
# -.- coding: utf-8 -.-

import logging
from logging.handlers import RotatingFileHandler
import datetime

def init_logger():
        logger = logging.getLogger()
        logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s :: %(levelname)s :: %(message)s')
        file_handler = RotatingFileHandler('backup-%s.log'%(), 'a', 2000000, 1)
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        steam_handler = logging.StreamHandler()
        steam_handler.setLevel(logging.DEBUG)
        logger.addHandler(steam_handler)

        return logger
