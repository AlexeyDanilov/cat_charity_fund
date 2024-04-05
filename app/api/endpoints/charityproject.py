from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (
    check_charity_project_exists, check_unique_name, full_amount_not_less_invested_amount,
    not_allowed_change_closed_or_investing_project, not_allowed_change_closed_project
)
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud.charityproject import charity_project_crud
from app.crud.donation import donation_crud
from app.schemas.charityproject import CharityProjectCreate, CharityProjectDB, CharityProjectUpdate
from app.services.invest import invest_after_creating_entity

router = APIRouter()


@router.post(
    '/',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)]
)
async def create_new_charity_project(
        new_project: CharityProjectCreate,
        session: AsyncSession = Depends(get_async_session)
):
    await check_unique_name(new_project.name, session)
    new_charity_project = await charity_project_crud.create(new_project, session, commit_flag=False)
    donations = await donation_crud.get_multi_not_fully_invested(session)
    updated_data = await invest_after_creating_entity(new_charity_project, donations)
    updated_data = updated_data if updated_data else [new_charity_project, *donations]
    await charity_project_crud.commit_and_refresh(updated_data, session)
    return new_charity_project


@router.get(
    '/',
    response_model=list[CharityProjectDB],
    response_model_exclude_none=True
)
async def charity_projects_list(session: AsyncSession = Depends(get_async_session)):
    charity_projects = await charity_project_crud.get_multi(session)
    return charity_projects


@router.patch(
    '/{project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
    response_model_exclude_none=True
)
async def charity_projects_update(
        project_id: int,
        obj_in: CharityProjectUpdate,
        session: AsyncSession = Depends(get_async_session)
):
    charity_project = await check_charity_project_exists(project_id, session)
    if obj_in.full_amount is not None:
        await full_amount_not_less_invested_amount(charity_project, obj_in.full_amount)

    if obj_in.name is not None:
        await check_unique_name(obj_in.name, session)

    charity_project = await not_allowed_change_closed_project(charity_project)
    charity_project = await charity_project_crud.update(charity_project, obj_in, session)
    return charity_project


@router.delete(
    '/{project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)]
)
async def charity_project_delete(
        project_id: int,
        session: AsyncSession = Depends(get_async_session)
):
    charity_project = await check_charity_project_exists(project_id, session)
    charity_project = await not_allowed_change_closed_or_investing_project(charity_project)
    charity_project = await charity_project_crud.remove(charity_project, session)
    return charity_project
