from enum import Enum as PyEnum

class AccountStatus(str, PyEnum):
    ACTIVE = "ACTIVE"
    FROZEN = "FROZEN"
    CLOSED = "CLOSED"

class AccountTier(str, PyEnum):
    LIMITED = "LIMITED"
    FULL = "FULL"


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

class PreUserOnboardingState(str, PyEnum):
    OTP_SENT = "OTP_SENT"
    OTP_VERIFIED = "OTP_VERIFIED"
    PROFILE_DONE = "PROFILE_DONE"
    READY_FOR_USER = "READY_FOR_USER"
