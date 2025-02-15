"""
fieldtype
=============

同花顺的API参数.

Functions:
-----------
TBD

Usage:
------
TBD

Author:
-------
Bruce Li (jiangwlee@163.com)

Version:
--------
0.0.1
"""

from enum import Enum


# 定义参数类型
class FieldType(Enum):
	CHANGE_RATE = 199112,  # 涨幅
	LATEST = 10,  # 最新价格
	REASON_TYPE = 9001,  # 涨停原因
	FIRST_LIMIT_UP_TIME = 330323,  # 首次涨停时间
	LAST_LIMIT_UP_TIME = 330324,  # 最终涨停时间
	LIMIT_UP_TYPE = 330325,  # 涨停类型
	FIRST_LIMIT_DOWN_TIME = 330333, # 首次跌停时间
	LAST_LIMIT_DOWN_TIME = 330334, # 最终跌停时间
	OPEN_NUM = 9002,  # 打开次数
	HIGH_DAYS_VALUE = 330329,  # 几天几板
	ORDER_VOLUME = 133971,  # 封单量
	ORDER_AMOUNT = 133970,  # 封单金额
	TURNOVER_RATE = 1968584,  # 换手率
	CURRENCY_VALUE = 3475914,  # 流通市值
	LIMIT_UP_SUC_RATE = 9003,  # 开板次数


common_types = [
	FieldType.LATEST,
	FieldType.CHANGE_RATE,
]