runserver:
	uvicorn restaurant_schedule.main:app --reload --port 5000

test:
	pytest --cov=restaurant_schedule --cov-branch restaurant_schedule/tests/*

style:
	flake8 restaurant_schedule