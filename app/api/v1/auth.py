from fastapi import APIRouter, status

from app.schemas.User.login import RequestOTP, VerifyOTP
from app.orchestration.signup import UserOnboarding
from app.auth.OTP.service import send_otp, verify_otp
from app.schemas.User.signup import (
    PhoneSubmitRequest,
    PhoneSubmitResponse,
)


router = APIRouter(tags=["Auth"])

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

@router.post("/signup/phone", response_model=PhoneSubmitResponse)
async def submit_phone(payload: PhoneSubmitRequest):
    return await UserOnboarding.submit_phone(payload.phone)