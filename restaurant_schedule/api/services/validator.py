import json

from restaurant_schedule.api.custom_types import ValidationResult
from restaurant_schedule.api.enums import WeekDays
from restaurant_schedule.api.schemas import ScheduleData
from pydantic import ValidationError


async def validate_restaurant_schedule_raw_data(
    restaurant_schedule_data: dict,
) -> ValidationResult:
    valid_data: dict | None = None
    schedule_types: list[str] = []

    for weekday in restaurant_schedule_data:
        try:
            WeekDays(weekday)
        except ValueError as e:
            return ValidationResult(valid_data=valid_data, error={'error': str(e)})

        weekday_schedule_data: list[dict] = restaurant_schedule_data[weekday]
        for data in weekday_schedule_data:
            try:
                validate_data = ScheduleData.parse_obj(data)
            except ValidationError as e:
                return ValidationResult(valid_data=None, error=json.loads(e.json()))
            else:
                schedule_types.append(validate_data.type)

    error = await handle_restaurant_error_state(schedule_types)
    valid_data = restaurant_schedule_data if error is None else valid_data

    return ValidationResult(valid_data=valid_data, error=error)


async def handle_restaurant_error_state(schedule_types) -> dict | None:
    error: dict | None = None
    open_types = list(filter(lambda t: t == 'open', schedule_types))
    close_types = list(filter(lambda t: t == 'close', schedule_types))
    if len(open_types) > len(close_types):
        error = {'error': 'Restaurant missed close state'}
    elif len(open_types) < len(close_types):
        error = {'error': 'Restaurant missed open state'}

    return error
