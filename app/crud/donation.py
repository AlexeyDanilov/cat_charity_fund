from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import Donation, User


class DonationCRUD(CRUDBase):

    async def update(
            self,
            db_obj,
            obj_in,
            session: AsyncSession,
    ):
        ...

    async def remove(
            self,
            db_obj,
            session: AsyncSession,
    ):
        ...

    async def get_by_user(self, user: User, session: AsyncSession):
        donations = await session.execute(select(Donation).where(Donation.user_id == user.id))
        return donations.scalars().all()


donation_crud = DonationCRUD(Donation)
