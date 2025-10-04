
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_dataplayer_db, get_realtime_db
from app.models.dataplayer_models import DwPlayerAccount, DwPlayerDashboard, DwPlayerHistoricalTransaction, DwRobotBackofficeMember
from app.schemas.robot_get_members import RobotGetMemberDto
from app.core.security import get_current_token
from app.schemas.response import ResponseDto
from app.schemas.robot_update_members import RobotUpdateMemberDto
from app.services.player_service import PlayerService
from datetime import datetime, date
from sqlalchemy.exc import SQLAlchemyError

router = APIRouter()

def parse_datetime(value: str):
    if value and value.strip() != "":
        return datetime.fromisoformat(value)  # or use your string format
    return None

@router.post("/dw/robot/get/member", tags=["Robot Get Member"])
def get_robot_member(
    dto: RobotGetMemberDto,
    token: str = Depends(get_current_token),
    db_dataplayer: Session = Depends(get_dataplayer_db)
):
    downline_code = dto.downlineCode
    find_robot_member = db_dataplayer.query(DwRobotBackofficeMember).filter_by(
        downline_code=downline_code,
        robot_status=False
    ).all()
    
    if not find_robot_member:
        return ResponseDto.error(message="Robot member is not found", statusCode=200, data=[])
    
    data = [m.to_dict() for m in find_robot_member]
    return ResponseDto.success(data=data, message="successfully")


@router.put("/dw/robot/update/member", tags=["Robot Update Member"])
def update_robot_member(
    dto: RobotUpdateMemberDto,
    token: str = Depends(get_current_token),
    db_dataplayer: Session = Depends(get_dataplayer_db)
):
    # Extract values from DTO
    downline_code = dto.downlineCode
    username = dto.username
    nickname = dto.nickname
    member_type = dto.type
    first_name = dto.firstName
    last_name = dto.lastName
    created_time = dto.createdTime
    last_login = dto.lastLogin
    login_ip = dto.loginIP

    # Step 1: Find robot member
    find_robot_member = db_dataplayer.query(DwRobotBackofficeMember).filter_by(
        downline_code=downline_code,
        username=username,
        robot_status=False
    ).first()

    if not find_robot_member:
        return ResponseDto.error(message="Robot member is not found", statusCode=200, data=[])

    # Step 2: Update robot member first
    try:
        find_robot_member.nickname = nickname
        find_robot_member.firstname = first_name
        find_robot_member.lastname = last_name
        find_robot_member.type = member_type
        find_robot_member.created_time = parse_datetime(created_time)
        find_robot_member.last_login = parse_datetime(last_login)
        find_robot_member.login_ip = login_ip
        find_robot_member.robot_status = True

        db_dataplayer.commit()  # commit robot member update
    except SQLAlchemyError as e:
        db_dataplayer.rollback()
        return ResponseDto.error(message=f"Failed to update robot member: {str(e)}", statusCode=500, data=[])

    # Step 3: Prepare IDs
    wb_id = find_robot_member.wb_id
    wb_code = find_robot_member.wb_code
    downline_id = find_robot_member.downline_id
    user_id = find_robot_member.user_id

    # Step 4: Check if DwPlayerAccount already exists
    find_member_account = db_dataplayer.query(DwPlayerAccount).filter_by(
        wb_id=wb_id,
        wb_code=wb_code,
        downline_id=downline_id,
        downline_code=downline_code,
        player_name=username
    ).first()

    if find_member_account:
        # Robot member updated, account exists — just return success
        return ResponseDto.success(
            data=[], 
            message="Robot member updated, but DwPlayerAccount already exists"
        )

    # Step 5: Generate player code and register_date
    service = PlayerService(db_dataplayer)
    player_code = service.generate_player_code(downline_code)

    register_date = (
        datetime.strptime(created_time, "%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%d")
        if isinstance(created_time, str)
        else created_time.strftime("%Y-%m-%d")
    )

    # Step 6: Create DwPlayerAccount
    new_member_account = DwPlayerAccount(
        wb_id=wb_id,
        wb_code=wb_code,
        downline_id=downline_id,
        downline_code=downline_code,
        player_code=player_code,
        player_name=username,
        phone_number='',
        balance=0.00,
        deleted=False,
        active=True,
        register_date=register_date,
        nickname=first_name
    )

    try:
        db_dataplayer.add(new_member_account)
        db_dataplayer.commit()
    except SQLAlchemyError as e:
        db_dataplayer.rollback()
        return ResponseDto.error(message=f"Failed to create member account: {str(e)}", statusCode=500, data=[])

    new_member_account_id = new_member_account.id

    # Step 7: Update or create dashboard
    find_player_dashboard = db_dataplayer.query(DwPlayerDashboard).filter_by(
        wb_id=wb_id,
        wb_code=wb_code,
        downline_id=downline_id,
        downline_code=downline_code,
        historical_date=register_date
    ).first()

    find_player_historical = db_dataplayer.query(DwPlayerHistoricalTransaction).filter_by(
        wb_id=wb_id,
        wb_code=wb_code,
        downline_id=downline_id,
        downline_code=downline_code,
        player_account_id=new_member_account_id,
        player_code=player_code,
        player_name=username,
        historical_type='REGISTER'
    ).first()

    if find_player_dashboard:
        if not find_player_historical:
            find_player_dashboard.total_register += 1
            try:
                db_dataplayer.commit()
            except SQLAlchemyError as e:
                db_dataplayer.rollback()
                return ResponseDto.error(message=f"Failed to update player dashboard: {str(e)}", statusCode=500, data=[])
    else:
        new_player_dashboard = DwPlayerDashboard(
            wb_id=wb_id,
            wb_code=wb_code,
            downline_id=downline_id,
            downline_code=downline_code,
            historical_date=register_date,
            total_register=1
        )
        try:
            db_dataplayer.add(new_player_dashboard)
            db_dataplayer.commit()
        except SQLAlchemyError as e:
            db_dataplayer.rollback()
            return ResponseDto.error(message=f"Failed to create player dashboard: {str(e)}", statusCode=500, data=[])

    # Step 8: Create historical transaction
    new_player_historical = DwPlayerHistoricalTransaction(
        wb_id=wb_id,
        wb_code=wb_code,
        user_id=user_id,
        downline_id=downline_id,
        downline_code=downline_code,
        player_account_id=new_member_account_id,
        player_code=player_code,
        player_name=username,
        historical_type='REGISTER',
        historical_date=register_date,
        amount=0.00
    )
    try:
        db_dataplayer.add(new_player_historical)
        db_dataplayer.commit()
    except SQLAlchemyError as e:
        db_dataplayer.rollback()
        return ResponseDto.error(message=f"Failed to create player historical transaction: {str(e)}", statusCode=500, data=[])

    return ResponseDto.success(data=[], message="Successfully updated robot member and created new member account")