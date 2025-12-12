from app.core.redis import redis_client
from app.core.securities import generate_otp
from typing import Optional

OTP_EXPIRY = 300 
OTP_MAX_REQUESTS = 3

OTP_VERIFY_MAX_ATTEMPTS = 5         
OTP_VERIFY_WINDOW = 15 * 60          
OTP_LOCKOUT_TTL = 60 * 60            

class OTPRateLimitExceeded(Exception):
    """Raised when the user exceeds the allowed OTP request limit."""

class OTPException(Exception):
    """Base OTP exception."""

class OTPTooManyRequests(OTPException):
    """Raised when user requests OTP too frequently."""

class OTPLocked(OTPException):
    """Raised when phone is temporarily locked due to too many failed verifications."""

class OTPExpired(OTPException):
    """Raised when OTP has expired."""

class OTPMismatch(OTPException):
    """Raised when OTP does not match."""

async def send_otp(phone: str):
    #Check rate limit
    count_key = f"otp_count:{phone}"
    count = await redis_client.incr(count_key)

    if count == 1:
        await redis_client.expire(count_key, OTP_EXPIRY)

    if count > OTP_MAX_REQUESTS:
        raise OTPRateLimitExceeded("Too many OTP requests, Try again later")

    # Generate and store OTP
    otp = generate_otp(6)
    otp_key = f"otp:{phone}"
    await redis_client.set(otp_key, otp, ex=OTP_EXPIRY)

    # Send via provider (dummy)
    print(f"SMS to {phone}: {otp}")  # replace with real SMS API

    return True

async def verify_otp(phone: str, user_otp: str):
    otp_key = f"otp:{phone}"
    saved = await redis_client.get(otp_key)

    if not saved:
        return False

    if saved != user_otp:
        return False

    # OTP correct → delete it
    await redis_client.delete(otp_key)

    return True
