from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import httpx

app = FastAPI(
    title="Clasificador de Commits",
    description="API para clasificar mensajes de commit usando IA local",
    version="1.0.0"
)

OLLAMA_URL = "http://host.docker.internal:11434"


class CommitRequest(BaseModel):
    texto: str
    motor: str = "ollama"


@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "service": "clasificador-commits"
    }


@app.post("/clasificar")
async def clasificar_commit(request: CommitRequest):
    prompt = f"""
Clasifica el siguiente mensaje de commit según estas categorías:

- feat: nueva funcionalidad
- fix: corrección de errores
- docs: documentación
- refactor: modificación interna del código sin cambiar funcionalidad
- test: pruebas
- chore: tareas de mantenimiento

Mensaje del commit:
"{request.texto}"

Responde únicamente con la categoría y una breve explicación.
"""

    payload = {
        "model": "qwen2.5:0.5b",
        "prompt": prompt,
        "stream": False
    }

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{OLLAMA_URL}/api/generate",
                json=payload,
                timeout=120.0
            )

        response.raise_for_status()
        resultado = response.json()

        return {
            "texto": request.texto,
            "motor": request.motor,
            "resultado": resultado.get("response", "")
        }

    except httpx.HTTPError as error:
        raise HTTPException(
            status_code=502,
            detail=f"Error comunicando con Ollama: {str(error)}"
        )
