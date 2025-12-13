from typing import Final

from app.core.redis import redis_client
from app.core.securities import generate_otp
from app.auth.OTP.bruteforce import (
    is_locked,
    _increment_failed_attempts,
    _clear_failed_attempts,
)
from app.auth.OTP.otp_exceptions import (
    OTPRateLimitExceeded,
    OTPLocked,
    OTPExpired,
    OTPMismatch,
)

OTP_EXPIRY: Final[int] = 300
OTP_MAX_REQUESTS: Final[int] = 3

OTP_VERIFY_MAX_ATTEMPTS: Final[int] = 5
OTP_VERIFY_WINDOW: Final[int] = 15 * 60
OTP_LOCKOUT_TTL: Final[int] = 60 * 60


async def send_otp(phone: str) -> bool:
    """
    Generate and send a One-Time Password (OTP) to the given phone number.

    Enforces request-level rate limiting to prevent OTP abuse.

    Args:
        phone: Phone number for which the OTP should be generated.

    Raises:
        OTPRateLimitExceeded: If OTP request limit is exceeded.

    Returns:
        True if OTP generation and storage succeeds.
    """
    #Check rate limit
    count_key = f"otp_count:{phone}"
    request_count: int = await redis_client.incr(count_key)

    if request_count == 1:
        await redis_client.expire(count_key, OTP_EXPIRY)

    if request_count > OTP_MAX_REQUESTS:
        raise OTPRateLimitExceeded(
            "Too many OTP requests, Try again later"
        )

    otp: str = generate_otp(6)
    otp_key = f"otp:{phone}"
    await redis_client.set(otp_key, otp, ex=OTP_EXPIRY)

    print(f"SMS to {phone}: {otp}")

    return True


async def verify_otp(phone: str, user_otp: str) -> bool:
    """
    Verify OTP with brute-force protection.

    Raises:
        OTPLocked: If the phone number is locked due to excessive failures.
        OTPExpired: If the OTP is expired or not found.
        OTPMismatch: If the provided OTP is incorrect.

    Returns:
        True if OTP verification succeeds.
    """
    if await is_locked(phone):
        raise OTPLocked(
            "Too many failed verification attempts. Try later."
        )

    otp_key = f"otp:{phone}"
    saved_otp: str | None = await redis_client.get(otp_key)

    if not saved_otp:
        await _increment_failed_attempts(phone)
        raise OTPExpired(
            "OTP expired or not found. Request a new OTP."
        )

    if saved_otp != user_otp:
        attempts: int = await _increment_failed_attempts(phone)
        raise OTPMismatch(
            f"OTP incorrect. Attempt {attempts}/{OTP_VERIFY_MAX_ATTEMPTS}."
        )

    await redis_client.delete(otp_key)
    await _clear_failed_attempts(phone)

    return True
