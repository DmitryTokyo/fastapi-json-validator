from typing import NamedTuple


class ValidationResult(NamedTuple):
    valid_data: dict | None
    error: dict | list | None
