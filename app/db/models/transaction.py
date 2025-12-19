from __future__ import annotations
from typing import Optional, List
from uuid import uuid4
from enum import Enum as PyEnum
from datetime import datetime

from decimal import Decimal 
from sqlalchemy import (
    String, Numeric, Enum, ForeignKey, JSON, TIMESTAMP
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import (
    DeclarativeBase, Mapped, mapped_column, relationship
)
from sqlalchemy.sql import func

from app.db.base import Base
from app.domain.enums import CurrencyCode, TransactionStatus


class Transaction(Base):
    __tablename__ = "transactions"

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    idempotency_key: Mapped[Optional[str]] = mapped_column(String, index=True, unique=True)
    sender_account: Mapped[UUID] = mapped_column(ForeignKey("accounts.id"))
    receiver_account: Mapped[UUID] = mapped_column(ForeignKey("accounts.id"))
    amount: Mapped[Decimal] = mapped_column(Numeric(20, 6), nullable=False)
    currency: Mapped[CurrencyCode] = mapped_column(String, nullable=False)
    status: Mapped[TransactionStatus] = mapped_column(
        Enum(TransactionStatus), default=TransactionStatus.PENDING
    )
    additional_metadata: Mapped[Optional[dict]] = mapped_column(JSON)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )

    # Relationships
    sender_account_obj: Mapped["Account"] = relationship(
        "Account",
        foreign_keys=[sender_account],
        back_populates="sent_transactions"
    )
    receiver_account_obj: Mapped["Account"] = relationship(
        "Account",
        foreign_keys=[receiver_account],
        back_populates="received_transactions"
    )
    ledger_entries: Mapped[List["LedgerEntry"]] = relationship(
        back_populates="transaction",
        cascade="all, delete-orphan"
    )
