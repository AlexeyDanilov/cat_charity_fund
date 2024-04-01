from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charityproject import charity_project_crud
from app.models import CharityProject


async def check_unique_name(name: str, session: AsyncSession) -> None:
    charity_project_id = await session.execute(
        select(CharityProject.id).where(
            CharityProject.name == name
        )
    )
    charity_project_id = charity_project_id.scalars().first()
    if charity_project_id is not None:
        raise HTTPException(
            status_code=400,
            detail='Проект с таким именем уже существует'
        )


async def check_charity_project_exists(project_id: int, session: AsyncSession):
    charity_project = await charity_project_crud.get(project_id, session)
    if charity_project is None:
        raise HTTPException(
            status_code=404,
            detail='Проект не найден'
        )

    return charity_project


async def full_amount_not_less_invested_amount(charity_project: CharityProject, full_amount: int):
    if full_amount < charity_project.invested_amount:
        raise HTTPException(
            status_code=400,
            detail='Требуемая сумма не может быть меньше внесённой'
        )


async def not_allowed_change_closed_or_investing_project(charity_project: CharityProject):
    if charity_project.fully_invested or charity_project.invested_amount > 0:
        raise HTTPException(
            status_code=400,
            detail='Нельзя удалять закрытый проект или проект, в который уже инвестировали'
        )

    return charity_project


async def not_allowed_change_closed_project(charity_project: CharityProject):
    if charity_project.fully_invested:
        raise HTTPException(
            status_code=400,
            detail='Нельзя изменять закрытый проект'
        )

    return charity_project
