from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import settings

BaseDataplayer = declarative_base()
BaseRealtime = declarative_base()

# Dataplayer connection
dataplayer_url = (
    f"postgresql+psycopg2://{settings.DTAPL['user']}:{settings.DTAPL['password']}@"
    f"{settings.DTAPL['host']}:{settings.DTAPL['port']}/{settings.DTAPL['database']}"
)
engine_dataplayer = create_engine(dataplayer_url, pool_pre_ping=True)
SessionLocalDataplayer = sessionmaker(autocommit=False, autoflush=False, bind=engine_dataplayer)

# Realtime connection
realtime_url = (
    f"postgresql+psycopg2://{settings.REALTIME['user']}:{settings.REALTIME['password']}@"
    f"{settings.REALTIME['host']}:{settings.REALTIME['port']}/{settings.REALTIME['database']}"
)
engine_realtime = create_engine(realtime_url, pool_pre_ping=True)
SessionLocalRealtime = sessionmaker(autocommit=False, autoflush=False, bind=engine_realtime)

# Dependency functions
def get_dataplayer_db():
    db = SessionLocalDataplayer()
    try:
        yield db
    finally:
        db.close()

def get_realtime_db():
    db = SessionLocalRealtime()
    try:
        yield db
    finally:
        db.close()
