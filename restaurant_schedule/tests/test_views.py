import pytest
from httpx import AsyncClient
from restaurant_schedule.api.custom_types import ValidationResult
from restaurant_schedule.config.settings import settings
from restaurant_schedule.main import app


@pytest.mark.asyncio
@pytest.mark.parametrize(
    'validate_result, expected_status_code, expected_content',
    [
        (ValidationResult(valid_data={'data': 'test data'}, error=None), 200, b'some result'),
        (
            ValidationResult(valid_data={}, error={'error': 'test error'}),
            400,
            b'{"detail":{"error":"test error"}}',
        ),
    ],
)
async def test_read_main(restaurant_data_one_range, mocker, validate_result, expected_status_code, expected_content):
    mocker.patch(
        'restaurant_schedule.api.endpoints.validate_restaurant_schedule_raw_data',
        return_value=validate_result,
    )
    mocker.patch('restaurant_schedule.api.endpoints.get_readable_restaurant_schedule', return_value='some result')

    async with AsyncClient(app=app, base_url=f'http://{settings.API_V1_STR}') as ac:
        response = await ac.post('schedule/', json=restaurant_data_one_range)

    assert response.status_code == expected_status_code
    assert response.content == expected_content
