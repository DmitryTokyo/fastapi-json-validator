import pytest
from restaurant_schedule.api.custom_types import ValidationResult
from restaurant_schedule.api.services.schedule_representation import (
    get_readable_restaurant_schedule,
    get_sortable_raw_schedule_data,
)
from restaurant_schedule.api.services.validator import validate_restaurant_schedule_raw_data, \
    handle_restaurant_error_state


@pytest.mark.asyncio
async def test_successful_validate_restaurant_schedule_data(restaurant_data_one_range):
    valid_data = await validate_restaurant_schedule_raw_data(restaurant_data_one_range)

    assert valid_data == ValidationResult(valid_data=restaurant_data_one_range, error=None)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    'restaurant_data, expected_result',
    [
        ({'weekdays': []}, ValidationResult(valid_data=None, error={'error': "'weekdays' is not a valid WeekDays"})),
        (
            {'monday': [{'type': 'open', 'value': 32400}]},
            ValidationResult(valid_data=None, error={'error': 'Restaurant missed close state'}),
        ),
        (
            {'monday': [{'type': 'close', 'value': 32400}]},
            ValidationResult(valid_data=None, error={'error': 'Restaurant missed open state'}),
        ),
        (
            {'monday': [{'types': 'close', 'value': 32400}]},
            ValidationResult(
                valid_data=None,
                error=[{'loc': ['type'], 'msg': 'field required', 'type': 'value_error.missing'}],
            ),
        ),
    ],
)
async def test_unsuccessful_validate_restaurant_schedule_data(restaurant_data, expected_result):
    valid_data = await validate_restaurant_schedule_raw_data(restaurant_data)

    assert valid_data == expected_result


@pytest.mark.asyncio
@pytest.mark.parametrize(
    'schedule_types, expected_result',
    [
        (['open', 'close', 'open'], {'error': 'Restaurant missed close state'}),
        (['close', 'open', 'close'], {'error': 'Restaurant missed open state'}),
        (['open', 'close', 'open', 'close'], None),
    ],
)
async def test_handle_restaurant_error_state(schedule_types, expected_result):
    error = await handle_restaurant_error_state(schedule_types)
    assert error == expected_result


@pytest.mark.asyncio
@pytest.mark.parametrize(
    'valid_data, expected_result',
    [
        (
            {'monday': [{'type': 'open', 'value': 32400}, {'type': 'close', 'value': 72000}]},
            {'Monday': [['09 AM', '08 PM']]},
        ),
        (
            {'monday': [{'type': 'open', 'value': 64800}], 'tuesday': [{'type': 'close', 'value': 3600}]},
            {'Monday': [['06 PM', '01 AM']], 'Tuesday': []},
        ),
        (
            {
                'monday': [{'type': 'open', 'value': 64800}],
                'tuesday': [
                    {'type': 'close', 'value': 3600},
                    {'type': 'open', 'value': 32400},
                    {'type': 'close', 'value': 39600},
                ],
            },
            {'Monday': [['06 PM', '01 AM']], 'Tuesday': [['09 AM', '11 AM']]},
        ),
    ],
)
async def test_get_sortable_raw_schedule_data(valid_data, expected_result):
    sortable_schedule_data = await get_sortable_raw_schedule_data(valid_data)

    assert sortable_schedule_data == expected_result


@pytest.mark.asyncio
@pytest.mark.parametrize(
    'sortable_raw_schedule_data, expected_result',
    [
        ({'Monday': [['09 AM', '08 PM']]}, 'Monday: 09 AM - 08 PM'),
        ({'Monday': [['06 PM', '01 AM']], 'Tuesday': []}, 'Monday: 06 PM - 01 AM\nTuesday: Closed'),
        (
            {'Monday': [['06 PM', '01 AM']], 'Tuesday': [['11 AM', '14 PM']]},
            'Monday: 06 PM - 01 AM\nTuesday: 11 AM - 14 PM',
        ),
    ],
)
async def test_get_readable_restaurant_schedule(
    mocker, restaurant_data_one_range, sortable_raw_schedule_data, expected_result,
):
    mocker.patch(
        'restaurant_schedule.api.services.schedule_representation.get_sortable_raw_schedule_data',
        return_value=sortable_raw_schedule_data,
    )
    restaurant_schedule = await get_readable_restaurant_schedule(restaurant_data_one_range)

    assert restaurant_schedule == expected_result
