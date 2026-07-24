from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from app.motores.eco import clasificar as clasificar_eco
from app.motores.ollama import clasificar as clasificar_ollama


app = FastAPI(
    title="Clasificador de Commits",
    description="API para clasificar mensajes de commit usando IA local",
    version="1.0.0"
)


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

    if request.motor == "eco":
        resultado = clasificar_eco(request.texto)

        return {
            "texto": request.texto,
            "motor": "eco",
            "resultado": resultado
        }

    if request.motor == "ollama":
        try:
            resultado = await clasificar_ollama(request.texto)

            return {
                "texto": request.texto,
                "motor": "ollama",
                "resultado": resultado
            }

        except (ConnectionError, ValueError) as error:
            raise HTTPException(
                status_code=502,
                detail=str(error)
            )

    raise HTTPException(
        status_code=400,
        detail=f"Motor no soportado: {request.motor}"
    )
