from fastapi import APIRouter
from app.schemas.User.login import RequestOTP, VerifyOTP
from app.services.OTP.otp_service import send_otp, verify_otp

router = APIRouter()

@router.post("/send-otp")
async def send_otp_route(payload: RequestOTP):
    await send_otp(payload.phone)
    return {"status": "otp_sent"}

@router.post("/verify-otp")
async def verify_otp_route(payload: VerifyOTP):
    valid = await verify_otp(payload.phone, payload.otp)

    if not valid:
        return {"valid": False}
    return {"valid": True}