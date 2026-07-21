from tools.task_tool import normalize_task_text


def test_normalize_task_text():
    result = normalize_task_text(
        "Tenho um pendente para comprar arroz"
    )

    assert result == "comprar arroz" 