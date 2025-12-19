from datetime import datetime
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.User.user_kyc import UserKYC
from app.domain.kyc.enums import KYCStatus


class UserKYCRepository:

    async def get_by_user_id(
        self,
        db: AsyncSession,
        user_id,
    ) -> UserKYC | None:
        result = await db.execute(
            select(UserKYC).where(UserKYC.user_id == user_id)
        )
        return result.scalar_one_or_none()

    async def create(
        self,
        *,
        db: AsyncSession,
        user_id,
        document_type: str,
        document_number_hash: str,
    ) -> UserKYC:
        kyc = UserKYC(
            user_id=user_id,
            status=KYCStatus.PENDING,
            document_type=document_type,
            document_number=document_number_hash,
            submitted_at=datetime.utcnow(),
        )

        db.add(kyc)
        await db.commit()
        await db.refresh(kyc)
        return kyc

