FROM python:3.9.13
WORKDIR /week1
RUN pip install poetry

COPY pyproject.toml poetry.lock ./
COPY week1 week1
RUN poetry install --no-root
EXPOSE 8000

CMD ["uvicorn", "main:app" "--reload", "--host", "0.0.0.0"]