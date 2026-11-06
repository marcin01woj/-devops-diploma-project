from app.main import app


def test_home_page():
    client = app.test_client()
    response = client.get("/")

    assert response.status_code == 200
    assert b"Moja pierwsza aplikacja DevOps!" in response.data


def test_health_endpoint():
    client = app.test_client()
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json == {"status": "healthy"}


def test_metrics_endpoint():
    client = app.test_client()
    response = client.get("/metrics")

    assert response.status_code == 200
    assert b"app_requests_total" in response.data
    assert b"app_http_responses_total" in response.data