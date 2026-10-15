"""tests/test_pages_apptest.py

Automated sanity checks for all Streamlit pages using Streamlit AppTest.
Ensures every page can mount and execute its default run without raising uncaught exceptions.
"""

from pathlib import Path
import pytest
from streamlit.testing.v1 import AppTest

PAGES_DIR = Path(__file__).resolve().parent.parent / "pages"
PAGE_FILES = sorted([str(p) for p in PAGES_DIR.glob("*.py") if p.is_file()])


@pytest.mark.parametrize("page_path", PAGE_FILES, ids=lambda p: Path(p).name)
def test_page_renders_without_exception(page_path: str):
    at = AppTest.from_file(page_path)
    at.run(timeout=5)
    assert not at.exception, f"Page {Path(page_path).name} raised exception: {at.exception}"
