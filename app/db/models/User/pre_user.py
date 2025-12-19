from __future__ import annotations

from datetime import datetime, date
from typing import Optional

from sqlalchemy import (
    String,
    DateTime,
    func,
    CheckConstraint,
    Enum,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base
from app.db.enums import PreUserOnboardingState


class PreUser(Base):
    """
    Represents a partially onboarded user.
    Exists only during signup / onboarding flow.
    """

    __tablename__ = "pre_users"

    __table_args__ = (
        CheckConstraint(
            "length(phone) >= 8",
            name="ck_preusers_phone_min_len",
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)

    phone: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        unique=True,
    )

    onboarding_state: Mapped[PreUserOnboardingState] = mapped_column(
    Enum(
        PreUserOnboardingState,
        name="preuser_onboarding_state",
        native_enum=True,
    ),
    nullable=False,
)

    hashed_password: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True,
    )


    first_name: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    last_name: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)


    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        server_onupdate=func.now(),
        nullable=False,
    )

    def __repr__(self) -> str:  # pragma: no cover
        return (
            f"<PreUser id={self.id} phone={self.phone} "
            f"state={self.onboarding_state}>"
        )

    date_of_birth: Mapped[Optional[date]] = mapped_column(
        nullable=True
    )

    address: Mapped[Optional[str]] = mapped_column(
        String(512),
        nullable=True,
    )

    profile_completed_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
