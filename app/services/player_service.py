from sqlalchemy import text
from sqlalchemy.orm import Session

class PlayerService:
    def __init__(self, db: Session):
        self.db = db

    def call_random_string(self, length: int) -> str:
        """Call the DB function random_string(length)"""
        stmt = text("SELECT random_string(:length)")
        result = self.db.execute(stmt, {"length": length}).fetchone()
        return result[0] if result else ""

    def call_generate_uid(self, size: int) -> str:
        """Call the DB function generate_uid(size)"""
        stmt = text("SELECT generate_uid(:size)")
        result = self.db.execute(stmt, {"size": size}).fetchone()
        return result[0] if result else ""

    def generate_player_code(self, downline_code: str) -> str:
        """Generate a new player_code"""
        random_part = self.call_random_string(6)
        uid_part = self.call_generate_uid(2)
        return f"{downline_code}{random_part}{uid_part}"