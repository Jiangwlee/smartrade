from pydantic import BaseModel, Field

class ChangeRankInfo(BaseModel):
    code: str = Field(..., description="股票代码")
    name: str = Field(..., description="股票名称")
    change: str = Field(..., description="涨幅")