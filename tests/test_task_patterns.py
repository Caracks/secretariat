import pytest

from core.pattern_loader import TaskField, clear_patterns_cache, get_task_field


@pytest.fixture(autouse=True)
def setup_and_teardown():
    """Garante que o cache seja limpo antes de cada teste rodar."""
    clear_patterns_cache()
    yield
    clear_patterns_cache()


def test_task_patterns_load_keywords():
    keywords = get_task_field(TaskField.main_keywords)

    assert isinstance(keywords, list), "O retorno deve ser uma lista"
    assert "pendente" in keywords
    assert "temos de" in keywords


def test_task_patterns_load_prefixes():
    prefixes = get_task_field(TaskField.prefixes)

    assert isinstance(prefixes, list), "O retorno deve ser uma lista"
    assert "tenho um pendente para" in prefixes
    assert "temos de" in prefixes


def test_task_patterns_load_non_existent_field():
    reject_keywords = get_task_field(TaskField.reject_keywords)

    assert isinstance(reject_keywords, list), "O retorno deve ser uma lista"
    assert "não" in reject_keywords
    assert "nop" in reject_keywords