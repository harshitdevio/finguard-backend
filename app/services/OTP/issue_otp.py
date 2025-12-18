from app.core.redis import redis_client
from app.core.security.otp import OTP_TTL
from app.core.security.otp import generate_otp, OTP_EXPIRY
from app.core.security.hashing.otp import hash_otp

async def issue_otp(*, phone: str) -> str:
    """
    Generate, hash, and store an OTP for a phone number.

    Returns the raw OTP so it can be sent via SMS.
    """

    otp = generate_otp()
    otp_hash = hash_otp(otp=otp, identifier=phone)

    redis_key = f"otp:verify:{phone}"

    await redis_client.set(
        redis_key,
        otp_hash,
        ex=OTP_EXPIRY,
    )

    return otp
