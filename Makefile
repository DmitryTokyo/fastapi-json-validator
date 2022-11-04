runserver:
	uvicorn restaurant_schedule.main:app --reload --port 5000

test:
	pytest -vvs --cov

style:
	flake8 restaurant_schedule