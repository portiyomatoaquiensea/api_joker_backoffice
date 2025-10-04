from sqlalchemy import BigInteger, Column, ForeignKey, Integer, SmallInteger, String, DateTime, Numeric, Boolean, Date, func
from app.core.database import BaseDataplayer
from sqlalchemy.dialects.postgresql import TIMESTAMP

class DwJkBackofficeStatement(BaseDataplayer):
    __tablename__ = "dw_jk_backoffice_statements"

    id = Column(Integer, primary_key=True, autoincrement=True)
    date_time = Column(DateTime, nullable=False)
    amount = Column(Numeric(10, 2), nullable=False)
    request_id = Column(String(50), nullable=False, unique=True)
    related_username = Column(String(50), nullable=False)
    action = Column(String(20), nullable=False)
    currency = Column(String(3), nullable=False)
    request_by = Column(String(50), nullable=False)
    username = Column(String(50), nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    modified_at = Column(DateTime, server_default=func.now(), onupdate=func.now())


class DwPlayerAccount(BaseDataplayer):
    __tablename__ = "dw_player_accounts"

    id = Column(Integer, primary_key=True, autoincrement=True)
    wb_id = Column(Integer, nullable=False)
    wb_code = Column(String(50), nullable=False)
    downline_id = Column(Integer, nullable=False)
    downline_code = Column(String(50), nullable=False)
    player_code = Column(String(26), nullable=False)
    player_name = Column(String(255), nullable=False)
    phone_number = Column(String(255), nullable=True)
    balance = Column(Numeric(15, 4), nullable=False)
    deleted = Column(Integer, nullable=False, default=0)
    active = Column(Integer, nullable=False, default=1)
    register_date = Column(Date, nullable=False)
    created = Column(DateTime, server_default=func.now())
    modified = Column(DateTime, server_default=func.now(), onupdate=func.now())
    nickname = Column(String(250), nullable=True)

    def to_dict(self):
        return {
            "id": self.id,
            "wb_id": self.wb_id,
            "wb_code": self.wb_code,
            "downline_id": self.downline_id,
            "downline_code": self.downline_code,
            "player_code": self.player_code,
            "player_name": self.player_name,
            "phone_number": self.phone_number,
            "balance": float(self.balance),
            "deleted": bool(self.deleted),
            "active": bool(self.active),
            "register_date": self.register_date.isoformat() if self.register_date else None,
            "created": self.created.isoformat() if self.created else None,
            "modified": self.modified.isoformat() if self.modified else None,
            "nickname": self.nickname
        }


class DwDownline(BaseDataplayer):
    __tablename__ = "dw_downlines"

    id = Column(Integer, primary_key=True, autoincrement=True)
    wb_id = Column(Integer, nullable=False)
    wb_code = Column(String(50), nullable=False)
    code = Column(String(50), nullable=False)
    name = Column(String(255), nullable=False)
    _order = Column(Integer, nullable=True)
    active = Column(Boolean, default=True)
    created = Column(DateTime, server_default=func.now())
    modified = Column(DateTime, server_default=func.now(), onupdate=func.now())

class DwRobotBackofficeMember(BaseDataplayer):
    __tablename__ = "dw_robot_backoffice_members"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    username = Column(String(50), nullable=False)
    nickname = Column(String(255))
    firstname = Column(String(255))
    lastname = Column(String(255))
    type = Column(String(50))
    created_time = Column(DateTime)
    last_login = Column(DateTime)
    login_ip = Column(String(50))
    created_at = Column(DateTime, server_default=func.now())
    modified_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    robot_status = Column(Boolean, server_default="false")
    wb_id = Column(SmallInteger)
    wb_code = Column(String)
    user_id = Column(SmallInteger)
    downline_id = Column(SmallInteger)
    downline_code = Column(String)

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "nickname": self.nickname,
            "firstname": self.firstname,
            "lastname": self.lastname,
            "type": self.type,
            "created_time": self.created_time,
            "last_login": self.last_login,
            "login_ip": self.login_ip,
            "created_at": self.created_at,
            "modified_at": self.modified_at,
            "robot_status": self.robot_status,
            "wb_id": self.wb_id,
            "wb_code": self.wb_code,
            "user_id": self.user_id,
            "downline_id": self.downline_id,
            "downline_code": self.downline_code
        }
    
class DwPlayerHistoricalTransaction(BaseDataplayer):
    __tablename__ = "dw_player_historical_transactions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    wb_id = Column(Integer, nullable=False)
    wb_code = Column(String(50), nullable=False)
    user_id = Column(Integer, nullable=False)
    downline_id = Column(Integer, nullable=False)
    downline_code = Column(String(50), nullable=False)
    player_account_id = Column(Integer, nullable=False)
    player_code = Column(String(255), nullable=False)  # FIXED
    player_name = Column(String(255), nullable=False)
    historical_type = Column(String(255), nullable=False)  # FIXED
    historical_date = Column(Date, nullable=False)
    created = Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False)  # FIXED
    modified = Column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)  # FIXED
    amount = Column(Numeric(15, 4), nullable=False, server_default="0.0000")  # FIXED

    def to_dict(self):
        return {
            "id": self.id,
            "wb_id": self.wb_id,
            "wb_code": self.wb_code,
            "user_id": self.user_id,
            "downline_id": self.downline_id,
            "downline_code": self.downline_code,
            "player_account_id": self.player_account_id,
            "player_code": self.player_code,
            "player_name": self.player_name,
            "amount": float(self.amount) if self.amount is not None else 0.0,
            "historical_type": self.historical_type,
            "historical_date": self.historical_date.strftime("%Y-%m-%d") if self.historical_date else None,
            "created": self.created.strftime("%Y-%m-%d %H:%M:%S") if self.created else None,
            "modified": self.modified.strftime("%Y-%m-%d %H:%M:%S") if self.modified else None,
        }
    
class DwPlayerDashboard(BaseDataplayer):
    __tablename__ = "dw_player_dashboards"

    id = Column(Integer, primary_key=True, autoincrement=True)
    wb_id = Column(Integer, nullable=False)
    wb_code = Column(String(50), nullable=False)
    downline_id = Column(Integer, nullable=False)
    downline_code = Column(String(50), nullable=False)
    total_register = Column(Numeric, nullable=False, default=0)
    total_play = Column(Numeric, nullable=False, default=0)
    total_player_active = Column(Numeric, nullable=False, default=0)
    total_player_deposit = Column(Numeric, nullable=False, default=0)
    total_player_withdraw = Column(Numeric, nullable=False, default=0)
    total_deposit_amount = Column(Numeric(15, 4), nullable=False, default=0.0)
    total_withdraw_amount = Column(Numeric(15, 4), nullable=False, default=0.0)
    total_disbursement_amount = Column(Numeric(15, 4), nullable=False, default=0.0)
    total_deposit_adjustment_amount = Column(Numeric(15, 4), nullable=False, default=0.0)
    total_withdraw_adjustment_amount = Column(Numeric(15, 4), nullable=False, default=0.0)
    daily_available_balance = Column(Numeric(15, 4), nullable=False, default=0.0)
    daily_available_balance_previous_day = Column(Numeric(15, 4), nullable=False, default=0.0)
    historical_date = Column(Date, nullable=False)
    total_topup_amount = Column(Numeric(15, 4), nullable=False, default=0.0)
    total_credit_amount = Column(Numeric(15, 4), nullable=False, default=0.0)
    total_debit_amount = Column(Numeric(15, 4), nullable=False, default=0.0)
    total_expense_amount = Column(Numeric(15, 5), nullable=False, server_default="0.00000")
    total_bonus_amount = Column(Numeric(15, 5), nullable=False, server_default="0.00000")
    created = Column(DateTime(timezone=True), server_default=func.now())
    modified = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    def to_dict(self):
        return {
            "id": self.id,
            "wb_id": self.wb_id,
            "wb_code": self.wb_code,
            "downline_id": self.downline_id,
            "downline_code": self.downline_code,
            "total_register": float(self.total_register) if self.total_register is not None else 0.0,
            "total_play": float(self.total_play) if self.total_play is not None else 0.0,
            "total_player_active": float(self.total_player_active) if self.total_player_active is not None else 0.0,
            "total_player_deposit": float(self.total_player_deposit) if self.total_player_deposit is not None else 0.0,
            "total_player_withdraw": float(self.total_player_withdraw) if self.total_player_withdraw is not None else 0.0,
            "total_deposit_amount": float(self.total_deposit_amount) if self.total_deposit_amount is not None else 0.0,
            "total_withdraw_amount": float(self.total_withdraw_amount) if self.total_withdraw_amount is not None else 0.0,
            "total_disbursement_amount": float(self.total_disbursement_amount) if self.total_disbursement_amount is not None else 0.0,
            "total_deposit_adjustment_amount": float(self.total_deposit_adjustment_amount) if self.total_deposit_adjustment_amount is not None else 0.0,
            "total_withdraw_adjustment_amount": float(self.total_withdraw_adjustment_amount) if self.total_withdraw_adjustment_amount is not None else 0.0,
            "daily_available_balance": float(self.daily_available_balance) if self.daily_available_balance is not None else 0.0,
            "daily_available_balance_previous_day": float(self.daily_available_balance_previous_day) if self.daily_available_balance_previous_day is not None else 0.0,
            "historical_date": self.historical_date.isoformat() if self.historical_date else None,
            "total_topup_amount": float(self.total_topup_amount) if self.total_topup_amount is not None else 0.0,
            "total_credit_amount": float(self.total_credit_amount) if self.total_credit_amount is not None else 0.0,
            "total_debit_amount": float(self.total_debit_amount) if self.total_debit_amount is not None else 0.0,
            "total_expense_amount": float(self.total_expense_amount) if self.total_expense_amount is not None else 0.0,
            "total_bonus_amount": float(self.total_bonus_amount) if self.total_bonus_amount is not None else 0.0,
            "created": self.created.isoformat() if self.created else None,
            "modified": self.modified.isoformat() if self.modified else None,
        }
    
class DwBonusSetting(BaseDataplayer):
    __tablename__ = "dw_bonus_settings"

    id = Column(Integer, primary_key=True, autoincrement=True)
    wb_id = Column(Integer, nullable=False)
    wb_code = Column(String(50), nullable=False)
    downline_id = Column(Integer, nullable=False)
    downline_code = Column(String(50), nullable=False)
    backoffice_user = Column(String(10), nullable=False)
    backoffice_type = Column(String(50), nullable=True)
    backoffice_account_type = Column(String(50), nullable=True)
    active = Column(Boolean, nullable=False, server_default="false")
    created = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    modified = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "wb_id": self.wb_id,
            "wb_code": self.wb_code,
            "downline_id": self.downline_id,
            "downline_code": self.downline_code,
            "backoffice_user": self.backoffice_user,
            "backoffice_type": self.backoffice_type,
            "backoffice_account_type": self.backoffice_account_type,
            "active": self.active,
            "created": self.created,
            "modified": self.modified
        }
    
class DwSystemBalance(BaseDataplayer):
    __tablename__ = "dw_system_balances"

    id = Column(Integer, primary_key=True, autoincrement=True)
    wb_id = Column(Integer, nullable=False)
    wb_code = Column(String(50), nullable=False)
    downline_id = Column(Integer, nullable=False)
    downline_code = Column(String(50), nullable=False)
    available_balance = Column(Numeric(15, 4), nullable=False, server_default="0.0000")
    created = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    modified = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "wb_id": self.wb_id,
            "wb_code": self.wb_code,
            "downline_id": self.downline_id,
            "downline_code": self.downline_code,
            "available_balance": float(self.available_balance) if self.available_balance is not None else 0.0,
            "created": self.created,
            "modified": self.modified,
        }
    
class DwSystemBalanceTransaction(BaseDataplayer):
    __tablename__ = "dw_system_balance_transactions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    wb_id = Column(Integer, nullable=False)
    wb_code = Column(String(50), nullable=False)
    user_id = Column(Integer, nullable=False)
    downline_id = Column(Integer, nullable=False)
    downline_code = Column(String(50), nullable=False)
    amount = Column(Numeric(15, 4), nullable=False, server_default="0.0000")
    transaction_type = Column(String(50), nullable=False)
    begin_balance = Column(Numeric(15, 4), nullable=False, server_default="0.0000")
    last_balance = Column(Numeric(15, 4), nullable=False, server_default="0.0000")
    transaction_date = Column(Date, nullable=False)
    created = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    modified = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    # Foreign key to DwSystemBalance
    system_balance_id = Column(Integer, ForeignKey("dw_system_balances.id"), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "wb_id": self.wb_id,
            "wb_code": self.wb_code,
            "user_id": self.user_id,
            "downline_id": self.downline_id,
            "downline_code": self.downline_code,
            "amount": float(self.amount) if self.amount is not None else 0.0,
            "transaction_type": self.transaction_type,
            "begin_balance": float(self.begin_balance) if self.begin_balance is not None else 0.0,
            "last_balance": float(self.last_balance) if self.last_balance is not None else 0.0,
            "transaction_date": self.transaction_date,
            "created": self.created,
            "modified": self.modified,
            "system_balance_id": self.system_balance_id,
        }
    
class DwPlayerAccountTransaction(BaseDataplayer):
    __tablename__ = "dw_player_account_transactions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    wb_id = Column(Integer, nullable=False)
    wb_code = Column(String(50), nullable=False)
    user_id = Column(Integer, nullable=False)
    downline_id = Column(Integer, nullable=False)
    downline_code = Column(String(50), nullable=False)
    player_account_id = Column(Integer, nullable=False)
    player_code = Column(String(255), nullable=False)
    player_name = Column(String(255), nullable=False)
    amount = Column(Numeric(15, 4), nullable=False, server_default="0.0000")
    begin_balance = Column(Numeric(15, 4), nullable=False, server_default="0.0000")
    last_balance = Column(Numeric(15, 4), nullable=False, server_default="0.0000")
    transaction_type = Column(String(50), nullable=False)
    transaction_action = Column(String(50), nullable=False)
    transaction_date = Column(Date, nullable=False)
    created = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    modified = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    player_bank_account_id = Column(Integer)
    player_deposit_bank_account = Column(String(255))
    operator_bank_account_id = Column(Integer)
    operator_deposit_bank_account = Column(String(255))
    operator_bank_id = Column(Integer)

    def to_dict(self):
        return {
            "id": self.id,
            "wb_id": self.wb_id,
            "wb_code": self.wb_code,
            "user_id": self.user_id,
            "downline_id": self.downline_id,
            "downline_code": self.downline_code,
            "player_account_id": self.player_account_id,
            "player_code": self.player_code,
            "player_name": self.player_name,
            "amount": float(self.amount) if self.amount is not None else 0.0,
            "begin_balance": float(self.begin_balance) if self.begin_balance is not None else 0.0,
            "last_balance": float(self.last_balance) if self.last_balance is not None else 0.0,
            "transaction_type": self.transaction_type,
            "transaction_action": self.transaction_action,
            "transaction_date": self.transaction_date,
            "created": self.created,
            "modified": self.modified,
            "player_bank_account_id": self.player_bank_account_id,
            "player_deposit_bank_account": self.player_deposit_bank_account,
            "operator_bank_account_id": self.operator_bank_account_id,
            "operator_deposit_bank_account": self.operator_deposit_bank_account,
            "operator_bank_id": self.operator_bank_id,
        }
    

class DwPlayerDailyReport(BaseDataplayer):
    __tablename__ = "dw_player_daily_reports"

    id = Column(Integer, primary_key=True, autoincrement=True)
    wb_id = Column(Integer, nullable=False)
    wb_code = Column(String(50), nullable=False)
    downline_id = Column(Integer, nullable=False)
    downline_code = Column(String(50), nullable=False)
    total_deposit_amount = Column(Numeric(15, 4), nullable=False, server_default="0.0000")
    total_withdraw_amount = Column(Numeric(15, 4), nullable=False, server_default="0.0000")
    total_disbursement_amount = Column(Numeric(15, 4), nullable=False, server_default="0.0000")
    total_deposit_adjustment_amount = Column(Numeric(15, 4), nullable=False, server_default="0.0000")
    daily_available_balance = Column(Numeric(15, 4), nullable=False, server_default="0.0000")
    daily_available_balance_previous_day = Column(Numeric(15, 4), nullable=False, server_default="0.0000")
    report_date = Column(Date, nullable=False)
    created = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    modified = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    total_withdraw_adjustment_amount = Column(Numeric(15, 5), nullable=False, server_default="0.00000")
    total_topup_amount = Column(Numeric(15, 4), nullable=False, server_default="0.0000")
    total_credit_amount = Column(Numeric(15, 4), nullable=False, server_default="0.0000")
    total_debit_amount = Column(Numeric(15, 4), nullable=False, server_default="0.0000")
    total_expense_amount = Column(Numeric(15, 5), nullable=False, server_default="0.00000")
    total_bonus_amount = Column(Numeric(15, 5), nullable=False, server_default="0.00000")

    def to_dict(self):
        return {
            "id": self.id,
            "wb_id": self.wb_id,
            "wb_code": self.wb_code,
            "downline_id": self.downline_id,
            "downline_code": self.downline_code,
            "total_deposit_amount": float(self.total_deposit_amount) if self.total_deposit_amount is not None else 0.0,
            "total_withdraw_amount": float(self.total_withdraw_amount) if self.total_withdraw_amount is not None else 0.0,
            "total_disbursement_amount": float(self.total_disbursement_amount) if self.total_disbursement_amount is not None else 0.0,
            "total_deposit_adjustment_amount": float(self.total_deposit_adjustment_amount) if self.total_deposit_adjustment_amount is not None else 0.0,
            "daily_available_balance": float(self.daily_available_balance) if self.daily_available_balance is not None else 0.0,
            "daily_available_balance_previous_day": float(self.daily_available_balance_previous_day) if self.daily_available_balance_previous_day is not None else 0.0,
            "report_date": self.report_date,
            "created": self.created,
            "modified": self.modified,
            "total_withdraw_adjustment_amount": float(self.total_withdraw_adjustment_amount) if self.total_withdraw_adjustment_amount is not None else 0.0,
            "total_topup_amount": float(self.total_topup_amount) if self.total_topup_amount is not None else 0.0,
            "total_credit_amount": float(self.total_credit_amount) if self.total_credit_amount is not None else 0.0,
            "total_debit_amount": float(self.total_debit_amount) if self.total_debit_amount is not None else 0.0,
            "total_expense_amount": float(self.total_expense_amount) if self.total_expense_amount is not None else 0.0,
            "total_bonus_amount": float(self.total_bonus_amount) if self.total_bonus_amount is not None else 0.0,
        }