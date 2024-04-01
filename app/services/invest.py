from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import CharityProject, Donation


async def invest_after_creating_donation(donation: Donation, session: AsyncSession):
    charity_projects = await session.execute(
        select(CharityProject).filter(
            ~CharityProject.fully_invested
        ).order_by(CharityProject.create_date)
    )
    charity_projects = charity_projects.scalars().all()

    if not charity_projects:
        return []

    free_sum = donation.full_amount - donation.invested_amount
    for charity_project in charity_projects:
        invest_sum = min(
            free_sum, charity_project.full_amount - charity_project.invested_amount
        )
        charity_project.invested_amount += invest_sum
        charity_project.fully_invested = charity_project.invested_amount == charity_project.full_amount
        if charity_project.fully_invested:
            charity_project.close_date = datetime.utcnow()

        donation.invested_amount += invest_sum
        free_sum -= invest_sum

    if donation.full_amount <= donation.invested_amount:
        donation.fully_invested = True
        donation.close_date = datetime.utcnow()

    data = [charity_project for charity_project in charity_projects]
    data.append(donation)
    return data


async def invest_after_creating_project(charity_project: CharityProject, session: AsyncSession):
    donation = await session.execute(
        select(Donation).filter(~Donation.fully_invested).order_by(Donation.create_date)
    )
    donation = donation.scalars().first()

    if not donation:
        return

    invest_sum = min(charity_project.full_amount - charity_project.invested_amount,
                     donation.full_amount - donation.invested_amount)
    charity_project.invested_amount += invest_sum
    donation.invested_amount += invest_sum

    charity_project.fully_invested = charity_project.invested_amount == charity_project.full_amount
    if charity_project.fully_invested:
        charity_project.close_date = datetime.utcnow()

    donation.fully_invested = donation.full_amount == donation.invested_amount
    if donation.fully_invested:
        donation.close_date = datetime.utcnow()

    return charity_project, donation
