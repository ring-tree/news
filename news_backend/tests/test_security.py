from utils.security import get_hash_password, verify_password


def test_password_hash_roundtrip():
    hashed = get_hash_password("test-password-123")
    assert hashed.startswith("$2b$")
    assert verify_password("test-password-123", hashed)


def test_password_hash_rejects_wrong_password():
    hashed = get_hash_password("correct-password")
    assert not verify_password("wrong-password", hashed)


def test_password_hash_handles_invalid_hash():
    assert not verify_password("any-password", "not-a-bcrypt-hash")
