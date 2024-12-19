from pydantic import BaseModel, ConfigDict, Field
from typing import Optional, List
from datetime import date, datetime

class StockHangQingInfo(BaseModel):
    model_config = ConfigDict(populate_by_name=True) #允许使用字段原名初始化

    code: Optional[str] = Field("", description="股票代码")
    name: Optional[str] = Field("", description="股票名称")
    time: int = Field(..., description="日期", alias="nTime")
    index: int = Field(..., description="索引", alias="nIndex")
    amount: int = Field(..., description="成交额", alias="llValue")
    volume: int = Field(..., description="成交量", alias="llVolume")
    avg_price: int = Field(..., description="均价", alias="nAvgPx")
    high_price: int = Field(..., description="最高价", alias="nHighPx")
    low_price: int = Field(..., description="最低价", alias="nLowPx")
    open_price: int = Field(..., description="开盘价", alias="nOpenPx")
    close_price: int = Field(..., description="收盘价", alias="nLastPx")
    pre_close_price: int = Field(..., description="昨日收盘价", alias="nPreClosePx")


class LongHuItem(BaseModel):
    branchCode: int = Field(..., description="券商营业部代码")
    branchName: str = Field(..., description="券商营业部名称")
    enddate: date = Field(..., description="结束日期，格式为 'YYYY-MM-DD'")
    stockid: int = Field(..., description="股票ID")
    stockcode: str = Field(..., description="股票代码")
    stockname: str = Field(..., description="股票名称")
    market: int = Field(..., description="市场相关标识（具体含义需根据业务确定）")
    tclose: float = Field(..., description="收盘价")
    chngPct: float = Field(..., description="涨跌幅百分比")
    value: float = Field(..., description="某个金额数值（具体含义需根据业务确定）")
    tvalue: float = Field(..., description="另一个金额数值（具体含义需根据业务确定）")
    bvalue: float = Field(..., description="买入金额数值（具体含义需根据业务确定）")
    bratio: float = Field(..., description="买入比例（具体含义需根据业务确定）")
    svalue: float = Field(..., description="卖出金额数值（具体含义需根据业务确定）")
    sratio: float = Field(..., description="卖出比例（具体含义需根据业务确定）")
    netvalue: float = Field(..., description="净值（具体含义需根据业务确定）")
    netratio: float = Field(..., description="净值比例（具体含义需根据业务确定）")
    infoClsCode: int = Field(..., description="信息分类代码")
    infoClsName: str = Field(..., description="信息分类名称")
    infoClsNameList: List[str] = Field(..., description="信息分类名称列表")
    inputtime: datetime = Field(..., description="输入时间，格式为 'YYYY-MM-DD HH:MM:SS'")

class LongHuInfo(BaseModel):
    name: str = Field(..., description="游资名称")
    items: List[LongHuItem] = Field(..., description="最近20个交易日的上榜信息")