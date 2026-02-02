# Architecture Documentation - File Vault

## Overview

**File Vault** is a zero-knowledge file encryption tool that implements **AES-256-CFB** with **PBKDF2-HMAC-SHA256** key derivation. Its modular design allows for professional scalability and maintenance.

## System Architecture

```text
┌─────────────────────────────────────────────────┐
│                   main.py                        │
│           (CLI - User Interface)                 │
└────────────────┬────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────┐
│              core/__init__.py                    │
│           (Package Entry Point)                  │
└────────────────┬────────────────────────────────┘
                 │
       ┌─────────┴─────────┐
       ▼                   ▼
┌──────────────┐    ┌──────────────────┐
│security_utils│    │   encryptor.py   │
│     .py      │    │  (FileVault)     │
│              │◄───┤                  │
│ - KDF        │    │ - encrypt_file() │
│ - Salt/IV    │    │ - decrypt_file() │
│ - Validation │    │ - get_file_info()│
└──────────────┘    └──────────────────┘
       │                   │
       └─────────┬─────────┘
                 ▼
┌─────────────────────────────────────────────────┐
│         cryptography (external library)         │
│   - AES-256-CFB (Cipher)                        │
│   - PBKDF2HMAC (Key Derivation)                 │
└─────────────────────────────────────────────────┘

```

## Core Modules

### 1. security_utils.py

**Purpose:** Provides low-level cryptographic functions.

**Key Functions:**

* `generate_salt()`: Generates a 16-byte random salt.
* `generate_iv()`: Generates a 16-byte random IV.
* `derive_key(password, salt)`: Derives a 256-bit key using PBKDF2.
* `validate_password(password)`: Validates password strength.

**Security Constants:**

* `SALT_SIZE = 16` (128 bits)
* `IV_SIZE = 16` (128 bits)
* `KEY_SIZE = 32` (256 bits)
* `ITERATIONS = 100,000` (PBKDF2 iterations)

### 2. encryptor.py

**Purpose:** Implements file encryption/decryption logic.

**Main Class:** `FileVault`

**Public Methods:**

* `encrypt_file(file_path, password, output_path=None)`
* `decrypt_file(file_path, password, output_path=None)`
* `get_file_info(file_path)`

**Processing Strategy:**

* Chunk-based reading/writing (64KB default).
* Minimizes RAM usage.
* Supports files of any size.

### 3. main.py

**Purpose:** Command Line Interface (CLI).

**Commands:**

* `encrypt <file>`: Encrypts a file.
* `decrypt <file>`: Decrypts a file.
* `info <file>`: Displays info about the encrypted file.

**Features:**

* Terminal colors (Windows/Linux/macOS compatible).
* Secure password input (no echo in terminal).
* Argument validation with `argparse`.
* Robust error handling.

---

## Encryption Flow

1. **Original File**
2. Read user password.
3. Generate random **Salt** (16B) and **IV** (16B).
4. Derive key with **PBKDF2** (Password + Salt → 32B Key).
5. Create **AES-256-CFB** cipher with Key and IV.
6. Write Salt + IV to the output file.
7. Read file by chunks → Encrypt each chunk → Write encrypted chunk.
8. Finalize and close files → **Encrypted File**.

## Decryption Flow

1. **Encrypted File**
2. Read Salt (first 16 bytes) and IV (next 16 bytes).
3. Read user password.
4. Derive key with **PBKDF2** (Password + Salt → 32B Key).
5. Create **AES-256-CFB** cipher with Key and IV.
6. Read encrypted data by chunks → Decrypt each chunk → Write decrypted chunk.
7. Finalize and close files → **Decrypted File**.

---

## Encrypted File Format

* **Bytes 0-15:** Salt (16 bytes) - Randomly generated, used for key derivation.
* **Bytes 16-31:** IV (16 bytes) - Initialization Vector; ensures same content → different ciphertexts.
* **Bytes 32+:** Encrypted Data - Original content encrypted with AES-256-CFB. Same size as original.

**Total Size:** 32 + original_size bytes.

---

## Cryptographic Specifications

### AES-256-CFB (Cipher Feedback Mode)

* **Algorithm:** Advanced Encryption Standard.
* **Key Size:** 256 bits (Maximum security).
* **Mode:** CFB (Cipher Feedback).
* **Block Size:** 128 bits.
* **Pros:** No padding required; converts block cipher to stream cipher; errors don't propagate beyond one block.
* **Cons:** No built-in authentication (consider HMAC for production); ciphertext tampering is not automatically detected.

### PBKDF2-HMAC-SHA256

* **Algorithm:** Password-Based Key Derivation Function 2.
* **PRF:** HMAC-SHA256.
* **Iterations:** 100,000 (OWASP recommended).
* **Output:** 256 bits (32 bytes).
* **Why PBKDF2:** Industry standard (NIST, OWASP); resistant to brute-force attacks; computationally expensive for attackers.

---

## Security Considerations

### ✅ Implemented

* **Strong Confidentiality:** AES-256 (Military grade), unique Salt/IV per file.
* **Password Protection:** PBKDF2 with 100K iterations, Salt prevents rainbow tables, no-echo terminal input.
* **Zero-Knowledge Design:** No passwords stored, no master keys, no backdoors.
* **Memory Efficiency:** Chunk processing, supports large files, constant RAM usage.

### ⚠️ Known Limitations

* **No Authentication:** CFB does not detect modifications. *Solution: Add HMAC-SHA256.*
* **No Compression:** Encrypted files do not compress. *Solution: Compress before encrypting.*
* **Single Password:** No password recovery. *Solution: Use a password manager.*
* **Proprietary Format:** Simple custom format. *Solution: Consider Age or OpenPGP.*

---

## Future Improvements

* **Short Term:** Add HMAC for authentication; implement integrity verification; multi-file support.
* **Medium Term:** Directory encryption; integrated compression; encrypted metadata (filenames).
* **Long Term:** Standard compatibility (Age, OpenPGP); HSM support; Post-Quantum algorithms; Multi-platform GUI.

---

## Design Patterns Used

1. **Strategy Pattern:** Allows for easy encryption algorithm swapping.
2. **Factory Pattern:** `generate_salt()` and `generate_iv()` act as factories for cryptographic objects.
3. **Single Responsibility Principle:** `security_utils` (crypto), `encryptor` (file logic), `main` (UI).
4. **Dependency Injection:** `FileVault` receives `chunk_size` as a parameter, facilitating testing.

---

## Testing

**Suite (test_vault.py):**

* **Basic Encrypt/Decrypt:** Verifies the full flow and content integrity.
* **Incorrect Password:** Verifies that a wrong password results in corrupted/unreadable data.
* **Large Files:** Verifies chunk processing and memory efficiency.
* **File Info:** Verifies metadata reading.
* **Password Validation:** Tests security rules.

**Run Tests:** `python test_vault.py`

---

## Compatibility & Performance

* **Platforms:** Linux, macOS (10.15+), Windows (10/11).
* **Requirements:** Python 3.8+, `cryptography >= 42.0.0`.

| Operation | HDD | SSD | NVMe |
| --- | --- | --- | --- |
| **Encryption** | 50-100 MB/s | 200-500 MB/s | 1-2 GB/s |
| **Decryption** | 50-100 MB/s | 200-500 MB/s | 1-2 GB/s |

---

## Conclusion

**File Vault** is a functional educational tool demonstrating modular architecture, correct cryptographic implementation, and zero-knowledge design. For production use, consider adding authentication (HMAC), standard formats, and professional security auditing.
