from core.pattern_loader import load_task_patterns

def test_task_patterns_load_keywords():
    task_patterns = load_task_patterns()
    keywords = task_patterns.main_keywords
    assert "pendente" in keywords
    assert "temos de" in keywords


def test_task_patterns_load_prefixes():
    task_patterns = load_task_patterns()
    prefixes = task_patterns.prefixes
    assert "tenho um pendente para" in prefixes
    assert "temos de" in prefixes
