FROM python:3.10-slim

ENV POETRY_VERSION=1.4.0

RUN pip install "poetry==$POETRY_VERSION"

WORKDIR /code
COPY poetry.lock pyproject.toml /code/
RUN poetry config virtualenvs.create false \
  && poetry install --no-root --no-interaction --no-ansi
COPY ../../ .

ENTRYPOINT ["bash", "entrypoint.sh"]
