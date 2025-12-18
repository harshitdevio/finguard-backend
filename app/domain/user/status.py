from enum import Enum


class OnboardingState(str, Enum):
    PHONE_SUBMITTED = "phone_submitted"

    OTP_SENT = "otp_sent"
    OTP_VERIFIED = "otp_verified"

    PREUSER_CREATED = "preuser_created"

    CREDENTIALS_SET = "credentials_set"

    PROFILE_COMPLETED = "profile_completed"

    RISK_PASSED = "risk_passed"
    LIMITED_ACCOUNT = "limited_account"

    KYC_SUBMITTED = "kyc_submitted"
    KYC_VERIFIED = "kyc_verified"
    
    FULL_ACCESS = "full_access"