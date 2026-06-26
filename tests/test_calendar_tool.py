
from tools.calendar_tool import parse_event_candidate


def test_parse_event_with_day_and_time():
    result = parse_event_candidate("bora jantar dia 7 às 20h")

    assert result["is_event"] is True
    assert result["title"] == "jantar"
    assert result["date_text"] == "dia 7"
    assert result["time_text"] == "às 20h"
    assert result["confidence"] == "high"


def test_parse_event_with_weekday():
    result = parse_event_candidate("bora jantar na quinta")

    assert result["is_event"] is True
    assert result["title"] == "jantar"
    assert result["date_text"] == "quinta"
    assert result["confidence"] == "medium"


def test_parse_non_event():
    result = parse_event_candidate("comprar arroz")

    assert result["is_event"] is False
    assert result["confidence"] == "low"