from datetime import datetime
from operator import itemgetter

from aiogoogle import Aiogoogle

from app.core.config import settings
from app.models.charity_project import CharityProject


async def spreadsheets_create(wrapper_services: Aiogoogle) -> str:
    now_date_time = datetime.now().strftime(settings.FORMAT)
    service = await wrapper_services.discover('sheets', 'v4')
    spreadsheet_body = {
        'properties': {'title': f'Отчет от {now_date_time}',
                       'locale': 'ru_RU'},
        'sheets': [{'properties': {'sheetType': 'GRID',
                                   'sheetId': 0,
                                   'title': 'Лист1',
                                   'gridProperties': {'rowCount': 50,
                                                      'columnCount': 5}}}]
    }
    response = await wrapper_services.as_service_account(
        service.spreadsheets.create(json=spreadsheet_body)
    )
    spreadsheetid = response['spreadsheetId']
    return spreadsheetid


async def set_user_permissions(
        spreadsheetid: str,
        wrapper_services: Aiogoogle
) -> None:
    permissions_body = {'type': 'user',
                        'role': 'writer',
                        'emailAddress': settings.email}
    service = await wrapper_services.discover('drive', 'v3')
    await wrapper_services.as_service_account(
        service.permissions.create(
            fileId=spreadsheetid,
            json=permissions_body,
            fields="id",
            sendNotificationEmail=False
        ))


async def spreadsheets_update_value(
        spreadsheetid: str,
        charity_projects: list[CharityProject],
        wrapper_services: Aiogoogle
) -> None:
    now_date_time = datetime.now().strftime(settings.FORMAT)
    service = await wrapper_services.discover('sheets', 'v4')
    table_header = [
        ['Отчет на', now_date_time],
        ['Топ проектов по скорости закрытия'],
        ['Название проекта', 'Время сбора', 'Описание']
    ]
    table_values = []
    for project in charity_projects:
        new_row = [str(project.name), str((project.close_date - project.create_date)), str(project.description)]
        table_values.append(new_row)
    table_values.sort(key=itemgetter(1))
    table_header.extend(table_values)
    update_body = {
        'majorDimension': 'ROWS',
        'values': table_header
    }
    await wrapper_services.as_service_account(
        service.spreadsheets.values.update(
            spreadsheetId=spreadsheetid,
            range='A1:E30',
            valueInputOption='USER_ENTERED',
            json=update_body
        )
    )
