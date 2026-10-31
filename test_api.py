from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def ask(question):
    return client.post("/query", json={"question": question})


def test_normal_question():
    response = ask("how to enable CORS in FastAPI")
    data = response.json()
    assert response.status_code == 200
    assert len(data["sources_used"]) > 0
    assert any("cors" in url for url in data["sources_used"])


def test_trap_question():
    response = ask("how to use Celery with FastAPI")
    data = response.json()
    assert response.status_code == 200
    assert data["sources_used"] == []


def test_off_topic_question():
    response = ask("how to bake a cake")
    data = response.json()
    assert response.status_code == 200
    assert data["sources_used"] == []
    assert "not available" in data["answer"]


def test_empty_question():
    response = ask("")
    data = response.json()
    assert response.status_code == 200
    assert data["sources_used"] == []


def test_missing_field():
    response = client.post("/query", json={})
    assert response.status_code == 422