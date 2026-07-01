from pathlib import Path

import streamlit as st


PROJECT_ROOT = Path(__file__).resolve().parents[1]
LESSON_DIR = PROJECT_ROOT / "data" / "lessons"


@st.cache_data
def load_lesson(filename: str) -> str:
    path = LESSON_DIR / filename
    return path.read_text(encoding="utf-8")
