from pydantic import BaseModel
from datetime import datetime
from decimal import Decimal

class JokerInsertStatementDto(BaseModel):
    downlineCode: str
    dateTime: datetime
    amount: Decimal
    requestId: str
    relatedUsername: str
    action: str
    currency: str
    requestBy: str
    username: str
