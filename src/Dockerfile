FROM python:3.8
WORKDIR /app

ENV PYTHONFAULTHANDLER=1 \
    PYTHONHASHSEED=random \
    PYTHONUNBUFFERED=1

RUN pip install poetry 
COPY pyproject.toml pyproject.toml 
COPY poetry.lock poetry.lock 
RUN poetry install --no-interaction
COPY . .

ENTRYPOINT poetry run uvicorn main:app --host 0.0.0.0
