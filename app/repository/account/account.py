# app/repository/account/account.py

from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.account import Account
from app.domain.enums import AccountTier, AccountStatus


class AccountRepository:

    async def create_limited(
        self,
        *,
        db: AsyncSession,
        user_id: int,
        daily_limit: int,
    ) -> Account:
        account = Account(
            user_id=user_id,
            tier=AccountTier.LIMITED,
            status=AccountStatus.ACTIVE,
            daily_limit=daily_limit,
        )

        db.add(account)
        await db.commit()
        await db.refresh(account)
        return account
