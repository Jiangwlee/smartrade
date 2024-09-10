from pydantic import BaseModel, Field

class StockRankInfo(BaseModel):
    sc: str = Field(..., description="股票代码")
    rk: int = Field(..., description="当前排行")
    rc: int = Field(..., description="排行变化")
    hisRc: int = Field(..., description="历史排行变化")