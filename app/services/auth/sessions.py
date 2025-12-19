from app.core.security.tokens import (
    create_access_token,
    create_refresh_token,
)
from app.services.auth.refresh_store import store_refresh_token


async def issue_session(
    *,
    db,
    user,
) -> dict[str, str]:
    """
    Issue session tokens after successful login routing.
    """

    access_token = create_access_token(
        user_id=str(user.id),
        tier=user.account.tier,
        status=user.status,
    )

    refresh_token = create_refresh_token(user_id=str(user.id))

    await store_refresh_token(
        db=db,
        user_id=str(user.id),
        refresh_token=refresh_token,
    )

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
    }
