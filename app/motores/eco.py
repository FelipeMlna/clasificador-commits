def clasificar(texto: str) -> str:
    texto = texto.lower()

    # Pruebas
    if any(palabra in texto for palabra in [
        "test",
        "tests",
        "testing",
        "unit test",
        "unit tests",
        "prueba",
        "pruebas"
    ]):
        return "test"

    # Mantenimiento, dependencias y configuración
    if any(palabra in texto for palabra in [
        "dependency",
        "dependencies",
        "dependencia",
        "dependencias",
        "package",
        "packages",
        "library",
        "libraries",
        "configuration",
        "configuración",
        "config",
        "tooling",
        "build"
    ]):
        return "chore"

    # Corrección de errores
    if any(palabra in texto for palabra in [
        "bug",
        "error",
        "fix",
        "broken",
        "crash",
        "issue"
    ]):
        return "fix"

    # Documentación
    if any(palabra in texto for palabra in [
        "readme",
        "documentation",
        "documentación",
        "docs"
    ]):
        return "docs"

    # Refactorización
    if any(palabra in texto for palabra in [
        "refactor",
        "restructure",
        "reorganize",
        "reorganizar"
    ]):
        return "refactor"

    # Nueva funcionalidad
    if any(palabra in texto for palabra in [
        "add",
        "create",
        "implement",
        "feature",
        "new"
    ]):
        return "feat"

    return "chore"
