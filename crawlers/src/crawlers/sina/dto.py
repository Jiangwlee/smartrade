from pydantic import BaseModel, Field

class AmountRankInfo(BaseModel):
    code: str = Field(..., description="股票代码")
    name: str = Field(..., description="股票名称")
    volume: int = Field(..., description="成交量")
    amount: int = Field(..., description="成交金额")