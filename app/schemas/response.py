from typing import Any
from pydantic import BaseModel

class ResponseDto(BaseModel):
    message: str
    statusCode: int
    data: Any = None

    @classmethod
    def success(cls, data: Any = None, message: str = "Success"):
        return cls(message=message, statusCode=200, data=data)

    @classmethod
    def error(cls, message: str = "Error", statusCode: int = 400, data: Any = None):
        return cls(message=message, statusCode=statusCode, data=data)
