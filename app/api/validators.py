from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import charity_project_crud
from app.models import CharityProject


async def check_name_duplicate(
        name: str,
        session: AsyncSession,
) -> None:
    charity_project = await charity_project_crud.get_project_id_by_name(name, session)
    if charity_project is not None:
        raise HTTPException(
            status_code=400,
            detail='Проект с таким именем уже существует!',
        )


async def check_charity_project_exists(
        charity_project_id: int,
        session: AsyncSession,
) -> CharityProject:
    charity_project = await charity_project_crud.get(charity_project_id, session)
    if charity_project is None:
        raise HTTPException(
            status_code=404,
            detail='Проект не найдена!'
        )
    return charity_project


async def check_charity_project_fully(project: CharityProject):
    if project.fully_invested:
        raise HTTPException(
            status_code=400,
            detail='Закрытый проект нельзя редактировать!'
        )
    return project


async def check_charity_project_full_amount(project: CharityProject, full_amount: int):
    if project.invested_amount > full_amount:
        raise HTTPException(
            status_code=422,
            detail='Нельзя установить full_amount меньше fully_invested'
        )
    return project


async def check_charity_project_already_invested(project: CharityProject):
    if project.invested_amount > 0:
        raise HTTPException(
            status_code=400,
            detail='В проект были внесены средства, не подлежит удалению!'
        )
    return project


async def check_charity_project_already_closed(project: CharityProject):
    if project.invested_amount == project.full_amount:
        raise HTTPException(
            status_code=400,
            detail='Удаление закрытых проектов запрещено.'
        )
    return project
