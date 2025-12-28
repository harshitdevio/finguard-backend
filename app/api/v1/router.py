from fastapi import APIRouter
from . import accounts, transactions, auth

router = APIRouter(prefix="/v1")

router.include_router(accounts.router)
router.include_router(transactions.router)
router.include_router(auth.router)