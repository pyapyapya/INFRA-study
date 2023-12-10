FROM --platform=linux/amd64 python:3.9-slim AS build
WORKDIR /week1
RUN pip install poetry
ENV PATH="${PATH}:/path/to/poetry/bin"

COPY . /week1

RUN poetry install --no-root && rm -rf $POETRY_CACHE_DIR

FROM python:3.9-slim

WORKDIR /week1
COPY --from=build /week1 /week1

CMD ["uvicorn", "week1.main:app", "--reload", "--host", "0.0.0.0", "--port", "80"]