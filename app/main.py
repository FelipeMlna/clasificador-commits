import time

from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel

from app.db import obtener_conexion
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

    inicio = time.perf_counter()

    if request.motor == "eco":
        resultado = clasificar_eco(request.texto)

    elif request.motor == "ollama":
        try:
            resultado = await clasificar_ollama(request.texto)

        except (ConnectionError, ValueError) as error:
            raise HTTPException(
                status_code=502,
                detail=str(error)
            )

    else:
        raise HTTPException(
            status_code=400,
            detail=f"Motor no soportado: {request.motor}"
        )

    latencia_ms = round(
        (time.perf_counter() - inicio) * 1000
    )

    try:
        conexion = obtener_conexion()

        with conexion:
            with conexion.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO inferencias (
                        texto,
                        motor,
                        resultado,
                        latencia_ms
                    )
                    VALUES (%s, %s, %s, %s)
                    """,
                    (
                        request.texto,
                        request.motor,
                        resultado,
                        latencia_ms
                    )
                )

        conexion.close()

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Error al guardar la inferencia: {error}"
        )

    return {
        "texto": request.texto,
        "motor": request.motor,
        "resultado": resultado,
        "latencia_ms": latencia_ms
    }


@app.get("/inferencias")
def obtener_inferencias(
    limite: int = Query(default=10, ge=1, le=100)
):
    try:
        conexion = obtener_conexion()

        with conexion:
            with conexion.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT
                        id,
                        texto,
                        motor,
                        resultado,
                        latencia_ms,
                        creado_en
                    FROM inferencias
                    ORDER BY creado_en DESC
                    LIMIT %s
                    """,
                    (limite,)
                )

                columnas = [
                    descripcion[0]
                    for descripcion in cursor.description
                ]

                resultados = [
                    dict(zip(columnas, fila))
                    for fila in cursor.fetchall()
                ]

        conexion.close()

        return resultados

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Error al consultar las inferencias: {error}"
        )
