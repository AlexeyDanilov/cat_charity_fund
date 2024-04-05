from datetime import datetime

from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import User


class CRUDBase:

    def __init__(self, model):
        self.model = model

    async def get(
            self,
            obj_id: int,
            session: AsyncSession,
    ):
        db_obj = await session.execute(
            select(self.model).where(
                self.model.id == obj_id
            )
        )
        return db_obj.scalars().first()

    async def get_multi(
            self,
            session: AsyncSession
    ):
        db_objs = await session.execute(select(self.model))
        return db_objs.scalars().all()

    async def create(
            self,
            obj_in,
            session: AsyncSession,
            user: User = None,
            commit_flag: bool = True
    ):
        obj_in_data = obj_in.dict()
        if not commit_flag:
            for key, default_value in self.model.__table__.columns.items():
                if key not in ('id', 'create_date') and key not in obj_in_data and default_value.default is not None:
                    obj_in_data[key] = default_value.default.arg
        if user is not None:
            obj_in_data['user_id'] = user.id
        db_obj = self.model(**obj_in_data)
        if commit_flag:
            session.add(db_obj)
            await session.commit()
            await session.refresh(db_obj)
        return db_obj

    async def update(
            self,
            db_obj,
            obj_in,
            session: AsyncSession,
    ):
        obj_data = jsonable_encoder(db_obj)
        update_data = obj_in.dict(exclude_unset=True)

        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        if db_obj.full_amount == db_obj.invested_amount:
            db_obj.fully_invested = True
            db_obj.close_date = datetime.now()
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def remove(
            self,
            db_obj,
            session: AsyncSession,
    ):
        await session.delete(db_obj)
        await session.commit()
        return db_obj

    async def commit_and_refresh(
            self,
            objs,
            session: AsyncSession
    ):
        if not objs:
            return
        session.add_all(objs)
        await session.commit()

        for obj in objs:
            await session.refresh(obj)

    async def get_multi_not_fully_invested(self, session: AsyncSession):
        charity_projects = await session.execute(
            select(self.model).filter(
                ~self.model.fully_invested
            ).order_by(self.model.create_date)
        )
        charity_projects = charity_projects.scalars().all()
        return charity_projects
