from pydantic import BaseModel


class ScheduleData(BaseModel):
    type: str
    value: int
