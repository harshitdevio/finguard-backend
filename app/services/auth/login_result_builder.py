from app.domain.auth.login_result import LoginResult, AuthStatus

def authenticated_result(
    *,
    access_token: str,
    account_tier: str,
    requires_step_up: bool,
) -> LoginResult:
    return LoginResult(
        auth_status=AuthStatus.AUTHENTICATED,
        access_token=access_token,
        account_tier=account_tier,
        requires_step_up=requires_step_up,
    )


def onboarding_required_result() -> LoginResult:
    return LoginResult(
        auth_status=AuthStatus.ONBOARDING_REQUIRED,
    )


def denied_result() -> LoginResult:
    return LoginResult(
        auth_status=AuthStatus.DENIED,
    )
