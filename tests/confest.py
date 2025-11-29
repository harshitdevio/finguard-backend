import asyncio
import os
import time
from typing import AsyncGenerator

import pytest
import docker
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine,
)
from sqlalchemy.orm import sessionmaker
from httpx import AsyncClient
from fastapi import FastAPI

from app.core.config import settings
from app.db.models import Base 
from app.main import app as fastapi_app  


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()

# Temporary Postgres Via Docker
@pytest.fixture(scope="session")
def postgres_container():
    client = docker.from_env()

    container = client.containers.run(
        "postgres:16-alpine",
        name="test-postgres",
        environment={
            "POSTGRES_USER": "test",
            "POSTGRES_PASSWORD": "test",
            "POSTGRES_DB": "test_db",
        },
        ports={"5432/tcp": 5433},   # host 5433 → container 5432
        detach=True,
        auto_remove=True,
    )

    time.sleep(2)
    retries = 10
    while retries:
        try:
            import psycopg2
            psycopg2.connect(
                host="localhost",
                port=5433,
                user="test",
                password="test",
                database="test_db"
            )
            break
        except Exception:
            retries -= 1
            time.sleep(1)

    if retries == 0:
        raise RuntimeError("Postgres test container did not start in time")

    yield container