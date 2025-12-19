from __future__ import annotations
from typing import Optional, TYPE_CHECKING
from uuid import uuid4
from datetime import datetime

from decimal import Decimal
from sqlalchemy import Numeric, Enum, ForeignKey, TIMESTAMP
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from app.db.base import Base
from app.domain.enums import LedgerEntryType

class LedgerEntry(Base):
    __tablename__ = "ledger_entries"

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    account_id: Mapped[UUID] = mapped_column(ForeignKey("accounts.id"), nullable=False)
    transaction_id: Mapped[UUID] = mapped_column(ForeignKey("transactions.id"), nullable=False)
    entry_type: Mapped[LedgerEntryType] = mapped_column(Enum(LedgerEntryType), nullable=False)  # "DEBIT" or "CREDIT"
    amount: Mapped[Decimal] = mapped_column(Numeric(20, 6), nullable=False)
    balance_after: Mapped[Optional[Decimal]] = mapped_column(Numeric(20, 6))
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), server_default=func.now())

    # Relationships
    account: Mapped["Account"] = relationship("Account", back_populates="ledger_entries")
    transaction: Mapped["Transaction"] = relationship("Transaction", back_populates="ledger_entries")
