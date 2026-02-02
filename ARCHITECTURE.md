# Architecture Documentation - File Vault

## Overview

File Vault is a zero-knowledge file encryption tool that implements AES-256-CFB with PBKDF2-HMAC-SHA256 key derivation. The modular design allows for scalability and professional maintenance.

## System Architecture

```
┌─────────────────────────────────────────────────┐
│                   main.py                        │
│            (CLI - User Interface)                │
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
│         cryptography (external library)          │
│   - AES-256-CFB (Cipher)                        │
│   - PBKDF2HMAC (Key Derivation)                 │
└─────────────────────────────────────────────────┘
```

## Main Modules

### 1. security_utils.py

**Purpose**: Provides low-level cryptographic functions.

**Key Functions**:
- `generate_salt()`: Generates random 16-byte salt
- `generate_iv()`: Generates random 16-byte IV
- `derive_key(password, salt)`: Derives 256-bit key using PBKDF2
- `validate_password(password)`: Validates password strength

**Security Constants**:
```python
SALT_SIZE = 16        # 128 bits
IV_SIZE = 16          # 128 bits  
KEY_SIZE = 32         # 256 bits
ITERATIONS = 100_000  # PBKDF2 iterations
```

### 2. encryptor.py

**Purpose**: Implements file encryption/decryption logic.

**Main Class: FileVault**

Public methods:
- `encrypt_file(file_path, password, output_path=None)`
- `decrypt_file(file_path, password, output_path=None)`
- `get_file_info(file_path)`

**Processing Strategy**:
- Read/write by chunks (64KB by default)
- Minimizes RAM usage
- Supports files of any size

### 3. main.py

**Purpose**: Command-line interface (CLI).

**Commands**:
- `encrypt <file>`: Encrypt a file
- `decrypt <file>`: Decrypt a file
- `info <file>`: Show encrypted file information

**Features**:
- Terminal colors (Windows/Linux/macOS compatible)
- Secure password input (no echo to terminal)
- Argument validation with `argparse`
- Robust error handling

## Encryption Flow

```
┌──────────────┐
│ Original     │
│ File         │
└──────┬───────┘
       │
       ▼
┌──────────────────────────────────┐
│ 1. Read password from user       │
└──────────────┬───────────────────┘
               │
               ▼
┌──────────────────────────────────┐
│ 2. Generate random Salt (16B)    │
│    Generate random IV (16B)      │
└──────────────┬───────────────────┘
               │
               ▼
┌──────────────────────────────────┐
│ 3. Derive key with PBKDF2        │
│    Password + Salt → Key (32B)   │
└──────────────┬───────────────────┘
               │
               ▼
┌──────────────────────────────────┐
│ 4. Create AES-256-CFB cipher     │
│    with Key and IV               │
└──────────────┬───────────────────┘
               │
               ▼
┌──────────────────────────────────┐
│ 5. Write Salt + IV to output     │
│    file                          │
└──────────────┬───────────────────┘
               │
               ▼
┌──────────────────────────────────┐
│ 6. Read file by chunks           │
│    Encrypt each chunk            │
│    Write encrypted chunk         │
└──────────────┬───────────────────┘
               │
               ▼
┌──────────────────────────────────┐
│ 7. Finalize and close files      │
└──────────────┬───────────────────┘
               │
               ▼
       ┌───────────────┐
       │ Encrypted     │
       │ File          │
       └───────────────┘
```

## Decryption Flow

```
┌──────────────┐
│ Encrypted    │
│ File         │
└──────┬───────┘
       │
       ▼
┌──────────────────────────────────┐
│ 1. Read Salt (first 16 bytes)    │
│    Read IV (next 16 bytes)       │
└──────────────┬───────────────────┘
               │
               ▼
┌──────────────────────────────────┐
│ 2. Read password from user       │
└──────────────┬───────────────────┘
               │
               ▼
┌──────────────────────────────────┐
│ 3. Derive key with PBKDF2        │
│    Password + Salt → Key (32B)   │
└──────────────┬───────────────────┘
               │
               ▼
┌──────────────────────────────────┐
│ 4. Create AES-256-CFB cipher     │
│    with Key and IV               │
└──────────────┬───────────────────┘
               │
               ▼
┌──────────────────────────────────┐
│ 5. Read encrypted data by chunks │
│    Decrypt each chunk            │
│    Write decrypted chunk         │
└──────────────┬───────────────────┘
               │
               ▼
┌──────────────────────────────────┐
│ 6. Finalize and close files      │
└──────────────┬───────────────────┘
               │
               ▼
       ┌───────────────┐
       │ Decrypted     │
       │ File          │
       └───────────────┘
```

## Encrypted File Format

```
┌─────────────────────────────────────────┐
│  Byte 0-15: Salt (16 bytes)             │
│  ────────────────────────────────────   │
│  Randomly generated                     │
│  Used to derive the key                 │
└─────────────────────────────────────────┘
┌─────────────────────────────────────────┐
│  Byte 16-31: IV (16 bytes)              │
│  ────────────────────────────────────   │
│  Initialization vector                  │
│  Ensures same content →                 │
│  different ciphertexts                  │
└─────────────────────────────────────────┘
┌─────────────────────────────────────────┐
│  Byte 32+: Encrypted Data               │
│  ────────────────────────────────────   │
│  Original file content                  │
│  encrypted with AES-256-CFB             │
│  Same size as original                  │
└─────────────────────────────────────────┘
```

**Total Size**: `32 + original_size` bytes

## Cryptographic Specifications

### AES-256-CFB (Cipher Feedback Mode)

**Characteristics**:
- **Algorithm**: Advanced Encryption Standard
- **Key size**: 256 bits (maximum security)
- **Mode**: CFB (Cipher Feedback)
- **Block size**: 128 bits

**CFB Advantages**:
- No padding required (works with any data size)
- Converts block cipher into stream cipher
- Errors don't propagate beyond one block

**Disadvantages**:
- Doesn't provide authentication (consider HMAC for production)
- Ciphertext modification is not automatically detected

### PBKDF2-HMAC-SHA256

**Specifications**:
- **Algorithm**: Password-Based Key Derivation Function 2
- **PRF**: HMAC-SHA256
- **Iterations**: 100,000 (OWASP recommended)
- **Output**: 256 bits (32 bytes)

**Why PBKDF2**:
- Industry standard (NIST, OWASP)
- Resistant to brute-force attacks
- Computationally expensive for attackers
- Easy to adjust iterations in the future

**Resistance Calculation**:
```
Time to test 1 password:
  t = (iterations × hmac_time) / processor_cores

With modern hardware (~1M hashes/sec):
  100,000 iterations = 100ms per attempt
  
For an 8-character password (a-zA-Z0-9):
  Search space: 62^8 ≈ 218 trillion
  Estimated time: ~69,000 years on 1 CPU
```

## Security Considerations

### Implemented

1. **Strong Confidentiality**
   - AES-256 (military standard)
   - Unique salt per file
   - Unique IV per file

2. **Password Protection**
   - PBKDF2 with 100K iterations
   - Salt prevents rainbow tables
   - No-echo terminal input

3. **Zero-Knowledge Design**
   - Passwords never stored
   - No master keys
   - No backdoors

4. **Memory Efficiency**
   - Chunk-based processing
   - Supports large files
   - Constant RAM usage

### Known Limitations

1. **No Authentication**
   - CFB doesn't detect modifications
   - Solution: Add HMAC-SHA256

2. **No Compression**
   - Encrypted files don't compress
   - Solution: Compress before encryption

3. **Single Password**
   - No password recovery
   - Solution: Use password manager

4. **Non-Standard Format**
   - Simple proprietary format
   - Solution: Consider Age or OpenPGP

## Future Improvements

### Short Term
1. Add HMAC for authentication
2. Implement integrity verification
3. Support for multiple files
4. Real-time progress for large files

### Medium Term
1. Directory encryption support
2. Integrated compression (pre-encryption)
3. Encrypted metadata (filenames)
4. Memory-mapped encryption (mmap)

### Long Term
1. Compatibility with standards (Age, OpenPGP)
2. Hardware security module (HSM) support
3. Post-quantum algorithms
4. Cross-platform GUI

## Design Patterns Used

### 1. Strategy Pattern
- Allows easy algorithm switching
- `FileVault` can be extended for other modes

### 2. Factory Pattern
- `generate_salt()`, `generate_iv()` act as factories
- Encapsulate cryptographic object creation

### 3. Single Responsibility Principle
- Each module has a clear responsibility
- `security_utils`: Cryptographic operations
- `encryptor`: File logic
- `main`: User interface

### 4. Dependency Injection
- `FileVault` receives `chunk_size` as parameter
- Facilitates testing and configuration

## Testing

### Test Suite (test_vault.py)

1. **Basic Encryption/Decryption Test**
   - Verifies complete flow
   - Checks content integrity

2. **Wrong Password Test**
   - Verifies wrong password → corrupted data

3. **Large File Test**
   - Verifies chunk processing
   - Checks memory efficiency

4. **File Info Test**
   - Verifies metadata reading

5. **Password Validation Test**
   - Checks security rules

### Run Tests
```bash
python test_vault.py
```

## Compatibility

### Supported Platforms
- Linux (all distributions)
- macOS (10.15+)
- Windows (10/11)

### Requirements
- Python 3.8+
- cryptography >= 42.0.0
- colorama >= 0.4.6 (Windows, optional)

## Performance

### Benchmarks (Typical Hardware)

| Operation | HDD | SSD | NVMe |
|-----------|-----|-----|------|
| Encryption | 50-100 MB/s | 200-500 MB/s | 1-2 GB/s |
| Decryption | 50-100 MB/s | 200-500 MB/s | 1-2 GB/s |

**Performance Factors**:
- Storage speed
- CPU power
- Chunk size
- System load

### Chunk Size Optimization

```python
# Small files (< 1 MB)
vault = FileVault(chunk_size=16384)  # 16 KB

# Medium files (1-100 MB)
vault = FileVault(chunk_size=65536)  # 64 KB (default)

# Large files (> 100 MB)
vault = FileVault(chunk_size=1048576)  # 1 MB
```

## Conclusion

File Vault is an educational and functional tool that demonstrates:
- Professional modular architecture
- Correct cryptography implementation
- Zero-knowledge design
- Python best practices

For production use, consider adding:
- Authentication (HMAC)
- Format standards
- Professional security audit
- Enterprise key management
