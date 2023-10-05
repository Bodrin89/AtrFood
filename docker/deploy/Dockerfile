# The builder image, used to build the virtual environment
FROM python:3.11-buster as builder
ARG POETRY_VERSION=1.6.1

RUN pip install poetry==$POETRY_VERSION

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

WORKDIR /code

COPY pyproject.toml poetry.lock ./

RUN poetry install --without dev --no-root && rm -rf $POETRY_CACHE_DIR

# The runtime image, used to just run the code provided its virtual environment
FROM python:3.11-slim-buster as runtime

WORKDIR /code

RUN groupadd -r docker && useradd -g docker docker
RUN chown -R docker:docker /code
USER docker

ENV VIRTUAL_ENV=/code/.venv \
    PATH="/code/.venv/bin:$PATH"

COPY --from=builder ${VIRTUAL_ENV} ${VIRTUAL_ENV}

COPY ../.. .

ENTRYPOINT ["bash", "entrypoint.sh"]

CMD ["gunicorn", "config.wsgi", "-w", "4", "-b", "0.0.0.0:80"]
