from fastapi.testclient import TestClient
from app.main import app


client = TestClient(app)


def test_health():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
        "service": "clasificador-commits"
    }


def test_clasificar_con_motor_eco():
    response = client.post(
        "/clasificar",
        json={
            "texto": "Upgrade project dependencies",
            "motor": "eco"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["texto"] == "Upgrade project dependencies"
    assert data["motor"] == "eco"
    assert data["resultado"] == "chore"
