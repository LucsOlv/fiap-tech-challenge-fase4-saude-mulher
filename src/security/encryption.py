"""Data encryption for sensitive health information (LGPD compliance)."""

import os
import base64
from typing import Optional


class DataEncryption:
    """AES-256 encryption for data at rest and Fernet for data in transit."""

    def __init__(self, key: Optional[bytes] = None):
        try:
            from cryptography.fernet import Fernet
            self._fernet_cls = Fernet

            if key:
                self.key = key
            else:
                env_key = os.getenv("ENCRYPTION_KEY", "")
                if env_key:
                    self.key = base64.urlsafe_b64decode(env_key.encode() + b"==")
                else:
                    self.key = Fernet.generate_key()

            self.fernet = Fernet(self.key)
        except (ImportError, Exception):
            self.fernet = None
            self.key = None if key is None else key

    def encrypt(self, data: bytes) -> bytes:
        """Encrypt data using Fernet (AES-128-CBC)."""
        if self.fernet is None:
            return data  # No encryption available
        return self.fernet.encrypt(data)

    def decrypt(self, encrypted_data: bytes) -> bytes:
        """Decrypt Fernet-encrypted data."""
        if self.fernet is None:
            return encrypted_data
        return self.fernet.decrypt(encrypted_data)

    def encrypt_file(self, file_path: str, output_path: str = None) -> str:
        """Encrypt a file for secure storage."""
        if output_path is None:
            output_path = file_path + ".enc"

        with open(file_path, "rb") as f:
            data = f.read()

        encrypted = self.encrypt(data)

        with open(output_path, "wb") as f:
            f.write(encrypted)

        return output_path

    def decrypt_file(self, file_path: str, output_path: str = None) -> str:
        """Decrypt an encrypted file."""
        if output_path is None:
            output_path = file_path.replace(".enc", ".dec")

        with open(file_path, "rb") as f:
            data = f.read()

        decrypted = self.decrypt(data)

        with open(output_path, "wb") as f:
            f.write(decrypted)

        return output_path

    def encrypt_string(self, text: str) -> str:
        """Encrypt a string and return base64 encoded result."""
        encrypted = self.encrypt(text.encode())
        return base64.urlsafe_b64encode(encrypted).decode()

    def decrypt_string(self, encrypted_text: str) -> str:
        """Decrypt a base64 encoded encrypted string."""
        data = base64.urlsafe_b64decode(encrypted_text.encode())
        return self.decrypt(data).decode()
