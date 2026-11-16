def test_predict_success(client, apartment_data):
    response = client.post(
        "/pred/",
        json=apartment_data,
    )

    assert response.status_code == 200


def test_predict_empty_body(client):
    response = client.post("/pred/")

    assert response.status_code == 400


def test_predict_invalid_area(client, apartment_data):
    apartment_data["area"] = -10

    response = client.post(
        "/pred/",
        json=apartment_data,
    )

    assert response.status_code == 422


def test_predict_missing_field(client, apartment_data):
    apartment_data.pop("area")

    response = client.post(
        "/pred/",
        json=apartment_data,
    )

    assert response.status_code == 422


def test_health(client):
    response = client.get("/health")

    assert response.status_code == 200


def test_ready(client):
    response = client.get("/ready")

    assert response.status_code == 200
