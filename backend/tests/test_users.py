from app.core.security import (
    hash_password,
    verify_password,
)
def test_hash_password():

    password = "Password123"

    hashed = hash_password(password)

    assert hashed != password

    assert verify_password(password, hashed)

def test_wrong_hash():

    password = "Password123"

    hashed = hash_password(password)

    assert not verify_password(
        "WrongPassword",
        hashed,
    )