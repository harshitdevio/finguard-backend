from __future__ import annotations

import hmac
import hashlib
import os
from typing import Final

OTP_SECRET_KEY: Final[str | None] = os.getenv("OTP_SECRET_KEY")

if not OTP_SECRET_KEY:
    raise RuntimeError("OTP_SECRET_KEY is not set")

def _normalize_otp(otp: str) -> str:
    """
    Normalize OTP input to avoid subtle mismatches.
    """
    otp = otp.strip()

    if not otp.isdigit():
        raise ValueError("OTP must contain only digits")

    return otp