from __future__ import annotations
from typing import Any

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.User.pre_user import PreUser

class PreUserRepository:
    """
    Handles persistence for users who haven't finished signing up yet.
    Mainly used to track where a user is in the onboarding flow.
    """

    async def upsert_by_phone(
        self,
        db: AsyncSession,
        *,
        phone: str,
        onboarding_state: str,
    ) -> PreUser:
        """
        Check if we've seen this phone number before. If yes, just update their 
        progress; if not, create a new record so they can start onboarding.
        """
        result = await db.execute(
            select(PreUser).where(PreUser.phone == phone)
        )
        preuser = result.scalar_one_or_none()

        if preuser:
            preuser.onboarding_state = onboarding_state
        else:
            preuser = PreUser(
                phone=phone,
                onboarding_state=onboarding_state,
            )
            db.add(preuser)

        await db.commit()
        await db.refresh(preuser)
        return preuser

    async def get_by_phone(self, db: AsyncSession, phone: str) -> PreUser:
        """
        Find a specific pre-user using their phone number. 
        Throws an error if the phone number isn't in our system.
        """
        result = await db.execute(
            select(PreUser).where(PreUser.phone == phone)
        )
        return result.scalar_one()

    async def get(self, db: AsyncSession, preuser_id: int) -> PreUser:
        """
        Fetch a pre-user by their internal database ID.
        """
        result = await db.execute(
            select(PreUser).where(PreUser.id == preuser_id)
        )
        return result.scalar_one()

    async def update_state(
        self,
        db: AsyncSession,
        *,
        preuser_id: int,
        onboarding_state: str,
    ) -> None:
        """
        Quickly update which step of the signup process the user is currently on.
        """
        await db.execute(
            update(PreUser)
            .where(PreUser.id == preuser_id)
            .values(onboarding_state=onboarding_state)
        )
        await db.commit()

    async def update_profile(
        self,
        db: AsyncSession,
        preuser_id: int,
        profile_data: dict[str, Any],
    ) -> None:
        """
        Bulk update multiple profile fields at once. 
        Make sure the keys in 'profile_data' actually exist on the PreUser model.
        """
        await db.execute(
            update(PreUser)
            .where(PreUser.id == preuser_id)
            .values(**profile_data)
        )
        await db.commit()