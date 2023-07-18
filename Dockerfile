FROM python:3.10-slim-buster

ENV PYTHONUNBUFFERED 1

WORKDIR /app

RUN apt-get update \
    && apt-get -y install libpq-dev gcc

COPY . /app

RUN pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-dev

RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y

CMD ["alembic", "upgrade", "head"]
CMD ["python", "-m", "bot"]
