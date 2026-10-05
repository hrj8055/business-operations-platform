def test_register_user(client):
    response = client.post(
        "/register",
        json={"username": "alice", "password": "AlicePass123"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "alice"
    assert data["is_active"] is True
    assert "password" not in data
    assert "hashed_password" not in data


def test_register_duplicate_username(client):
    client.post("/register", json={"username": "bob", "password": "BobPass123"})
    response = client.post("/register", json={"username": "bob", "password": "Different123"})
    assert response.status_code == 400
    assert response.json()["detail"] == "Username already registered"


def test_login_success(client):
    client.post("/register", json={"username": "carol", "password": "CarolPass123"})
    response = client.post(
        "/login",
        data={"username": "carol", "password": "CarolPass123"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_wrong_password(client):
    client.post("/register", json={"username": "dave", "password": "DavePass123"})
    response = client.post(
        "/login",
        data={"username": "dave", "password": "WrongPassword"},
    )
    assert response.status_code == 401


def test_login_nonexistent_user(client):
    response = client.post(
        "/login",
        data={"username": "ghost", "password": "Whatever123"},
    )
    assert response.status_code == 401


def test_create_employee_without_token(client):
    response = client.post(
        "/employees/",
        json={
            "full_name": "No Auth",
            "email": "noauth@test.com",
            "department": "Engineering",
            "is_active": True,
        },
    )
    assert response.status_code == 401


def test_create_employee_with_token(client, auth_headers):
    response = client.post(
        "/employees/",
        json={
            "full_name": "With Auth",
            "email": "withauth@test.com",
            "department": "Engineering",
            "is_active": True,
        },
        headers=auth_headers,
    )
    assert response.status_code == 200
    assert response.json()["full_name"] == "With Auth"
