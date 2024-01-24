FROM python:3.12

ENV PYTHONUNBUFFERED=1

COPY src/requirements.txt /code/

WORKDIR /code/

RUN pip install -r requirements.txt

COPY src /code/

