from datetime import datetime, date
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.enums import PreUserOnboardingState
from app.db.models.User.pre_user import PreUser
from app.repository.user.pre_user import PreUserRepository


class PreUserProfileError(Exception):
    """Base exception for PreUser profile operations."""


class InvalidPreUserState(PreUserProfileError):
    """Raised when profile is completed in an invalid onboarding state."""


class ProfileAlreadyCompleted(PreUserProfileError):
    """Raised when profile is already completed."""


async def complete_basic_profile(
    *,
    db: AsyncSession,
    phone: str,
    first_name: str,
    last_name: str,
    date_of_birth: date,
    address: str,
) -> PreUser:
    """
    Complete basic profile details for a PreUser.

    Rules:
    - Allowed only after credentials are set
    - Write-once operation
    - Marks profile completion timestamp
    """

    repo = PreUserRepository()

    preuser = await repo.get_by_phone(db, phone)

    # State guard
    if preuser.onboarding_state != PreUserOnboardingState.CREDENTIALS_SET:
        raise InvalidPreUserState(
            f"Cannot complete profile in state {preuser.onboarding_state}"
        )

    # Write-once guard
    if preuser.profile_completed_at is not None:
        raise ProfileAlreadyCompleted("Profile already completed")

    await repo.update_profile(
        db,
        preuser_id=preuser.id,
        profile_data={
            "first_name": first_name,
            "last_name": last_name,
            "date_of_birth": date_of_birth,
            "address": address,
            "profile_completed_at": datetime.utcnow(),
            "onboarding_state": PreUserOnboardingState.PROFILE_DONE,
        },
    )

    return await repo.get(db, preuser.id)
