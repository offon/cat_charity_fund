from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_superuser, current_user
from app.crud.charity_project import charity_project_crud
from app.crud.donation import donation_crud
from app.models import User
from app.schemas.donation import (DonationGet, DonationPost,
                                  DonationPostReturn, DonationtBase)

router = APIRouter()


@router.get(
    '/',
    response_model=list[DonationGet],
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)]
)
async def get_all_donation(
        session: AsyncSession = Depends(get_async_session)
):
    all_donation = await donation_crud.get_multi(session)
    return all_donation


@router.post(
    '/',
    response_model=DonationPostReturn,
    response_model_exclude_none=True
)
async def create_donation(
        donation: DonationPost,
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_user)):
    projects_for_invest = await charity_project_crud.get_for_invest(session)
    new_donation = await donation_crud.create(donation, projects_for_invest, session, user)
    return new_donation


@router.get(
    '/my',
    response_model=list[DonationtBase],
    response_model_exclude_none=True,
)
async def get_all_donation(
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_user)
):
    all_donation = await donation_crud.get_my_donations(user=user, session=session)
    return all_donation