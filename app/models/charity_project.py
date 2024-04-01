from sqlalchemy import Column, String, Text

from app.models.base_project import BaseProject


class CharityProject(BaseProject):
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text)
