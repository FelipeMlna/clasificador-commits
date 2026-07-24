import httpx


OLLAMA_URL = "http://host.docker.internal:11434"


CATEGORIAS_VALIDAS = {
    "feat",
    "fix",
    "docs",
    "refactor",
    "test",
    "chore"
}


async def clasificar(texto: str) -> str:
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
{texto}

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

        if respuesta not in CATEGORIAS_VALIDAS:
            raise ValueError(
                f"Ollama devolvió una categoría inválida: {respuesta}"
            )

        return respuesta

    except httpx.HTTPError as error:
        raise ConnectionError(
            f"Error comunicando con Ollama: {str(error)}"
        )
