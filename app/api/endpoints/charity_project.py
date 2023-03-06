from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (check_charity_project_already_closed,
                                check_charity_project_already_invested,
                                check_charity_project_exists,
                                check_charity_project_full_amount,
                                check_charity_project_fully,
                                check_name_duplicate)
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud.charity_project import charity_project_crud
from app.crud.donation import donation_crud
from app.schemas.charity_project import (CharityProjectBase,
                                         CharityProjectCreate,
                                         CharityProjectGet,
                                         CharityProjectUpdate)

router = APIRouter()


@router.get(
    '/',
    response_model=list[CharityProjectGet],
    response_model_exclude_none=True,
    description='Получает список всех проектов.'
)
async def get_all_charity_project(
        session: AsyncSession = Depends(get_async_session),
):
    all_projects = await charity_project_crud.get_multi(session)
    return all_projects


@router.post(
    '/',
    response_model=CharityProjectCreate,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
    # description=''
)
async def create_charity_project(
        charity_project: CharityProjectBase,
        session: AsyncSession = Depends(get_async_session)):
    """
    Создает благотворительный проект.\n
    Только для суперюзеров.
    """
    await check_name_duplicate(charity_project.name, session)
    donations_for_invest = await donation_crud.get_for_invest(session)
    new_project = await charity_project_crud.create(charity_project, donations_for_invest, session)
    return new_project


@router.delete(
    '/{charity_project_id}',
    response_model=CharityProjectGet,
    dependencies=[Depends(current_superuser)],
)
async def remove_charity_project(
        charity_project_id: int,
        session: AsyncSession = Depends(get_async_session),
):
    """
    Удаляет проект. Нельзя удалить проект, в который уже были инвестированы средства, его можно только закрыть.\n
    Только для суперюзеров.
    """
    charity_project = await check_charity_project_exists(charity_project_id, session)
    await check_charity_project_already_invested(charity_project)
    await check_charity_project_already_closed(charity_project)
    charity_project = await charity_project_crud.remove(charity_project, session)
    return charity_project


@router.patch(
    '/{charity_project_id}',
    response_model=CharityProjectGet,
    dependencies=[Depends(current_superuser)],
)
async def partially_update_meeting_room(
        charity_project_id: int,
        obj_in: CharityProjectUpdate,
        session: AsyncSession = Depends(get_async_session),
):
    """
    Закрытый проект нельзя редактировать, также нельзя установить требуемую сумму меньше уже вложенной.\n
    Только для суперюзеров.
    """
    charity_project = await check_charity_project_exists(
        charity_project_id, session
    )
    await check_charity_project_fully(charity_project)
    if obj_in.full_amount is not None:
        await check_charity_project_full_amount(charity_project, obj_in.full_amount)
    if obj_in.name is not None:
        await check_name_duplicate(obj_in.name, session)

    charity_project = await charity_project_crud.update(
        db_obj=charity_project,
        obj_in=obj_in,
        session=session)
    return charity_project
