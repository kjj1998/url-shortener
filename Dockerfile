FROM python:3.12.0

RUN pip install poetry==1.7.1

COPY pyproject.toml poetry.lock ./
COPY alembic.ini ./
COPY alembic ./alembic
COPY url_shortener ./url_shortener
COPY README.md ./
COPY entrypoint.sh ./entrypoint.sh

RUN chmod +x entrypoint.sh

RUN poetry install

ENTRYPOINT ["./entrypoint.sh"]