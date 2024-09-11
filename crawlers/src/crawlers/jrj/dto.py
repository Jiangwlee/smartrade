from pydantic import BaseModel, Field
from typing import Optional

class StockHangQingInfo(BaseModel):
    code: Optional[str] = Field("", description="股票代码")
    date: int = Field(..., description="日期", alias="nTime")
    index: int = Field(..., description="索引", alias="nIndex")
    amount: int = Field(..., description="成交额", alias="llValue")
    volume: int = Field(..., description="成交量", alias="llVolume")
    avg_price: int = Field(..., description="均价", alias="nAvgPx")
    high_price: int = Field(..., description="最高价", alias="nHighPx")
    low_price: int = Field(..., description="最低价", alias="nLowPx")
    open_price: int = Field(..., description="开盘价", alias="nOpenPx")
    close_price: int = Field(..., description="收盘价", alias="nLastPx")
    pre_close_price: int = Field(..., description="昨日收盘价", alias="nPreClosePx")
