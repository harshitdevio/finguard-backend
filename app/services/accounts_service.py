from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from uuid import uuid4
from decimal import Decimal

from app.db.models.account import Account
from app.db.enums import CurrencyCode
from app.services.audit_log import create_audit_log
from fastapi import HTTPException, status


class AccountService:
    async def create_account(self, db, user, payload):
        # Validate currency
        if payload.currency.upper() not in CurrencyCode.__members__:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Unsupported currency. Supported: {', '.join(CurrencyCode)}"
            )

        # Check existing
        existing = db.execute(
            select(Account).where(
                Account.user_id == user.id,
                Account.currency == payload.currency.upper()
            )
        ).scalar_one_or_none()

        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"User already has a {payload.currency.upper()} account"
            )

        # Create account
        new_acc = Account(
            id=uuid4(),
            user_id=user.id,
            currency=payload.currency.upper(),
            balance=Decimal("0"),
            status="ACTIVE"
        )

        db.add(new_acc)

        # Audit log
        audit = create_audit_log(
            db=db,
            actor=str(user.id),
            action="CREATE_ACCOUNT",
            object_type="ACCOUNT",
            object_id=new_acc.id,
            payload={
                "currency": new_acc.currency,
                "initial_balance": "0"
            }
        )
        db.add(audit)

        # Commit
        try:
            db.commit()
            db.refresh(new_acc)
        except IntegrityError:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Database integrity error"
            )

        return new_acc


# Create global instance
account_service = AccountService()
