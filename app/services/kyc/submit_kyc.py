from app.repository.user.user_kyc import UserKYCRepository
from app.core.Utils.kyc_ref_hash import hash_kyc_ref


class KYCAlreadySubmitted(Exception):
    pass


async def submit_kyc(
    *,
    db,
    user,
    document_type: str,
    document_number: str,
) -> None:
    """
    Submit KYC details for async verification.
    """

    repo = UserKYCRepository()

    existing = await repo.get_by_user_id(db, user.id)
    if existing:
        raise KYCAlreadySubmitted()

    await repo.create(
        db=db,
        user_id=user.id,
        document_type=document_type,
        document_number_hash=hash_kyc_ref(document_number),
    )
