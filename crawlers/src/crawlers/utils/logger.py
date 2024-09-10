import os
import logging
from crawlers.config import CONSOLE_HANDLER, FILE_HANDLER

def getLogger(module: str = ""):
    logger = logging.getLogger('smartcrawler')
    logger.addHandler(CONSOLE_HANDLER)
    if os.name == 'posix':
        logger.addHandler(FILE_HANDLER)
    logger.setLevel(logging.DEBUG)
    return logger