# File Vault

A professional-grade, zero-knowledge file encryption tool using AES-256-CFB with PBKDF2 key derivation.

## Features

- **Strong Encryption**: AES-256 in CFB mode
- **Secure Key Derivation**: PBKDF2-HMAC-SHA256 with 100,000 iterations
- **Zero-Knowledge Architecture**: Passwords never stored
- **Memory Efficient**: Chunk-based processing for large files
- **Cross-Platform**: Works on Windows, Linux, and macOS
- **User-Friendly CLI**: Simple command-line interface

## Security Specifications

| Feature | Specification |
|---------|--------------|
| Encryption Algorithm | AES-256-CFB |
| Key Derivation | PBKDF2-HMAC-SHA256 |
| KDF Iterations | 100,000 |
| Salt Size | 16 bytes (128 bits) |
| IV Size | 16 bytes (128 bits) |
| Key Size | 32 bytes (256 bits) |

## Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Install Dependencies

```bash
pip install -r requirements.txt
```

## Usage

### Encrypt a File

```bash
python main.py encrypt document.pdf
```

This will create `document.pdf.encrypted` in the same directory.

### Decrypt a File

```bash
python main.py decrypt document.pdf.encrypted
```

This will restore the original `document.pdf`.

### Custom Output Path

```bash
python main.py encrypt document.pdf -o /secure/location/encrypted.bin
python main.py decrypt encrypted.bin -o /restore/document.pdf
```

### Delete Original After Encryption/Decryption

```bash
python main.py encrypt document.pdf --delete-original
python main.py decrypt document.pdf.encrypted --delete-original
```

### View File Information

```bash
python main.py info document.pdf.encrypted
```

### Advanced Options

```bash
# Custom chunk size (default: 64KB)
python main.py encrypt largefile.iso -c 1048576  # 1MB chunks

# Skip password strength warnings
python main.py encrypt document.pdf --force
```

## File Format

Encrypted files use the following structure:

```
[16 bytes: Salt][16 bytes: IV][Remaining bytes: Encrypted Data]
```

- **Salt**: Random 16-byte value for key derivation
- **IV**: Random 16-byte initialization vector
- **Encrypted Data**: AES-256-CFB encrypted file contents

## Security Considerations

### What This Tool Provides

- **Confidentiality**: Strong AES-256 encryption
- **Unique Encryption**: Each encryption uses new salt and IV
- **Password Protection**: PBKDF2 with high iteration count
- **Memory Safety**: Chunk-based processing prevents memory overflow

### Important Limitations

1. **No Integrity Checking**: CFB mode doesn't provide authentication
   - An attacker could modify encrypted data without detection
   - Consider adding HMAC for production use

2. **Password is Everything**: 
   - No password recovery mechanism
   - Lost password = permanent data loss
   - Use a strong, memorable password

3. **Not Post-Quantum Secure**: 
   - AES-256 is considered quantum-resistant
   - PBKDF2 parameters may need adjustment in the future

4. **No Key Escrow**: 
   - True zero-knowledge design
   - No backdoors or master keys

### Best Practices

1. **Use Strong Passwords**:
   - Minimum 12 characters
   - Mix of uppercase, lowercase, numbers, and symbols
   - Avoid dictionary words and personal information

2. **Secure Password Management**:
   - Use a password manager
   - Never share passwords over insecure channels
   - Change passwords if compromise is suspected

3. **Backup Important Data**:
   - Keep unencrypted backups in secure locations
   - Test decryption before deleting originals
   - Document your encryption strategy

4. **Verify Integrity**:
   - Use checksums (MD5, SHA256) for important files
   - Verify file size after encryption/decryption
   - Test decryption immediately after encryption

## Architecture

```
file_vault/
├── core/
│   ├── __init__.py          # Package initialization
│   ├── security_utils.py    # Cryptographic utilities
│   └── encryptor.py         # Main encryption engine
├── main.py                  # CLI interface
└── requirements.txt         # Python dependencies
```

### Module Overview

- **security_utils.py**: Key derivation, salt/IV generation, validation
- **encryptor.py**: `FileVault` class with encrypt/decrypt methods
- **main.py**: Command-line interface using argparse

## Examples

### Example 1: Encrypting a Sensitive Document

```bash
$ python main.py encrypt confidential.docx
ℹ File size: 245.50 KB
ℹ Enter a strong password for encryption
Password: ****************
Confirm password: ****************
ℹ Encrypting file...
✓ File encrypted successfully!
ℹ Output file: confidential.docx.encrypted
ℹ Output size: 245.53 KB
```

### Example 2: Decrypting with Custom Output

```bash
$ python main.py decrypt confidential.docx.encrypted -o restored.docx
ℹ File size: 245.53 KB
Password: ****************
ℹ Decrypting file...
✓ File decrypted successfully!
ℹ Output file: restored.docx
ℹ Output size: 245.50 KB
```

### Example 3: File Information

```bash
$ python main.py info confidential.docx.encrypted

File Information:
  Path: confidential.docx.encrypted
  Total Size: 245.53 KB
  ✓ Appears to be encrypted
  Encrypted Data: 245.50 KB
  ✓ Valid encryption header
```

## Troubleshooting

### "Decryption failed" Error

**Possible causes**:
- Incorrect password
- Corrupted file
- File was not encrypted with this tool
- File was modified after encryption

**Solutions**:
- Double-check your password
- Try re-encrypting the original file
- Verify file integrity with checksums

### "Permission denied" Error

**Causes**:
- Insufficient file system permissions
- File is in use by another program
- Antivirus blocking access

**Solutions**:
- Run with appropriate permissions
- Close programs using the file
- Add exception in antivirus software

### Memory Issues with Large Files

**Solution**:
Increase chunk size for better performance:

```bash
python main.py encrypt large_file.iso -c 1048576  # 1MB chunks
```

## Performance

Performance depends on:
- File size
- Storage speed (SSD vs HDD)
- CPU capabilities
- Chunk size configuration

Typical performance on modern hardware:
- ~50-100 MB/s on HDD
- ~200-500 MB/s on SSD
- ~1-2 GB/s on NVMe SSD

## Contributing

This is a demonstration project. For production use:
1. Add HMAC for authentication
2. Implement secure key storage options
3. Add comprehensive error recovery
4. Include automated testing suite
5. Perform security audit

## License

MIT License - See LICENSE file for details

## Disclaimer

This tool is provided for educational and personal use. For production environments:
- Conduct thorough security audits
- Follow your organization's security policies
- Consider using established encryption solutions
- Implement proper key management

**The authors are not responsible for data loss or security breaches resulting from improper use of this tool.**

## Support

For issues, questions, or contributions:
- Open an issue on GitHub
- Read the documentation
- Review security considerations

---

**Remember**: Strong encryption is only as good as your password. Choose wisely!
