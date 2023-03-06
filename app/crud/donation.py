from datetime import datetime
from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import CharityProject, Donation, User
from app.services.donation import invest_donation


class CRUDDonation(CRUDBase):
    async def get_my_donations(self, user, session):
        donations = await session.execute(select(Donation).where(Donation.user_id == user.id))
        return donations.scalars().all()

    async def create(
            self,
            obj_in,
            projects_for_invest: list[CharityProject],
            session: AsyncSession,
            user: Optional[User] = None
    ):
        obj_in_data = obj_in.dict()
        if user is not None:
            obj_in_data['user_id'] = user.id
        obj_in_data['create_date'] = datetime.now()
        db_obj = self.model(**obj_in_data)
        projects_for_invest, donation = invest_donation(db_obj, projects_for_invest, session)
        for projects in projects_for_invest:
            session.add(projects)
        session.add(donation)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj


donation_crud = CRUDDonation(Donation)