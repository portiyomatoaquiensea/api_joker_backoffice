from sqlalchemy import Column, Integer, String, DateTime, Numeric, Boolean, func
from app.core.database import BaseRealtime

class DwRobotStatement(BaseRealtime):
    __tablename__ = "dw_robot_statements"

    id = Column(Integer, primary_key=True, autoincrement=True)
    wb_id = Column(Integer, nullable=True)
    wb_code = Column(String(50), nullable=True)
    user_id = Column(Integer, nullable=True)
    user_lock = Column(String(50), nullable=True)
    downline_id = Column(Integer, nullable=True)
    downline_code = Column(String(50), nullable=True)
    player_status = Column(String(50), nullable=True)
    player_account_id = Column(Integer, nullable=True)
    player_code = Column(String(255), nullable=True)
    player_name = Column(String(255), nullable=True)
    player_bank_account_id = Column(Integer, nullable=True)
    player_deposit_bank_account = Column(String(255), nullable=True)
    operator_bank_account_id = Column(Integer, nullable=True)
    operator_deposit_bank_account = Column(String(255), nullable=True)
    operator_bank_id = Column(Integer, nullable=True)
    amount = Column(Numeric(15, 4), nullable=False, default=0)
    transaction_type = Column(String(50), nullable=False)
    transaction_status = Column(String(50), nullable=False)
    transaction_date = Column(DateTime, nullable=False)
    transaction_reference = Column(String(255), nullable=False)
    transaction_belong = Column(String(50), nullable=False)
    created = Column(DateTime, server_default=func.now())
    modified = Column(DateTime, server_default=func.now(), onupdate=func.now())
    is_locked = Column(Boolean, default=False)
