from datetime import datetime, timedelta, timezone

from fastapi.security import HTTPBearer
from jose import jwt

from app.core.config import settings

security = HTTPBearer()

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=30))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)