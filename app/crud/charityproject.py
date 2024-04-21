from typing import Optional

from sqlalchemy import select, extract, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import CharityProject


class CharityProjectCRUD(CRUDBase):

    async def get_charity_project_by_id(
            self,
            project_id: int,
            session: AsyncSession
    ) -> Optional[CharityProject]:
        charity_project = await session.execute(
            select(CharityProject).where(CharityProject.id == project_id)
        )
        return charity_project.scalars().first()

    async def get_closed_projects(self, session: AsyncSession) -> list[dict[str, int]]:
        closed_projects = await session.execute(select(
            [CharityProject.name,
             extract('year', CharityProject.create_date).label('create_year'),
             extract('month', CharityProject.create_date).label('create_month'),
             extract('day', CharityProject.create_date).label('create_day'),
             extract('hour', CharityProject.create_date).label('create_hour'),
             extract('minute', CharityProject.create_date).label('create_minute'),
             extract('second', CharityProject.create_date).label('create_second'),
             extract('microseconds', CharityProject.create_date).label('create_microseconds'),
             extract('year', CharityProject.close_date).label('close_year'),
             extract('month', CharityProject.close_date).label('close_month'),
             extract('day', CharityProject.close_date).label('close_day'),
             extract('hour', CharityProject.close_date).label('close_hour'),
             extract('minute', CharityProject.close_date).label('close_minute'),
             extract('second', CharityProject.close_date).label('close_second'),
             extract('microseconds', CharityProject.close_date).label('close_microseconds'),
             CharityProject.description]
        ).where(CharityProject.close_date is not None).order_by(
            (func.julianday(CharityProject.close_date) - func.julianday(CharityProject.create_date)).asc()))
        return closed_projects.all()


charity_project_crud = CharityProjectCRUD(CharityProject)
