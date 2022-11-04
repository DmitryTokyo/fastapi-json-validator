from fastapi import FastAPI

from restaurant_schedule.api.endpoints import api_router
from restaurant_schedule.config.settings import settings

app = FastAPI(title=settings.PROJECT_NAME, openapi_url=f'{settings.API_V1_STR}/openapi.json')

app.include_router(api_router, prefix=settings.API_V1_STR)
