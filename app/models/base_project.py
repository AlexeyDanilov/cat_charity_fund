from datetime import datetime

from app.core.db import Base

from sqlalchemy import Column, Integer, Boolean, DateTime, CheckConstraint

from app.models.model_constants import DEFAULT_AMOUNT


class BaseProject(Base):

    __abstract__ = True

    __table_args__ = (
        CheckConstraint('invested_amount >= 0', name='invested_amount_non_negative'),
        CheckConstraint('invested_amount <= full_amount', name='invested_amount_not_exceed_full_amount'),
    )

    full_amount = Column(Integer)
    invested_amount = Column(Integer, default=DEFAULT_AMOUNT)
    fully_invested = Column(Boolean, default=False)
    create_date = Column(DateTime, default=datetime.now)
    close_date = Column(DateTime)
