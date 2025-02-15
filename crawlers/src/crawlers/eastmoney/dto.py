from pydantic import BaseModel, Field

class StockRankInfo(BaseModel):
    sc: str = Field(..., description="股票代码")
    rk: int = Field(..., description="当前排行")
    rc: int = Field(..., description="排行变化")
    hisRc: int = Field(..., description="历史排行变化")

"""
股票净流入/流出信息.
"""
class StockNetAmountInfo(BaseModel):
    code: str = Field(..., alias="f12")
    name: str = Field(..., alias="f14")
    net_amount: float = Field(..., alias="f62")
    big_order_net_amount: float = Field(..., description="大单净额", alias="f66")
    big_order_rate: float = Field(..., description="大单占比", alias="f69")