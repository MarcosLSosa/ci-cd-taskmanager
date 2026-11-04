import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import pytest
from app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True

    with app.test_client() as client:
        yield client


def test_home_page(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"TaskManager" in response.data


def test_health_endpoint(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json["status"] == "healthy"


def test_add_task(client):
    response = client.post(
        "/add",
        data={"title": "Nueva tarea"},
        follow_redirects=True
    )

    assert response.status_code == 200
    assert b"Nueva tarea" in response.data
