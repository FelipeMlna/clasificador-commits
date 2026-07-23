from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import httpx
from app.motores.eco import clasificar as clasificar_eco

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
    if request.motor == "eco":
        return {
            "texto": request.texto,
            "motor": "eco",
            "resultado": clasificar_eco(request.texto)
        }
    prompt = f"""
You are a commit message classifier.

Your task is to classify the commit message into exactly ONE label.

LABELS:
- feat: adds a new user-facing feature or capability.
- fix: fixes a bug, error, defect, crash, or incorrect behavior.
- docs: changes documentation only.
- refactor: restructures or improves existing code without changing behavior.
- test: adds, modifies, or removes tests.
- chore: maintenance, dependencies, configuration, tooling, or build changes.

DECISION RULES:
1. If the commit is about tests or testing, choose test.
2. If the commit is about dependencies, packages, libraries, configuration, tooling, or build maintenance, choose chore.
3. If the commit fixes a bug or incorrect behavior, choose fix.
4. If the commit adds a new feature or capability, choose feat.
5. If the commit changes documentation only, choose docs.
6. If the commit restructures existing code without changing its behavior, choose refactor.

EXAMPLES:
"Create unit tests for the login service" = test
"Upgrade project dependencies" = chore
"Update package dependencies" = chore
"Fix login bug" = fix
"Add user registration" = feat
"Update README documentation" = docs
"Refactor authentication service" = refactor

COMMIT MESSAGE:
{request.texto}

OUTPUT:
Return exactly one label from this list:
feat, fix, docs, refactor, test, chore

Return only the label. No explanation. No punctuation.
    """

    payload = {
        "model": "qwen2.5:0.5b",
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": 0
        }
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

        respuesta = resultado.get("response", "").strip().lower()

        categorias_validas = {
            "feat",
            "fix",
            "docs",
            "refactor",
            "test",
            "chore"
        }

        if respuesta not in categorias_validas:
            raise HTTPException(
                status_code=502,
                detail=f"Ollama devolvió una categoría inválida: {respuesta}"
            )

        return {
            "texto": request.texto,
            "motor": request.motor,
            "resultado": respuesta
        }

    except httpx.HTTPError as error:
        raise HTTPException(
            status_code=502,
            detail=f"Error comunicando con Ollama: {str(error)}"
        )
