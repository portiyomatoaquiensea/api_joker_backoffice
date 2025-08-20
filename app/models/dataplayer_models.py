from sqlalchemy import Column, Integer, String, DateTime, Numeric, Boolean, Date, func
from app.core.database import BaseDataplayer

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
