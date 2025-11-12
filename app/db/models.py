from __future__ import annotations
from typing import Optional, List
from uuid import uuid4
from enum import Enum as PyEnum

from decimal import Decimal 
from sqlalchemy import (
    String, Numeric, Enum, ForeignKey, JSON, TIMESTAMP
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import (
    DeclarativeBase, Mapped, mapped_column, relationship
)
from sqlalchemy.sql import func


class Base(DeclarativeBase):
    pass


class AccountStatus(str, PyEnum):
    ACTIVE = "ACTIVE"
    FROZEN = "FROZEN"
    CLOSED = "CLOSED"


class TransactionStatus(str, PyEnum):
    PENDING = "PENDING"
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"
    FLAGGED = "FLAGGED"

class CurrencyCode(str, PyEnum):
    USD = "USD"
    INR = "INR"
    EUR = "EUR"

class LedgerEntryType(str, PyEnum):
    DEBIT = "DEBIT"
    CREDIT = "CREDIT"

class Account(Base):
    __tablename__ = "accounts"

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    user_id: Mapped[Optional[UUID]] = mapped_column(UUID(as_uuid=True))
    currency: Mapped[CurrencyCode] = mapped_column(Enum(CurrencyCode), default=CurrencyCode.INR ,nullable=False)
    balance: Mapped[Decimal] = mapped_column(Numeric(20, 6), nullable=False, default=0)
    status: Mapped[AccountStatus] = mapped_column(Enum(AccountStatus), default=AccountStatus.ACTIVE)
    created_at: Mapped = mapped_column(TIMESTAMP(timezone=True), server_default=func.now())

    # Reverse relationships
    sent_transactions: Mapped[List["Transaction"]] = relationship(
        back_populates="sender_account_obj",
        foreign_keys="Transaction.sender_account",
        cascade="all, delete-orphan"
    )
    received_transactions: Mapped[List["Transaction"]] = relationship(
        back_populates="receiver_account_obj",
        foreign_keys="Transaction.receiver_account",
        cascade="all, delete-orphan"
    )
    ledger_entries: Mapped[List["LedgerEntry"]] = relationship(
        back_populates="account",
        cascade="all, delete-orphan"
    )


class Transaction(Base):
    __tablename__ = "transactions"

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    idempotency_key: Mapped[Optional[str]] = mapped_column(String, index=True, nullable=False, unique=True)
    sender_account: Mapped[UUID] = mapped_column(ForeignKey("accounts.id"))
    receiver_account: Mapped[UUID] = mapped_column(ForeignKey("accounts.id"))
    amount: Mapped[Decimal] = mapped_column(Numeric(20, 6), nullable=False)
    currency: Mapped[str] = mapped_column(String, nullable=False)
    status: Mapped[TransactionStatus] = mapped_column(
        Enum(TransactionStatus), default=TransactionStatus.PENDING
    )
    metadata: Mapped[Optional[dict]] = mapped_column(JSON)
    created_at: Mapped = mapped_column(TIMESTAMP(timezone=True), server_default=func.now())
    updated_at: Mapped = mapped_column(
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


class LedgerEntry(Base):
    __tablename__ = "ledger_entries"

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    account_id: Mapped[UUID] = mapped_column(ForeignKey("accounts.id"), nullable=False)
    transaction_id: Mapped[UUID] = mapped_column(ForeignKey("transactions.id"), nullable=False)
    entry_type: Mapped[LedgerEntryType] = mapped_column(Enum(LedgerEntryType), nullable=False)  # "DEBIT" or "CREDIT"
    amount: Mapped[Decimal] = mapped_column(Numeric(20, 6), nullable=False)
    balance_after: Mapped[Optional[Decimal]] = mapped_column(Numeric(20, 6))
    created_at: Mapped = mapped_column(TIMESTAMP(timezone=True), server_default=func.now())

    # Relationships
    account: Mapped["Account"] = relationship("Account", back_populates="ledger_entries")
    transaction: Mapped["Transaction"] = relationship("Transaction", back_populates="ledger_entries")
