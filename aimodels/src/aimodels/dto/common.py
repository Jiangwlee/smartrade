from pydantic import BaseModel, Field
from typing import Any

class HttpResp(BaseModel):
    code: int = Field(..., description="HTTP Response Code")
    data: Any = Field(..., description="HTTP Response Data")
    msg: str = Field(..., description="HTTP Response Message")