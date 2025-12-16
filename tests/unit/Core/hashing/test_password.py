"""
Unit tests for password hashing utilities.

This test suite validates the PasswordHasher implementation including:
- Proper Argon2id parameter configuration
- Pepper application and consistency
- Hash generation and verification
- Error handling for edge cases
- Security properties (timing attacks, rehashing)
- Fail-fast behavior for missing pepper

Test philosophy:
- Unit tests mock external dependencies (env vars, pepper loading)
- Focus on contract adherence and security guarantees
- Validate both happy paths and failure modes
"""

from __future__ import annotations

import pytest
from unittest.mock import patch, MagicMock
from passlib.exc import UnknownHashError

from app.core.security.hashing.password import PasswordHasher
from app.core.security.hashing.base import HashingError


class TestPasswordHasherInitialization:
    """Test suite for PasswordHasher initialization and configuration."""

    def test_initializes_with_valid_pepper(self):
        """Should successfully initialize when pepper is available."""
        with patch("app.core.security.hashing.password.get_pepper", return_value="test-pepper-secret"):
            hasher = PasswordHasher()
            assert hasher._pepper == "test-pepper-secret"