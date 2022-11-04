FROM python:3.10-slim

WORKDIR /app

COPY ./requirements/base.txt /app/requirements/base.txt

RUN pip install --no-cache-dir --upgrade -r /app/requirements/base.txt

COPY ./restaurant_schedule /app/restaurant_schedule

CMD ["uvicorn", "restaurant_schedule.main:app", "--host", "0.0.0.0", "--port", "5000"]