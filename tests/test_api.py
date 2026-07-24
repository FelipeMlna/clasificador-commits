from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, MagicMock, patch

from app.main import app


client = TestClient(app)


def crear_mock_conexion():
    conexion = MagicMock()
    cursor = MagicMock()

    conexion.cursor.return_value.__enter__.return_value = cursor
    conexion.__enter__.return_value = conexion

    return conexion


def test_health():
    response = client.get("/health")

    assert response.status_code == 200

    assert response.json() == {
        "status": "ok",
        "service": "clasificador-commits"
    }


def test_clasificar_con_motor_eco():
    mock_conexion = crear_mock_conexion()

    with patch(
        "app.main.obtener_conexion",
        return_value=mock_conexion
    ):
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
    assert data["latencia_ms"] >= 0


def test_clasificar_con_motor_ollama():
    respuesta_ollama = {
        "response": "fix"
    }

    mock_response = MagicMock()
    mock_response.json.return_value = respuesta_ollama
    mock_response.raise_for_status.return_value = None

    mock_conexion = crear_mock_conexion()

    with patch(
        "app.motores.ollama.httpx.AsyncClient.post",
        new_callable=AsyncMock,
        return_value=mock_response
    ), patch(
        "app.main.obtener_conexion",
        return_value=mock_conexion
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
    assert data["latencia_ms"] >= 0


def test_clasificar_motor_invalido():
    response = client.post(
        "/clasificar",
        json={
            "texto": "Something",
            "motor": "inexistente"
        }
    )

    assert response.status_code == 400
