import uuid

EMAIL = f"test_{uuid.uuid4().hex}@gmail.com"
PASSWORD = "Password123!"

def test_signup(test_client):

    response = test_client.post(
        "/api/v1/auth/signup",
        json={
            "email": EMAIL,
            "password": PASSWORD,
            "account_type": "DONOR",
            "name": "Test User",
            "phone": "9876543210",
            "locality": "Chennai",
            "pincode": "600001",
            "lat": 13.08,
            "lng": 80.27,
        },
    )

    assert response.status_code == 201

    assert response.json()["message"] == "User created successfully."

def test_duplicate_signup(test_client):

    response = test_client.post(
        "/api/v1/auth/signup",
        json={
            "email": EMAIL,
            "password": PASSWORD,
            "account_type": "DONOR",
            "name": "Test User",
            "phone": "9876543210",
            "locality": "Chennai",
            "pincode": "600001",
        },
    )

    assert response.status_code == 409

def test_login(test_client):

    response = test_client.post(
        "/api/v1/auth/login",
        json={
            "email": EMAIL,
            "password": PASSWORD,
        },
    )

    assert response.status_code == 200

    body = response.json()

    assert "access_token" in body

    assert body["token_type"] == "bearer"

def test_wrong_password(test_client):

    response = test_client.post(
        "/api/v1/auth/login",
        json={
            "email": EMAIL,
            "password": "WrongPassword",
        },
    )

    assert response.status_code == 401

def test_refresh(test_client):

    login = test_client.post(
        "/api/v1/auth/login",
        json={
            "email": EMAIL,
            "password": PASSWORD,
        },
    )

    response = test_client.post(
        "/api/v1/auth/refresh",
    )

    assert response.status_code == 200

    assert "access_token" in response.json()

def test_logout(test_client):

    response = test_client.post(
        "/api/v1/auth/logout"
    )

    assert response.status_code == 200

    assert response.json()["message"] == "Logged out successfully."

def test_me(test_client):

    login = test_client.post(
        "/api/v1/auth/login",
        json={
            "email": EMAIL,
            "password": PASSWORD,
        },
    )

    token = login.json()["access_token"]

    response = test_client.get(
        "/api/v1/auth/me",
        headers={
            "Authorization": f"Bearer {token}"
        },
    )

    assert response.status_code == 200

def test_change_password(test_client):

    login = test_client.post(
        "/api/v1/auth/login",
        json={
            "email": EMAIL,
            "password": PASSWORD,
        },
    )

    token = login.json()["access_token"]

    response = test_client.post(
        "/api/v1/auth/change-password",
        headers={
            "Authorization": f"Bearer {token}"
        },
        json={
            "current_password": PASSWORD,
            "new_password": "NewPassword123",
        },
    )

    assert response.status_code == 200