from typing import Optional
from pydantic import BaseModel

class RobotUpdateMemberDto(BaseModel):
    downlineCode: str
    username: str
    nickname: Optional[str] = None
    type: Optional[str] = None
    firstName: Optional[str] = None
    lastName: Optional[str] = None
    createdTime: Optional[str] = None
    lastLogin: Optional[str] = None
    loginIP: Optional[str] = None

