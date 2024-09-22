"""
预测结果.
"""
from pydantic import BaseModel, Field

class PredResult(BaseModel):
    date: str = Field(..., description="日期")
    code: str = Field(..., description="股票代码")
    name: str = Field(..., description="股票名称")
    change_rate: str = Field(..., description="竞价涨幅")
    pred: str = Field(..., description="预测结果")
    pred_label: int = Field(..., description="预测标签: 0 - 涨停; 1 - 断板")
    pred_prob: str = Field(..., description="预测概率")

