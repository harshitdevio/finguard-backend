"""
OTP hashing and verification utilities for Fintech authentication.

This module provides functions for securely hashing and verifying
one-time passwords (OTPs) using HMAC-SHA256. OTPs are tied to a
user-specific identifier to prevent reuse across accounts.

Security notes:
- OTPs are expected to be numeric and normalized before hashing.
- A global server-side secret key (OTP_SECRET_KEY) is required and
  must be set at runtime. The application fails hard if it is missing.
- Verification is performed in constant-time to mitigate timing attacks.
"""

from __future__ import annotations

import hmac
import hashlib
import os
from typing import Final

from app.core.config import settings

def _get_otp_secret_key() -> str:
    secret = settings.OTP_SECRET_KEY
    if not secret:
        raise RuntimeError("OTP_SECRET_KEY is not set")
    return secret


def _normalize_otp(otp: str) -> str:
    """
    Normalize OTP input to prevent subtle mismatches.

    Strips whitespace and ensures the OTP contains only digits.

    Args:
        otp: The raw OTP input.

    Returns:
        The normalized OTP string.

    Raises:
        ValueError: If the OTP contains non-numeric characters.
    """
    otp = otp.strip()

    if not otp.isdigit():
        raise ValueError("OTP must contain only digits")

    return otp


def hash_otp(*, otp: str, identifier: str) -> str:
    """
    Compute a secure HMAC-SHA256 hash of an OTP.

    OTPs are combined with a stable user-specific identifier to prevent
    OTP reuse across users and to bind them to a particular account.

    Args:
        otp: The raw OTP input.
        identifier: A stable, user-specific value (e.g., phone number or user ID).

    Returns:
        A hexadecimal string representing the HMAC-SHA256 hash of the OTP.

    Raises:
        ValueError: If OTP normalization fails.
    """
    otp = _normalize_otp(otp)

    message = f"{identifier}:{otp}".encode("utf-8")
    key = _get_otp_secret_key().encode("utf-8")

    digest = hmac.new(
        key=key,
        msg=message,
        digestmod=hashlib.sha256,
    ).hexdigest()

    return digest


def verify_otp(
    *,
    otp: str,
    identifier: str,
    stored_hash: str,
) -> bool:
    """
    Verify an OTP against a stored HMAC-SHA256 hash in constant time.

    Args:
        otp: The OTP provided by the user.
        identifier: The same user-specific identifier used during hashing.
        stored_hash: The previously computed OTP hash to verify against.

    Returns:
        True if the OTP is valid and matches the stored hash, False otherwise.

    Notes:
        - Returns False for any invalid input or normalization errors.
        - Uses hmac.compare_digest to prevent timing attacks.
    """
    if not otp or not stored_hash:
        return False

    try:
        computed_hash = hash_otp(otp=otp, identifier=identifier)
    except ValueError:
        return False

    return hmac.compare_digest(computed_hash, stored_hash)
