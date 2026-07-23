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
Eres un clasificador de mensajes de commits.

Debes elegir EXACTAMENTE una de estas categorías:

feat = nueva funcionalidad
fix = corrección de un error o bug
docs = documentación
refactor = reorganización o mejora interna del código sin cambiar su comportamiento
test = pruebas
chore = mantenimiento, configuración o dependencias

REGLAS IMPORTANTES:
- Si el mensaje corrige un error, usa fix.
- Si el mensaje agrega o modifica documentación, usa docs.
- Si el mensaje reorganiza o mejora código existente sin agregar funcionalidad, usa refactor.
- Si el mensaje agrega una funcionalidad nueva, usa feat.
- Si el mensaje crea o modifica pruebas, usa test.
- Si el mensaje actualiza dependencias o configuración, usa chore.

EJEMPLOS:
"corrige error en el inicio de sesión" -> fix
"agrega la documentación del proyecto" -> docs
"refactoriza el servicio de usuarios" -> refactor
"agrega autenticación con Google" -> feat
"crea pruebas unitarias para el login" -> test
"actualiza las dependencias del proyecto" -> chore

MENSAJE A CLASIFICAR:
"{request.texto}"

RESPONDE ÚNICAMENTE CON UNA DE ESTAS PALABRAS:

feat
fix
docs
refactor
test
chore

No escribas explicaciones.
No escribas frases adicionales.
No escribas "CATEGORIA:".
Responde solamente con una palabra.
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
