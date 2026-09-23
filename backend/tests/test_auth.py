def test_register_login_and_me(client):
    register_response = client.post(
        "/api/auth/register",
        json={
            "email": "new.admin@example.com",
            "full_name": "New Admin",
            "password": "StrongPass123!",
        },
    )
    assert register_response.status_code == 201
    register_data = register_response.json()["data"]
    assert register_data["user"]["role"]["name"] == "ADMIN"

    login_response = client.post(
        "/api/auth/login",
        json={"email": "new.admin@example.com", "password": "StrongPass123!"},
    )
    assert login_response.status_code == 200
    token = login_response.json()["data"]["access_token"]

    me_response = client.get("/api/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert me_response.status_code == 200
    assert me_response.json()["data"]["email"] == "new.admin@example.com"


def test_duplicate_email_is_rejected(client):
    payload = {
        "email": "person@example.com",
        "full_name": "Person Example",
        "password": "StrongPass123!",
    }
    assert client.post("/api/auth/register", json=payload).status_code == 201
    duplicate = client.post("/api/auth/register", json=payload)
    assert duplicate.status_code == 409
    assert duplicate.json()["error"]["code"] == "EMAIL_ALREADY_REGISTERED"

