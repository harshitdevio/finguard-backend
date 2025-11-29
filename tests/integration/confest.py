import pytest
from httpx import AsyncClient
from fastapi import FastAPI
from sqlalchemy.ext.asyncio import AsyncSession

from app.main import app as fastapi_app


@pytest.fixture()
async def integration_db(db_session: AsyncSession):
    yield db_session


@pytest.fixture()
def integration_app() -> FastAPI:
    return fastapi_app