from http.client import BAD_REQUEST

from aiogoogle import Aiogoogle
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.services.google_api import (set_user_permissions,
                                         spreadsheets_create,
                                         spreadsheets_update_value)
from app.core.db import get_async_session
from app.core.google_client import get_service
from app.core.user import current_superuser
from app.crud.charity_project import charity_project_crud

router = APIRouter()


@router.get(
    '/',
    dependencies=[Depends(current_superuser)],
)
async def get_report(
        session: AsyncSession = Depends(get_async_session),
        wrapper_services: Aiogoogle = Depends(get_service)

):
    """
    Формирует отчет на привязанном гугл аккаунте\n
    Только для суперюзеров.
    """
    projects = await charity_project_crud.get_projects_by_completion_rate(
        session
    )
    try:
        spreadsheetid = await spreadsheets_create(wrapper_services)
        await set_user_permissions(spreadsheetid, wrapper_services)
        await spreadsheets_update_value(spreadsheetid,
                                        projects,
                                        wrapper_services)
    except IOError:
        raise HTTPException(
            status_code=BAD_REQUEST,
            detail='Ошибка доступа к GoogleAPI или Google аккаунту',
        )
    return 'Отчет создан'