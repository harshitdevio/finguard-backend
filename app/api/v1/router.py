from fastapi import APIRouter
from . import accounts, transactions

router = APIRouter(prefix="/v1")

router.include_router(accounts.router)
router.include_router(transactions.router)
router.include_router(transactions.router)