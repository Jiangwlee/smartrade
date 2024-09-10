"""
dto (Data transfer object)
=============

本模块提供了同花顺的数据传输对象结构.

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

from pydantic import BaseModel, Field
from typing import List, Optional

"""
每日涨跌停汇总.
"""
class StockDailySummary(BaseModel):
    num: int = Field(..., description="最终涨跌停股票数量")
    history_num: int = Field(..., description="触及涨跌停股票数量")
    rate: float = Field(..., description="封板率")
    open_num: int = Field(..., description="打开涨跌停的股票数量")

"""
每日同比汇总.
"""
class StockDayOverDaySummary(BaseModel):
    today: StockDailySummary
    yesterday: StockDailySummary
    
class LimitDownStockModel(BaseModel):
    code: str = Field(..., description="股票代码")
    name: str = Field(..., description="股票名称")
    change_rate: float = Field(..., description="涨幅")
    last_limit_down_time: str = Field(..., description="最后一次跌停时间")
    first_limit_down_time: str = Field(..., description="首次跌停时间")
    turnover_rate: float = Field(..., description="换手率")
    market_type: str = Field(..., description="市场类型, HS 代表沪深")
    currency_value: int = Field(..., description="流通市值")

class PageInfo(BaseModel):
    limit: int = Field(..., description="每页包含的股票数量限制")
    total: int = Field(..., description="全部股票数量")
    count: int = Field(..., description="总页数")
    page: int = Field(..., description="当前是第几页")

class LimitDownRespDataModel(BaseModel):
    page: PageInfo
    info: List[LimitDownStockModel]
    limit_up_count: StockDayOverDaySummary
    limit_down_count: StockDayOverDaySummary
    date: str


class LimitUpStockModel(BaseModel):
    code: str = Field(..., description="股票代码")
    name: str = Field(..., description="股票名称")
    change_rate: float = Field(..., description="涨幅")
    last_limit_up_time: str = Field(..., description="最后一次涨停时间")
    first_limit_up_time: str = Field(..., description="首次涨停时间")
    turnover_rate: float = Field(..., description="换手率")
    market_type: str = Field(..., description="市场类型, HS 代表沪深")
    currency_value: int = Field(..., description="流通市值")
    open_num: Optional[int] = Field(..., description="打开涨停次数")
    limit_up_type: str = Field(..., description="涨停板类型")
    order_volume: int = Field(..., description="封单量")
    order_amount: float = Field(..., description="封单金额")
    limit_up_suc_rate: Optional[float] = Field(..., description="封板成功率")
    reason_type: Optional[str] = Field(..., description="涨停原因")
    high_days: str = Field(..., description="几天几板")

class LimitUpRespDataModel(BaseModel):
    page: PageInfo
    info: List[LimitUpStockModel]
    limit_up_count: StockDayOverDaySummary
    limit_down_count: StockDayOverDaySummary
    date: str
