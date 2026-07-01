import json
from pathlib import Path
from typing import Any

import streamlit as st


PROJECT_ROOT = Path(__file__).resolve().parents[1]
QUIZ_DIR = PROJECT_ROOT / "data" / "quizzes"


@st.cache_data
def load_quiz(topic: str) -> list[dict[str, Any]]:
    path = QUIZ_DIR / f"{topic}.json"
    return json.loads(path.read_text(encoding="utf-8"))


def grade_quiz(
    questions: list[dict[str, Any]],
    answers: dict[int, str | None],
) -> dict[str, int]:
    score = 0

    for index, question in enumerate(questions):
        if answers.get(index) == question["answer"]:
            score += 1

    return {"score": score, "total": len(questions)}
