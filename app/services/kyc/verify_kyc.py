from app.domain.kyc.enums import KYCStatus
from app.repository.user.user_kyc import UserKYCRepository


class KYCNotSubmitted(Exception):
    pass


async def approve_kyc(
    *,
    db,
    user,
    admin_id: str = "system",
) -> None:
    repo = UserKYCRepository()

    kyc = await repo.get_by_user_id(db, user.id)
    if not kyc:
        raise KYCNotSubmitted()

    await repo.update_status(
        db=db,
        user_id=user.id,
        status=KYCStatus.VERIFIED,
        verified_by=admin_id,
    )

    # Upgrade access
    user.onboarding_state = "FULL_ACCESS"
    await db.commit()


async def reject_kyc(
    *,
    db,
    user,
    admin_id: str = "system",
) -> None:
    repo = UserKYCRepository()

    kyc = await repo.get_by_user_id(db, user.id)
    if not kyc:
        raise KYCNotSubmitted()

    await repo.update_status(
        db=db,
        user_id=user.id,
        status=KYCStatus.REJECTED,
        verified_by=admin_id,
    )

    # User stays limited / blocked
    await db.commit()
