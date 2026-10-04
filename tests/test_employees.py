def test_create_employee(client):
    response = client.post(
        "/employees/",
        json={
            "full_name": "Alice Test",
            "email": "alice@test.com",
            "department": "Engineering",
            "is_active": True,
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["full_name"] == "Alice Test"
    assert data["email"] == "alice@test.com"
    assert "id" in data


def test_create_employee_duplicate_email(client):
    client.post(
        "/employees/",
        json={
            "full_name": "Bob Test",
            "email": "bob@test.com",
            "department": "Sales",
            "is_active": True,
        },
    )
    response = client.post(
        "/employees/",
        json={
            "full_name": "Bob Clone",
            "email": "bob@test.com",
            "department": "Marketing",
            "is_active": True,
        },
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "An employee with this email already exists"


def test_read_employee_not_found(client):
    response = client.get("/employees/9999")
    assert response.status_code == 404


def test_read_employees_list(client):
    client.post(
        "/employees/",
        json={
            "full_name": "Carol Test",
            "email": "carol@test.com",
            "department": "HR",
            "is_active": True,
        },
    )
    response = client.get("/employees/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["full_name"] == "Carol Test"


def test_update_employee(client):
    create_response = client.post(
        "/employees/",
        json={
            "full_name": "Dave Test",
            "email": "dave@test.com",
            "department": "Finance",
            "is_active": True,
        },
    )
    employee_id = create_response.json()["id"]

    update_response = client.patch(
        f"/employees/{employee_id}",
        json={"department": "Operations"},
    )
    assert update_response.status_code == 200
    assert update_response.json()["department"] == "Operations"
    assert update_response.json()["full_name"] == "Dave Test"


def test_delete_employee(client):
    create_response = client.post(
        "/employees/",
        json={
            "full_name": "Eve Test",
            "email": "eve@test.com",
            "department": "Legal",
            "is_active": True,
        },
    )
    employee_id = create_response.json()["id"]

    delete_response = client.delete(f"/employees/{employee_id}")
    assert delete_response.status_code == 200

    get_response = client.get(f"/employees/{employee_id}")
    assert get_response.status_code == 404