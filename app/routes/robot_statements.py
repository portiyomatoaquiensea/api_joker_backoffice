
from datetime import datetime
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_dataplayer_db, get_realtime_db
from app.models.dataplayer_models import DwBonusSetting, DwJkBackofficeStatement, DwPlayerAccount, DwDownline, DwPlayerAccountTransaction, DwPlayerDailyReport, DwPlayerDashboard, DwSystemBalance, DwSystemBalanceTransaction
from app.models.realtime_models import DwRobotStatement
from app.schemas.robot_statements import JokerInsertStatementDto
from app.core.security import get_current_token
from app.schemas.response import ResponseDto
from sqlalchemy.exc import SQLAlchemyError

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

    requestBy = dto.requestBy
    # 3. Prepare backoffice statement
    new_backoffice = DwJkBackofficeStatement(
        date_time=dto.dateTime,
        amount=dto.amount,
        request_id=dto.requestId,
        related_username=dto.relatedUsername,
        action=dto.action,
        currency=dto.currency,
        request_by=requestBy,
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
    
    date = (
        datetime.strptime(dto.dateTime, "%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%d")
        if isinstance(dto.dateTime, str)
        else dto.dateTime.strftime("%Y-%m-%d")
    )

    # 5. Check if player exists
    player = db_dataplayer.query(DwPlayerAccount).filter_by(
        wb_id=downline.wb_id,
        wb_code=downline.wb_code,
        downline_id=downline.id,
        downline_code=downline.code,
        player_name=dto.username
    ).first()

    bonus_setting = db_dataplayer.query(DwBonusSetting).filter_by(
        wb_id=downline.wb_id,
        wb_code=downline.wb_code,
        downline_id=downline.id,
        downline_code=downline.code,
        backoffice_user=requestBy,
        backoffice_type='JOKER123',
        active=True
    ).first()
    
    if bonus_setting:
        if bonus_setting.backoffice_account_type in ['CASHBACK', 'BONUS']:
            new_robot.transaction_type = bonus_setting.backoffice_account_type
            new_robot.transaction_status = "APPROVED"

    if player:
        new_robot.player_name = player.player_name
        new_robot.player_status = "OLD_PLAYER"
        new_robot.wb_id = player.wb_id
        new_robot.wb_code = player.wb_code
        new_robot.downline_id = player.downline_id
        new_robot.downline_code = player.downline_code
        new_robot.player_account_id = player.id
        new_robot.player_code = player.player_code

        if bonus_setting:
            if bonus_setting.backoffice_account_type in ['CASHBACK', 'BONUS']:
                system_balance = db_dataplayer.query(DwSystemBalance).filter_by(
                    wb_id=downline.wb_id,
                    wb_code=downline.wb_code,
                    downline_id=downline.id,
                    downline_code=downline.code,
                ).first()
                if not system_balance:
                    return ResponseDto.error(message="Downline Not Found", statusCode=404, data=[])
                
                available_system_balance = system_balance.available_balance
                end_system_balance = system_balance.available_balance - abs(dto.amount)
                
                #Robot USER ID
                ROBOTUSERID = 41
                new_system_balance_transaction = DwSystemBalanceTransaction(
                    system_balance_id=system_balance.id,
                    wb_id=downline.wb_id,
                    wb_code=downline.wb_code,
                    user_id=ROBOTUSERID,
                    downline_id=downline.id,
                    downline_code=downline.code,
                    amount=abs(dto.amount),
                    transaction_type=bonus_setting.backoffice_account_type,
                    begin_balance=available_system_balance,
                    last_balance=end_system_balance,
                    transaction_date=date
                )

                player_balance = player.balance
                end_player_balance = player.balance + abs(dto.amount)
                new_player_account_transaction = DwPlayerAccountTransaction(
                    wb_id=downline.wb_id,
                    wb_code=downline.wb_code,
                    user_id=ROBOTUSERID,
                    downline_id=downline.id,
                    downline_code=downline.code,
                    player_account_id=player.id,
                    player_code=player.player_code,
                    player_name=player.player_name,
                    amount=abs(dto.amount),
                    begin_balance=player_balance,
                    last_balance=end_player_balance,
                    transaction_type=bonus_setting.backoffice_account_type,
                    transaction_action="APPROVED",
                    transaction_date=date
                )
            
                try:
                    # update player balance
                    player.balance += abs(dto.amount)
                    # update system balance
                    system_balance.available_balance = available_system_balance - abs(dto.amount)

                    db_dataplayer.add(new_player_account_transaction)
                    db_dataplayer.add(new_system_balance_transaction)
                    db_dataplayer.commit()
                except SQLAlchemyError as e:
                    db_dataplayer.rollback()
                    return ResponseDto.error(message=f"Failed to create player transaction: {str(e)}", statusCode=500, data=[])

                find_player_dashboard = db_dataplayer.query(DwPlayerDashboard).filter_by(
                    wb_id=downline.wb_id,
                    wb_code=downline.wb_code,
                    downline_id=downline.id,
                    downline_code=downline.code,
                    historical_date=date
                ).first()

                if find_player_dashboard:
                    find_player_dashboard.total_bonus_amount += abs(dto.amount)
                    try:
                        db_dataplayer.commit()
                    except SQLAlchemyError as e:
                        db_dataplayer.rollback()
                        return ResponseDto.error(message=f"Failed to update player dashboard: {str(e)}", statusCode=500, data=[])
                else:
                    new_player_dashboard = DwPlayerDashboard(
                        wb_id=downline.wb_id,
                        wb_code=downline.wb_code,
                        downline_id=downline.id,
                        downline_code=downline.code,
                        historical_date=date,
                        total_bonus_amount=abs(dto.amount)
                    )
                    try:
                        db_dataplayer.add(new_player_dashboard)
                        db_dataplayer.commit()
                    except SQLAlchemyError as e:
                        db_dataplayer.rollback()
                        return ResponseDto.error(message=f"Failed to create player dashboard: {str(e)}", statusCode=500, data=[])
                    
                find_player_daily_report = db_dataplayer.query(DwPlayerDailyReport).filter_by(
                    wb_id=downline.wb_id,
                    wb_code=downline.wb_code,
                    downline_id=downline.id,
                    downline_code=downline.code,
                    report_date=date
                ).first()
            
                if find_player_daily_report:
                    find_player_daily_report.total_bonus_amount += abs(dto.amount)
                    try:
                        db_dataplayer.commit()
                    except SQLAlchemyError as e:
                        db_dataplayer.rollback()
                        return ResponseDto.error(message=f"Failed to update player daily report: {str(e)}", statusCode=500, data=[])
                else:
                    new_player_dashboard = DwPlayerDailyReport(
                        wb_id=downline.wb_id,
                        wb_code=downline.wb_code,
                        downline_id=downline.id,
                        downline_code=downline.code,
                        report_date=date,
                        total_bonus_amount=abs(dto.amount)
                    )
                    try:
                        db_dataplayer.add(new_player_dashboard)
                        db_dataplayer.commit()
                    except SQLAlchemyError as e:
                        db_dataplayer.rollback()
                        return ResponseDto.error(message=f"Failed to create player dashboard: {str(e)}", statusCode=500, data=[])

    # 6. Save both
    try:
        db_dataplayer.add(new_backoffice)
        db_realtime.add(new_robot)
        db_dataplayer.commit()
        db_realtime.commit()
    except SQLAlchemyError as e:
        db_dataplayer.rollback()
        db_realtime.rollback()
        return ResponseDto.error(message=f"Failed to Statement inserted: {str(e)}", statusCode=500, data=[])

    return ResponseDto.success(data={"requestId": dto.requestId}, message="Statement inserted successfully")