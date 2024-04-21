from datetime import datetime

from aiogoogle import Aiogoogle

from app.core.config import settings

FORMAT = "%Y/%m/%d %H:%M:%S"


async def spreadsheets_create(wrapper_services: Aiogoogle) -> str:
    now_date_time = datetime.now().strftime(FORMAT)
    service = await wrapper_services.discover('sheets', 'v4')
    spreadsheet_body = {
        'properties': {'title': f'Отчёт на {now_date_time}',
                       'locale': 'ru_RU'},
        'sheets': [{'properties': {'sheetType': 'GRID',
                                   'sheetId': 0,
                                   'title': 'Лист1',
                                   'gridProperties': {'rowCount': 100,
                                                      'columnCount': 11}}}]
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
            fields="id"
        ))


async def spreadsheets_update_value(
        spreadsheetid: str,
        closed_projects: list,
        wrapper_services: Aiogoogle
) -> None:
    now_date_time = datetime.now().strftime(FORMAT)
    service = await wrapper_services.discover('sheets', 'v4')
    table_values = [
        ['Отчёт от', now_date_time],
        ['Топ проектов по скорости закрытия'],
        ['Название проекта', 'Время сбора', 'Описание']
    ]

    for project in closed_projects:
        close_time = datetime(
            year=project['close_year'],
            month=project['close_month'],
            day=project['close_day'],
            hour=project['close_hour'],
            minute=project['close_minute'],
            second=project['close_second'],
            microsecond=project['close_microseconds'],
        )
        create_time = datetime(
            year=project['create_year'],
            month=project['create_month'],
            day=project['create_day'],
            hour=project['create_hour'],
            minute=project['create_minute'],
            second=project['create_second'],
            microsecond=project['create_microseconds'],
        )
        diff = close_time - create_time
        diff_days = diff.days
        diff_seconds = diff.seconds
        diff_microseconds = diff.microseconds

        hours, remainder = divmod(diff_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)

        formatted_diff = f"{diff_days} days, {hours:02d}:{minutes:02d}:{seconds:02d}.{diff_microseconds:06d}"
        new_row = [str(project['name']),
                   formatted_diff,
                   str(project['description'])]
        table_values.append(new_row)

    update_body = {
        'majorDimension': 'ROWS',
        'values': table_values
    }

    await wrapper_services.as_service_account(
        service.spreadsheets.values.update(
            spreadsheetId=spreadsheetid,
            range='A1:C30',
            valueInputOption='USER_ENTERED',
            json=update_body
        )
    )
