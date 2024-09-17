import os
import logging
from logging.handlers import RotatingFileHandler

##########################################
# 日志配置
##########################################

# 日志格式
FORMATTER = logging.Formatter('[%(levelname)-8s] - %(asctime)s - %(name)s - %(module)-14s| %(message)s')

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
# 工作目录配置
##########################################

WORK_DIR = os.path.join(os.path.expanduser("~"), "smartrade", "ai")
MODEL_DIR = os.path.join(WORK_DIR, "models")
DATA_SET = os.path.join(WORK_DIR, "dataset")
# 预测数据目录
PRED_DIR = os.path.join(DATA_SET, "pred")
PRED_DATASET = os.path.join(PRED_DIR, "dataset")
PRED_RESULT = os.path.join(PRED_DIR, "results")
# 评估数据目录
EVAL_DIR = os.path.join(DATA_SET, "eval")
EVAL_DATASET = os.path.join(EVAL_DIR, "dataset")
EVAL_RESULT = os.path.join(EVAL_DIR, "results")
for p in [PRED_DATASET, PRED_RESULT, EVAL_DATASET, EVAL_RESULT]:
    if not os.path.exists(p):
        os.makedirs(p, mode=0o666)