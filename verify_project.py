from __future__ import annotations

import json
from pathlib import Path


PROJECT_DIR = Path(__file__).resolve().parent
QUESTIONS_JS = PROJECT_DIR / "questions.js"
INDEX_HTML = PROJECT_DIR / "index.html"
APP_JS = PROJECT_DIR / "app.js"
STYLE_CSS = PROJECT_DIR / "style.css"


REQUIRED_SCREEN_IDS = [
    "screen-home",
    "screen-pre",
    "screen-question",
    "screen-results",
    "screen-mastery",
]


REQUIRED_BUTTON_IDS = [
    "begin-exam-button",
    "next-question-button",
    "retry-button",
    "restart-exam-button",
]


def load_questions() -> list[dict]:
    text = QUESTIONS_JS.read_text(encoding="utf-8")
    start = text.index("[")
    end = text.rindex("]") + 1
    return json.loads(text[start:end])


def validate_questions(items: list[dict]) -> None:
    assert len(items) == 120, f"Expected 120 questions, found {len(items)}"
    assert len({q['id'] for q in items}) == 120, "Question IDs are not unique"
    assert len({q['question'] for q in items}) == 120, "Question text is not unique"

    for exam in (1, 2, 3):
        exam_items = [q for q in items if q["exam"] == exam]
        assert len(exam_items) == 40, f"Exam {exam} has {len(exam_items)} questions"

    for item in items:
        assert len(item["options"]) == 4, f"Question {item['id']} does not have four options"
        assert 0 <= item["correct"] <= 3, f"Question {item['id']} has invalid correct index"
        assert item["question"].strip(), f"Question {item['id']} has empty prompt"
        assert item["category"].strip(), f"Question {item['id']} has empty category"


def validate_structure() -> None:
    html = INDEX_HTML.read_text(encoding="utf-8")
    js = APP_JS.read_text(encoding="utf-8")
    css = STYLE_CSS.read_text(encoding="utf-8")

    for screen_id in REQUIRED_SCREEN_IDS:
        assert f'id="{screen_id}"' in html, f"Missing screen id: {screen_id}"

    for button_id in REQUIRED_BUTTON_IDS:
        assert f'id="{button_id}"' in html, f"Missing button id: {button_id}"

    assert "localStorage" in js, "app.js should persist progress with localStorage"
    assert ".answer-button" in css, "style.css should contain answer button styling"


def main() -> None:
    for path in (QUESTIONS_JS, INDEX_HTML, APP_JS, STYLE_CSS):
        assert path.exists(), f"Missing required file: {path.name}"

    validate_questions(load_questions())
    validate_structure()
    print("Project verification passed.")


if __name__ == "__main__":
    main()
