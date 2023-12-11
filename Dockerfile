FROM --platform=linux/amd64 python:3.9-slim
WORKDIR /week1
COPY pyproject.toml .
COPY . /week1

RUN pip install poetry
RUN poetry config virtualenvs.create false
RUN poetry install --no-root

CMD ["poetry", "run", "uvicorn", "week1.main:app", "--reload", "--host", "0.0.0.0", "--port", "80"]