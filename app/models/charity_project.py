from sqlalchemy import Column, String, Text

from app.models.base_project import BaseProject
from app.models.model_constants import MAX_LENGTH_NAME


class CharityProject(BaseProject):
    name = Column(String(MAX_LENGTH_NAME), unique=True, nullable=False)
    description = Column(Text)
