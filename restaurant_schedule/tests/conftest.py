import pytest


@pytest.fixture
def restaurant_data_one_range():
    return {'monday': [{'type': 'open', 'value': 32400}, {'type': 'close', 'value': 72000}]}
