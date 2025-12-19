from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from uuid import uuid4
from decimal import Decimal

from app.db.models.account import Account
from app.domain.enums import CurrencyCode
from app.services.audit_log import create_audit_log
from fastapi import HTTPException, status


class AccountService:
    async def create_account(self, db, user, payload):
        # Validate currency
        currency = payload.currency.upper()

        if currency not in CurrencyCode.__members__:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Unsupported currency. Supported: {', '.join(CurrencyCode)}"
            )

        # Check existing
        result = await db.execute(
            select(Account).where(
                Account.user_id == user.id,
                Account.currency == currency
            )
        )
        existing = result.scalar_one_or_none()

        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"User already has a {currency} account"
            )

        # Create account
        new_acc = Account(
            id=uuid4(),
            user_id=user.id,
            currency=currency,
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
                "currency": currency,
                "initial_balance": "0"
            }
        )
        db.add(audit)

        # Commit
        try:
            await db.commit()
            await db.refresh(new_acc)
        except IntegrityError:
            await db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Database integrity error"
            )

        return new_acc


account_service = AccountService()
