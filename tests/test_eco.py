from app.motores.eco import clasificar


def test_clasificar_fix():
    assert clasificar("Fix login bug") == "fix"


def test_clasificar_feat():
    assert clasificar("Add user registration") == "feat"


def test_clasificar_docs():
    assert clasificar("Update README documentation") == "docs"


def test_clasificar_refactor():
    assert clasificar("Refactor authentication service") == "refactor"


def test_clasificar_test():
    assert clasificar("Create unit tests for the login service") == "test"


def test_clasificar_chore():
    assert clasificar("Upgrade project dependencies") == "chore"


def test_clasificar_por_defecto():
    assert clasificar("Update internal project files") == "chore"
