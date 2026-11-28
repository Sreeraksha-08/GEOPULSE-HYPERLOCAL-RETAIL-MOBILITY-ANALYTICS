from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_all_stores():
    response = client.get("/stores")
    assert response.status_code == 200
    assert response.json()["count"] == 16


def test_existing_stores():
    response = client.get("/stores?store_type=existing")
    assert response.status_code == 200
    assert response.json()["count"] == 12


def test_candidate_stores():
    response = client.get("/stores?store_type=candidate")
    assert response.status_code == 200
    assert response.json()["count"] == 4


def test_zones():
    response = client.get("/zones")
    assert response.status_code == 200
    assert response.json()["count"] == 25


def test_footfall():
    response = client.get("/footfall")
    assert response.status_code == 200
    assert response.json()["records"] == 336000
    assert response.json()["unique_devices"] == 1000


def test_zone_filter():
    response = client.get("/footfall?zone_id=BENG-Z01")
    assert response.status_code == 200
    assert response.json()["filters"]["zone_id"] == "BENG-Z01"


def test_activity_filter():
    response = client.get("/footfall?activity=lunch_visit")
    assert response.status_code == 200
    assert response.json()["activity_counts"]["lunch_visit"] == 20000


def test_invalid_footfall_filter():
    response = client.get("/footfall?zone_id=INVALID-ZONE")
    assert response.status_code == 404


def test_invalid_store_type():
    response = client.get("/stores?store_type=unknown")
    assert response.status_code == 422


def test_invalid_activity():
    response = client.get("/footfall?activity=unknown")
    assert response.status_code == 422
