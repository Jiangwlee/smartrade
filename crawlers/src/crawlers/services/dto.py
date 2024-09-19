from typing import List, Optional
from typing_extensions import Annotated
from pydantic import BaseModel, Field, BeforeValidator
from datetime import datetime, date as date_type

NULLABLE_STRING = Annotated[str, BeforeValidator(lambda v: "" if v is None else v)]

class BlockSummayDto(BaseModel):
    """板块概况
    """
    code: str = Field(..., description="板块代码")
    name: str = Field(..., description="板块名称")
    date: date_type = Field(..., description="日期")
    change_rate: float = Field(..., description="板块涨幅")
    limit_up_num: int = Field(..., description="板块涨停家数")
    high: str = Field(..., description="板块最高高度")
    stock_list: str = Field(..., description="股票列表")
    rank_position: int = Field(..., description="板块排名")

class LimitUpDetailsDto(BaseModel):
    code: str = Field(..., description="股票代码")
    name: str = Field(..., description="股票名称")
    date: date_type = Field(..., description="涨停日期")
    currency_value: int = Field(..., description="流通市值")
    turnover_rate: float = Field(..., description="换手率")
    first_limit_up_time: datetime = Field(..., description="首次涨停时间")
    last_limit_up_time: datetime = Field(..., description="最后涨停时间")
    open_num: int = Field(..., description="打开次数")
    limit_up_type: str = Field(..., description="封板类型")
    order_volume: float = Field(..., description="封单量")
    order_amount: float = Field(..., description="封单金额")
    high_days: str = Field(..., description="几天几板")
    reason_type: NULLABLE_STRING = Field(..., description="涨停原因")
    reason_info: NULLABLE_STRING = Field(..., description="涨停详情")
    block_ids: NULLABLE_STRING = Field(..., description="板块ID")
    blocks: Optional[List[BlockSummayDto]] = Field([], description="板块概要")
