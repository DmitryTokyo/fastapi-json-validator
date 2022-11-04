from enum import Enum


class WeekDays(Enum):
    monday = 'monday'
    tuesday = 'tuesday'
    wednesday = 'wednesday'
    thursday = 'thursday'
    friday = 'friday'
    saturday = 'saturday'
    sunday = 'sunday'

    def title(self) -> str:
        return self.value.capitalize()
