from pydantic import BaseModel
from datetime import datetime
from decimal import Decimal

class RobotGetMemberDto(BaseModel):
    downlineCode: str
