from fastapi import APIRouter
from app.schemas.User.login import RequestOTP, VerifyOTP
from app.services.User.otp_service import send_otp, verify_otp

router = APIRouter()

@router.post("/send-otp")
async def send_otp_route(payload: RequestOTP):
    await send_otp(payload.phone)
    return {"status": "otp_sent"}