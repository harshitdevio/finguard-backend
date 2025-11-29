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