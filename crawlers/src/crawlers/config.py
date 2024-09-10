import os
import logging
from logging.handlers import RotatingFileHandler

##########################################
# 日志配置
##########################################

# 日志格式
FORMATTER = logging.Formatter('%(asctime)s - %(name)s - %(module)s - %(levelname)s - %(message)s')

# 文件日志格式
FILE_HANDLER = None
if os.name == 'posix':
    LOGFILE = '/var/log/smartrade/crawlers.log'
    FILE_HANDLER = RotatingFileHandler(LOGFILE, maxBytes=1024*1024, backupCount=3)
    FILE_HANDLER.setFormatter(FORMATTER)

# 命令行日志
CONSOLE_HANDLER = logging.StreamHandler()
CONSOLE_HANDLER.setFormatter(FORMATTER)
CONSOLE_HANDLER.setLevel(logging.DEBUG)

##########################################
# 数据库配置
##########################################
DB_HOST="localhost"
DB_USER="jfsok"
DB_PASSWORD="iTbpamPcUYeqkY9k63rQ"
DB_DATABASE="smartrade"
DB_CONFIG = {
    "user": DB_USER,
    "password": DB_PASSWORD,
    "host": DB_HOST,
    "database": DB_DATABASE
}