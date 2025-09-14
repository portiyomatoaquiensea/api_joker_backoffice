from pydantic import BaseModel

class RobotGetMemberDto(BaseModel):
    downlineCode: str
