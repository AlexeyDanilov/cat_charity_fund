from datetime import datetime

from app.core.db import Base

from sqlalchemy import Column, Integer, Boolean, DateTime


class BaseProject(Base):
    __abstract__ = True

    full_amount = Column(Integer)
    invested_amount = Column(Integer, default=0)
    fully_invested = Column(Boolean, default=False)
    create_date = Column(DateTime, default=datetime.now)
    close_date = Column(DateTime)
