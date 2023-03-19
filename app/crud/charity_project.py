from datetime import datetime
from typing import Optional

from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import CharityProject, User
from app.models.donation import Donation
from app.services.charity_project import invest_donation


class CRUDCharityProject(CRUDBase):
    async def get_project_id_by_name(
            self,
            name: str,
            session: AsyncSession,
    ) -> Optional[int]:
        db_project_id = await session.execute(
            select(CharityProject.id).where(
                CharityProject.name == name
            )
        )
        db_project_id = db_project_id.scalars().first()
        return db_project_id

    async def create(
            self,
            obj_in,
            donations_for_invest: list[Donation],
            session: AsyncSession,
            user: Optional[User] = None

    ):
        obj_in_data = obj_in.dict()
        if user is not None:
            obj_in_data['user_id'] = user.id
        obj_in_data['create_date'] = datetime.now()
        db_obj = CharityProject(**obj_in_data)
        donations_for_invest, db_obj = await invest_donation(db_obj, donations_for_invest)
        for donation in donations_for_invest:
            session.add(donation)
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
        if db_obj.invested_amount == db_obj.full_amount:
            update_data['fully_invested'] = True
            update_data['close_date'] = datetime.now()
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def get_projects_by_completion_rate(
            self,
            session: AsyncSession,
    ) -> list[CharityProject]:
        charity_projects = await session.execute(
            select(CharityProject).where(CharityProject.fully_invested == 1)
        )
        charity_projects = charity_projects.scalars().all()
        return charity_projects


charity_project_crud = CRUDCharityProject(CharityProject)
