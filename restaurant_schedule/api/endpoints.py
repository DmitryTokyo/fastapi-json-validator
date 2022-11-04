from fastapi import APIRouter, HTTPException
from fastapi.responses import PlainTextResponse
from restaurant_schedule.api.services.schedule_representation import get_readable_restaurant_schedule
from restaurant_schedule.api.services.validator import validate_restaurant_schedule_raw_data

api_router = APIRouter(prefix='/schedule')


@api_router.post('/')
async def schedule(restaurant_schedule_data: dict):
    validation_result = await validate_restaurant_schedule_raw_data(restaurant_schedule_data)
    if validation_result.error:
        raise HTTPException(
            status_code=400,
            detail=validation_result.error,
        )
    readable_restaurant_schedule = await get_readable_restaurant_schedule(validation_result.valid_data)
    return PlainTextResponse(content=readable_restaurant_schedule, status_code=200)
