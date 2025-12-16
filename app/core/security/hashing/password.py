"""
Password hashing utilities for Fintech authentication.

This module provides a dedicated password hasher implementation using
Argon2id with parameters tuned for high security and resistance to
offline brute-force attacks.

Design principles:
- Password hashing is strictly separated from PIN and OTP hashing.
- A server-side pepper is applied before hashing to mitigate the impact
  of database compromise.
- Argon2id parameters are chosen to favor security over latency, as
  password verification is not a high-frequency operation.

This module implements the `Hasher` interface and is intended to be used
by authentication and account management services.

Do NOT reuse this module for PINs or OTPs.
"""

from __future__ import annotations

from passlib.context import CryptContext
from passlib.exc import UnknownHashError

from app.core.security.hashing.base import get_pepper, apply_pepper, HashingError, Hasher


pwd_context = CryptContext(
    schemes=["argon2"],
    deprecated="auto",
    argon2__type="ID",
    argon2__memory_cost=65536,  # 64 MB
    argon2__time_cost=3,
    argon2__parallelism=1,
    argon2__hash_len=32,
    argon2__salt_size=16,
)


class PasswordHasher(Hasher):
    """
    Argon2id-based password hasher implementation.

    This class encapsulates password hashing, verification, and rehash
    detection using a consistent configuration and a server-side pepper.
    """

    def __init__(self):
        """
        Initialize the password hasher.

        The server-side pepper is loaded once during initialization
        and reused for all hashing and verification operations.
        """
        self._pepper = get_pepper()

    def hash(self, password: str) -> str:
        """
        Hash a raw password using Argon2id.

        The password is peppered using a server-side secret before being
        hashed with the configured Argon2id parameters.

        Args:
            password: The raw password provided by the user.

        Returns:
            A secure Argon2id hash of the peppered password.

        Raises:
            HashingError: If the password is empty or hashing fails.
        """
        if not password:
            raise HashingError("Password cannot be empty")

        peppered = apply_pepper(password, self._pepper)
        return pwd_context.hash(peppered)
    
    def verify(self, password: str, hashed: str) -> bool:
        """
        Verify a password against a stored password hash.

        The password is peppered using the current server-side pepper
        and verified against the stored Argon2id hash.

        This method is fail-safe and returns False for invalid input,
        unknown hash formats, or verification failures.

        Args:
            password: The raw password provided by the user.
            hashed: The stored Argon2id password hash.

        Returns:
            True if the password matches the stored hash, False otherwise.
        """
        if not password or not hashed:
            return False

        try:
            peppered = apply_pepper(password, self._pepper)
            return pwd_context.verify(peppered, hashed)
        except UnknownHashError:
            return False
        
        
    def needs_rehash(self, hashed: str) -> bool:
        """
        Determine whether a stored password hash needs to be rehashed.

        This is used to transparently upgrade password hashes when
        Argon2 parameters are updated, typically after a successful
        password verification.

        Args:
            hashed: The stored password hash.

        Returns:
            True if the hash should be rehashed using current parameters,
            False otherwise.
        """
        return pwd_context.needs_update(hashed)
