import pytest
from httpx import AsyncClient
from fastapi import FastAPI

from app.main import app as fastapi_app

# Real app for full e2e workflows.
@pytest.fixture(scope="session")
def e2e_app() -> FastAPI:
    return fastapi_app

# async test client for full system interaction 
@pytest.fixture()
async def e2e_client(e2e_app: FastAPI):
    async with AsyncClient(
        app=e2e_app,
        base_url="http://test",
        follow_redirects=True,
    ) as client:
        yield client