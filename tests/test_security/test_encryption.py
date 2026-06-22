"""Tests for encryption module."""

from src.security.encryption import DataEncryption


class TestDataEncryption:
    """Test DataEncryption class."""

    def test_init_generates_key(self):
        de = DataEncryption()
        assert de.key is not None

    def test_encrypt_decrypt_string(self):
        de = DataEncryption()
        original = "dados sensíveis do paciente"
        encrypted = de.encrypt_string(original)
        decrypted = de.decrypt_string(encrypted)
        assert decrypted == original
        assert encrypted != original

    def test_encrypt_decrypt_bytes(self):
        de = DataEncryption()
        original = b"sensitive patient data"
        encrypted = de.encrypt(original)
        decrypted = de.decrypt(encrypted)
        assert decrypted == original

    def test_encrypt_file(self):
        import tempfile
        from pathlib import Path

        de = DataEncryption()
        with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
            f.write("test data for encryption")
            path = f.name

        enc_path = de.encrypt_file(path)
        assert Path(enc_path).exists()

        dec_path = de.encrypt_file(enc_path)  # Just to verify it exists
        Path(path).unlink()
        Path(enc_path).unlink()
