from time import strftime
from time import gmtime
from restaurant_schedule.api.enums import WeekDays


async def get_readable_restaurant_schedule(restaurant_schedule_data: dict[str, list]) -> str:
    readable_restaurant_schedule = []
    raw_sortable_data = await get_sortable_raw_schedule_data(restaurant_schedule_data)
    for weekday in raw_sortable_data:
        readable_time_ranges = ', '.join([' - '.join(d) for d in raw_sortable_data[weekday]])
        readable_time_ranges = readable_time_ranges if readable_time_ranges else 'Closed'
        readable_restaurant_schedule.append(f'{weekday}: {readable_time_ranges}')
    return '\n'.join(readable_restaurant_schedule)


async def get_sortable_raw_schedule_data(restaurant_schedule_data: dict) -> dict[str, list]:
    """
    We should sort the time range because the restaurant can close the next day after it opens.
    In this case, close time should relate to the day when it was opened
    """
    raw_sortable_schedule: dict[str, list] = {}
    previous_day: str | None = None
    is_day_time_range_complete = True
    day_time_range_chunk: list[str] = []

    for weekday in restaurant_schedule_data:
        weekday_title = WeekDays(weekday).title()
        raw_sortable_schedule[weekday_title] = []

        for schedule_state in restaurant_schedule_data[weekday]:
            formatted_time = strftime('%I %p', gmtime(schedule_state['value']))
            day_time_range_chunk.append(formatted_time)
            is_day_time_range_complete = schedule_state['type'] == 'close'

            if is_day_time_range_complete:
                raw_schedule_key = previous_day if previous_day else weekday_title
                raw_sortable_schedule[raw_schedule_key].append(day_time_range_chunk)
                day_time_range_chunk = []
                previous_day = None

        if not is_day_time_range_complete:
            previous_day = weekday_title

    return raw_sortable_schedule
