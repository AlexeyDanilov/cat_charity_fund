from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_user, current_superuser
from app.crud.charityproject import charity_project_crud
from app.crud.donation import donation_crud
from app.models import User
from app.schemas.donation import DonationCreate, DonationDB, DonationByUser
from app.services.invest import invest_after_creating_entity

router = APIRouter()


@router.post(
    '/',
    response_model=DonationByUser,
    response_model_exclude_none=True,
)
async def create_new_donation(
        new_donation: DonationCreate,
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)
):
    donation = await donation_crud.create(new_donation, session, user, False)
    charity_projects = await charity_project_crud.get_multi_not_fully_invested(session)
    updated_data = await invest_after_creating_entity(donation, charity_projects)
    updated_data = updated_data if updated_data else [donation, *charity_projects]
    await donation_crud.commit_and_refresh(updated_data, session)
    return donation


@router.get(
    '/',
    response_model=list[DonationDB],
    dependencies=[Depends(current_superuser)],
    response_model_exclude_none=True
)
async def get_all_donations(session: AsyncSession = Depends(get_async_session)):
    donations = await donation_crud.get_multi(session)
    return donations


@router.get(
    '/my',
    response_model=list[DonationByUser],
    response_model_exclude_none=True
)
async def get_all_user_donations(
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)
):
    donations = await donation_crud.get_by_user(user, session)
    return donations
