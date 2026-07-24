from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, MagicMock, patch

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


def test_clasificar_con_motor_ollama():
    respuesta_ollama = {
        "response": "fix"
    }

    mock_response = MagicMock()
    mock_response.json.return_value = respuesta_ollama
    mock_response.raise_for_status.return_value = None

    with patch(
        "app.main.httpx.AsyncClient.post",
        new_callable=AsyncMock,
        return_value=mock_response
    ):
        response = client.post(
            "/clasificar",
            json={
                "texto": "Fix login bug",
                "motor": "ollama"
            }
        )

    assert response.status_code == 200

    data = response.json()

    assert data["texto"] == "Fix login bug"
    assert data["motor"] == "ollama"
    assert data["resultado"] == "fix"
