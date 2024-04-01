from sqlalchemy import Column, ForeignKey, Integer, Text

from app.models.base_project import BaseProject


class Donation(BaseProject):
    user_id = Column(Integer, ForeignKey('user.id'))
    comment = Column(Text)
