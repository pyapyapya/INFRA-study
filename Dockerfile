FROM --platform=linux/amd64 python:3.9-slim
WORKDIR /week1
RUN pip install poetry

COPY pyproject.toml poetry.lock ./
COPY week1 week1
RUN poetry install --no-root
RUN chmod +x /week1/main.py

CMD ["poetry", "run", "uvicorn", "week1.main:app", "--reload", "--host", "0.0.0.0", "--port", "80"]