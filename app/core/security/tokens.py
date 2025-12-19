from datetime import datetime, timedelta
from jose import jwt
import secrets

from app.core.config import settings


ACCESS_TOKEN_TTL_MIN = 15
REFRESH_TOKEN_TTL_DAYS = 30
ALGORITHM = "HS256"


def create_access_token(*, user_id: str, tier: str, status: str) -> str:
    payload = {
        "sub": user_id,
        "tier": tier,
        "status": status,
        "type": "access",
        "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_TTL_MIN),
    }
    return jwt.encode(payload, settings.JWT_SECRET, algorithm=ALGORITHM)


def create_refresh_token(*, user_id: str) -> str:
    payload = {
        "sub": user_id,
        "type": "refresh",
        "exp": datetime.utcnow() + timedelta(days=REFRESH_TOKEN_TTL_DAYS),
        "jti": secrets.token_hex(16),
    }
    return jwt.encode(payload, settings.JWT_SECRET, algorithm=ALGORITHM)
