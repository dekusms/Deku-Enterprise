"""Password Security Test."""

from security.password import hash_password, verify_password, validate_password


def test_hash_password():
    password = "securepassword123"
    hashed = hash_password(password)
    assert hashed != password
    assert len(hashed) > 0


def test_verify_password():
    password = "securepassword123"
    hashed = hash_password(password)
    assert verify_password(password, hashed)
    assert not verify_password("wrongpassword", hashed)


def test_validate_password_min_length():
    policy = {"min_length": 8}
    err, message = validate_password("short", policy)
    assert err
    assert "at least 8 characters" in message


def test_validate_password_min_uppercase():
    policy = {"min_uppercase": 1}
    err, message = validate_password("lowercase", policy)
    assert err
    assert "at least 1 uppercase letter" in message


def test_validate_password_min_numbers():
    policy = {"min_numbers": 1}
    err, message = validate_password("NoNumbers", policy)
    assert err
    assert "at least 1 number" in message


def test_validate_password_min_special_characters():
    policy = {"min_special": 1, "allowed_specials": "!@#$%^&*"}
    err, message = validate_password("NoSpecials", policy)
    assert err
    assert "at least 1 special character" in message


def test_validate_password_entropy():
    policy = {"min_entropy": 3.0}
    err, message = validate_password("weak", policy)
    assert err
    assert "too weak" in message


def test_validate_password_pwned():
    policy = {"check_pwned": True}
    err, message = validate_password("password123", policy)
    assert err
    assert "data breaches" in message
