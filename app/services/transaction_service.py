from sqlalchemy import select
from sqlalchemy.orm import Session
from app.db.models import Transaction, Account, LedgerEntry, TransactionStatus
from fastapi import HTTPException
from uuid import uuid4


def create_transaction(db: Session, payload):
    # Step 1 — Check if idempotency_key already exists
    existing_tx = db.execute(
        select(Transaction).where(Transaction.idempotency_key == payload.idempotency_key)
    ).scalar_one_or_none()

    if existing_tx:
        return existing_tx

    # Step 2 — Start DB transaction
    with db.begin():
        sender = db.execute(
            select(Account).where(Account.id == payload.sender_account).with_for_update()
        ).scalar_one_or_none()

        receiver = db.execute(
            select(Account).where(Account.id == payload.receiver_account).with_for_update()
        ).scalar_one_or_none()

        if not sender:
            raise HTTPException(status_code=404, detail="Sender's account not found!")
        
        if not receiver:
            raise HTTPException(status_code=404, detail="Receiver's account not found!")

        if sender.balance < payload.amount:
            raise HTTPException(status_code=400, detail="Insufficient funds")

        # Step 3 — Create transaction
        tx = Transaction(
            id=uuid4(),
            idempotency_key=payload.idempotency_key,
            sender_account=payload.sender_account,
            receiver_account=payload.receiver_account,
            amount=payload.amount,
            currency=payload.currency,
            metadata=payload.metadata,
            status=TransactionStatus.PENDING,
        )
        db.add(tx)

        # Step 4 — Apply ledger updates
        sender.balance -= payload.amount
        receiver.balance += payload.amount

        db.add(LedgerEntry(
            account_id=sender.id,
            transaction_id=tx.id,
            entry_type="DEBIT",
            amount=payload.amount,
            balance_after=sender.balance
        ))
        db.add(LedgerEntry(
            account_id=receiver.id,
            transaction_id=tx.id,
            entry_type="CREDIT",
            amount=payload.amount,
            balance_after=receiver.balance
        ))

        tx.status = TransactionStatus.SUCCESS
        db.add(tx)

    return tx
