from typing import List
from pydantic import BaseModel

def rowsToModels(rows: List[tuple], model: BaseModel) -> List[BaseModel]:
    """
    将数据库返回的 Tuple 结果转换成 BaseModel.
    --
    @param rows: 数据库返回的查询结果列表
    @param model: 目标模型
    """
    return [model(**dict(zip(model.model_fields.keys(), row))) for row in rows]