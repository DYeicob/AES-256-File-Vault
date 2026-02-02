"""
Core cryptographic components for File Vault.

This package contains the encryption/decryption engine and security utilities.
"""

from .encryptor import FileVault
from .security_utils import (
    generate_salt,
    generate_iv,
    derive_key,
    validate_password,
    SALT_SIZE,
    IV_SIZE,
    KEY_SIZE,
    ITERATIONS
)

__all__ = [
    'FileVault',
    'generate_salt',
    'generate_iv',
    'derive_key',
    'validate_password',
    'SALT_SIZE',
    'IV_SIZE',
    'KEY_SIZE',
    'ITERATIONS'
]
