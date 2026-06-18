from core.pattern_loader import load_task_keywords, load_task_prefixes

def test_task_patterns_load_keywords():
    keywords = load_task_keywords()
    assert "pendente" in keywords
    assert "temos de" in keywords


def test_task_patterns_load_prefixes():
    prefixes = load_task_prefixes()
    assert "tenho um pendente para" in prefixes
    assert "temos de" in prefixes
