from pydantic import BaseModel, Field
from typing import Any

class HttpResp(BaseModel):
    code: int = Field(..., description="HTTP Response Code")
    data: Any = Field(..., description="HTTP Response Data")
    msg: str = Field(..., description="HTTP Response Message")

class DatePair(BaseModel):
    start: str = Field(..., description="Start date in %YYYYMMDD format")
    end: str = Field(..., description="Start date in %YYYYMMDD format")