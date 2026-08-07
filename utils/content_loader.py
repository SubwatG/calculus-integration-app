from pathlib import Path
import re

import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parents[1]
LESSON_DIR = PROJECT_ROOT / "data" / "lessons"
ARCHIVE_DIR = LESSON_DIR / "_archive"

# Files that are app scaffolding, not lessons
NON_LESSONS = {"SPEC.md", "MAPPING.md", "overview.md", "basic_rules.md"}


def _frontmatter_title(text: str) -> str | None:
    """Read title from YAML frontmatter if present."""
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n", text, re.DOTALL)
    if not m:
        return None
    tm = re.search(r"^title:\s*(.+)$", m.group(1), re.MULTILINE)
    if not tm:
        return None
    return tm.group(1).strip().strip("\"'")


def _heading_title(text: str) -> str | None:
    """Fallback: first heading, cleaned of duplicate numbering like '3.6 3.6'."""
    for line in text.splitlines():
        s = line.strip()
        if s.startswith("#"):
            title = re.sub(r"^#+\s*", "", s).strip()
            # "## 3.6 3.6 XXX" -> "3.6 XXX"
            title = re.sub(r"^(\d+\.\d+)\s+\1\b", r"\1", title)
            return title
    return None


def _display_name(filename: str, text: str) -> str:
    title = _frontmatter_title(text) or _heading_title(text)
    if title:
        return title
    # last resort: humanize filename
    stem = Path(filename).stem
    stem = re.sub(r"^silpakorn-(?:cal1-)?", "", stem)
    return stem.replace("-", " ")


def list_lessons() -> list[dict]:
    """Auto-discover lessons from data/lessons/.

    Returns sorted list of {"title": str, "filename": str}.
    Order: cal2 chapters before cal1, then by chapter/section number
    parsed from filename; unparsable names go last alphabetically.
    """
    if not LESSON_DIR.exists():
        return []
    lessons = []
    for p in sorted(LESSON_DIR.rglob("*.md")):
        if ARCHIVE_DIR in p.parents:
            continue
        if p.name in NON_LESSONS:
            continue
        rel = p.relative_to(LESSON_DIR).as_posix()
        try:
            text = p.read_text(encoding="utf-8")
        except Exception:
            continue
        lessons.append(
            {
                "title": _display_name(rel, text),
                "filename": rel,
                "text": text,
            }
        )

    def sort_key(item: dict) -> tuple:
        name = item["filename"]
        # new layout: cal2/ch01/00-intro.md
        m = re.match(r"cal(\d)/ch(\d+)/(\d+)-", name)
        if m:
            return (0, int(m.group(1)), int(m.group(2)), int(m.group(3)), name)
        m = re.match(r"silpakorn-(?:cal1-)?cal1_ch(\d+)-", name)
        if m:
            return (1, int(m.group(1)), 0, 0, name)  # cal1 after cal2
        m = re.match(r"silpakorn-ch(\d+)-", name)
        if m:
            return (2, int(m.group(1)), 0, 0, name)
        return (3, 0, 0, 0, name)

    lessons.sort(key=sort_key)
    return lessons


@st.cache_data
def load_lesson(filename: str) -> str:
    path = LESSON_DIR / filename
    return path.read_text(encoding="utf-8")
