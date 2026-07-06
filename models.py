from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import declarative_base # base class all tables inherit from
from datetime import datetime, timezone


Base = declarative_base()

class URL(Base):
    __tablename__ = "urls"

    id = Column(Integer, primary_key=True)
    short_code = Column(String, unique=True)
    original_url = Column(String)
    created_at = Column(DateTime, default= lambda: datetime.now(timezone.utc))
    expires_at = Column(DateTime, nullable = True)
    clicks = Column(Integer, default = 0)