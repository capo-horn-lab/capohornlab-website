"""Regression coverage for the embedded Research detail dataset."""
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_research_detail_dataset_is_strict_json_and_terminated() -> None:
    source = (ROOT / "research-detail.html").read_text(encoding="utf-8")
    marker = "var researchData = "
    start = source.index(marker) + len(marker)
    array_start = source.index("[", start)
    in_string = False
    escaped = False
    depth = 0
    array_end = None
    for index in range(array_start, len(source)):
        char = source[index]
        if in_string:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                in_string = False
            continue
        if char == '"':
            in_string = True
        elif char == "[":
            depth += 1
        elif char == "]":
            depth -= 1
            if depth == 0:
                array_end = index + 1
                break
    assert array_end is not None
    parsed = json.loads(source[start:array_end])
    assert len(parsed) == 14
    assert parsed[-1]["slug"] == "news-longhorizon-es"
