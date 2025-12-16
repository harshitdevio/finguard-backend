"""
Shared hashing primitives and security utilities.

This module defines common building blocks used by all hashing components
(passwords, PINs, OTPs) across the system.

Responsibilities:
- Loading and managing the global server-side pepper
- Applying the pepper to secrets in a consistent, explicit manner
- Providing constant-time comparison utilities
- Defining the Hasher protocol used by hashing implementations

Security notes:
- The pepper is required to be present at runtime and the application
  will fail fast if it is missing.
- Pepper application uses an explicit boundary to avoid ambiguity.
- All consumers are expected to treat this module as security-critical.

This module intentionally contains no hashing algorithms itself.
"""

from __future__ import annotations

import os
import hmac
from typing import Final

PEPPER_ENV_KEY: Final[str] = "PASSWORD_PEPPER"

def get_pepper() -> str:
    """
    Load global pepper from environment.
    Intentionally fails hard if missing.
    """
    pepper = os.getenv(PEPPER_ENV_KEY)
    if not pepper:
        raise RuntimeError(
            f"{PEPPER_ENV_KEY} must be set for cryptographic operations"
        )
    return pepper

def apply_pepper(secret: str, pepper: str) -> str:
    """
    Combine secret with pepper using explicit boundary.
    """
    if not secret:
        raise ValueError("Secret cannot be empty")

    return f"{secret}::{pepper}"

def constant_time_equals(a: str, b: str) -> bool:
    """
    Prevent timing attacks during secret comparison.
    """
    if not a or not b:
        return False

    return hmac.compare_digest(a, b)


class HashingError(Exception):
    """Base exception for hashing-related failures."""


from typing import Protocol

class Hasher(Protocol):
    """
    Interface for components that transform a secret into a persistent,
    non-reversible representation and later verify it.

    A Hasher is responsible for:
    - Hashing a secret for storage (e.g. database, cache)
    - Verifying a provided secret against a previously stored hash

    This protocol defines behavior, not implementation.
    Implementations may use different algorithms and security models
    (e.g. Argon2, HMAC, etc.) as long as they honor this interface.

    Notes:
    - This is a structural (duck-typed) interface used for static type checking.
    - It imposes no runtime behavior or security guarantees by itself.
    - Not all secrets (e.g. short-lived OTPs) are required to implement this.

    Methods:
        hash(secret): Return a string suitable for persistent storage.
        verify(secret, hashed): Return True if the secret matches the stored value.
    """

    def hash(self, secret: str) -> str:
        """Hash a secret into a persistent, non-reversible representation."""
        ...

    def verify(self, secret: str, hashed: str) -> bool:
        """Verify a secret against a previously generated hash."""
        ...
