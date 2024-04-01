from typing import Optional

from sqlalchemy import select
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


charity_project_crud = CharityProjectCRUD(CharityProject)
