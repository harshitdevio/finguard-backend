from enum import Enum
from dataclasses import dataclass


class AuthStatus(str, Enum):
    AUTHENTICATED = "AUTHENTICATED"
    ONBOARDING_REQUIRED = "ONBOARDING_REQUIRED"
    DENIED = "DENIED"

@dataclass(frozen=True)
class LoginResult:
    auth_status: AuthStatus
    account_tier: str | None = None
    requires_step_up: bool = False
    access_token: str | None = None
