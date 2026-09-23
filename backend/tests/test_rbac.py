def _register(client, email):
    response = client.post(
        "/api/auth/register",
        json={"email": email, "full_name": email.split("@")[0], "password": "StrongPass123!"},
    )
    assert response.status_code == 201
    return response.json()["data"]["access_token"]


def test_admin_can_list_users(client):
    admin_token = _register(client, "admin@example.com")
    _register(client, "employee@example.com")

    response = client.get("/api/users", headers={"Authorization": f"Bearer {admin_token}"})
    assert response.status_code == 200
    assert len(response.json()["data"]) == 2


def test_employee_cannot_list_users(client):
    _register(client, "admin@example.com")
    employee_token = _register(client, "employee@example.com")

    response = client.get("/api/users", headers={"Authorization": f"Bearer {employee_token}"})
    assert response.status_code == 403
    assert response.json()["error"]["code"] == "FORBIDDEN"

