import pytest
from httpx import AsyncClient
from fastapi import FastAPI

from app.main import app as fastapi_app