FROM python:3.11-slim

WORKDIR /app

RUN pip install "poetry==1.8.3"

# Disable virtualenv creation inside container
RUN poetry config virtualenvs.create false

# Copy dependency files first for caching
COPY pyproject.toml poetry.lock* /app/

RUN poetry install --no-root --no-dev

COPY . /app

CMD ["poetry", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
