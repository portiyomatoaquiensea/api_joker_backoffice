
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_dataplayer_db, get_realtime_db
from app.models.dataplayer_models import DwJkBackofficeStatement, DwPlayerAccount, DwDownline
from app.models.realtime_models import DwRobotStatement
from app.schemas.robot_statements import JokerInsertStatementDto
from app.core.security import get_current_token
from datetime import datetime
from app.schemas.response import ResponseDto

router = APIRouter()

@router.post("/dw/joker/insert/statement", tags=["Joker Statements"])
def joker_insert_statement(
    dto: JokerInsertStatementDto,
    token: str = Depends(get_current_token),
    db_dataplayer: Session = Depends(get_dataplayer_db),
    db_realtime: Session = Depends(get_realtime_db)
):
    # 1. Check if request_id already exists
    existing = db_dataplayer.query(DwJkBackofficeStatement).filter_by(
        request_id=dto.requestId,
        request_by=dto.requestBy
    ).first()
    if existing:
        return ResponseDto.error(message="Already Taken", statusCode=404, data=[])

    # 2. Validate downline
    downline = db_dataplayer.query(DwDownline).filter_by(code=dto.downlineCode).first()
    if not downline:
        return ResponseDto.error(message="Downline Not Found", statusCode=404, data=[])

    # 3. Prepare backoffice statement
    new_backoffice = DwJkBackofficeStatement(
        date_time=dto.dateTime,
        amount=dto.amount,
        request_id=dto.requestId,
        related_username=dto.relatedUsername,
        action=dto.action,
        currency=dto.currency,
        request_by=dto.requestBy,
        username=dto.username,
    )

    # 4. Prepare robot statement
    new_robot = DwRobotStatement(
        wb_id=downline.wb_id,
        wb_code=downline.wb_code,
        downline_id=downline.id,
        downline_code=downline.code,
        player_name=dto.username,
        player_status="NEW_PLAYER",
        transaction_type="DEPOSIT" if dto.action.upper() != "WITHDRAW" else "WITHDRAW",
        transaction_status="PENDING",
        transaction_belong="IS_MEMBER",
        transaction_reference=dto.requestId,
        transaction_date=dto.dateTime,
        amount=abs(float(dto.amount)),
    )

    # 5. Check if player exists
    player = db_dataplayer.query(DwPlayerAccount).filter_by(
        downline_code=dto.requestBy, player_name=dto.username
    ).first()

    if player:
        new_robot.player_name = player.player_name
        new_robot.player_status = "OLD_PLAYER"
        new_robot.wb_id = player.wb_id
        new_robot.wb_code = player.wb_code
        new_robot.downline_id = player.downline_id
        new_robot.downline_code = player.downline_code
        new_robot.player_account_id = player.id
        new_robot.player_code = player.player_code

    # 6. Save both
    db_dataplayer.add(new_backoffice)
    db_dataplayer.commit()

    db_realtime.add(new_robot)
    db_realtime.commit()

    return ResponseDto.success(data={"requestId": dto.requestId}, message="Statement inserted successfully")