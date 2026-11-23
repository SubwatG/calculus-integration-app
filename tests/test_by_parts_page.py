from pathlib import Path
from streamlit.testing.v1 import AppTest

PAGES_DIR = Path(__file__).resolve().parent.parent / "pages"
BP_PAGE = str(PAGES_DIR / "by_parts.py")


def test_by_parts_page_initial_render_no_premature_answer():
    """UX PED-01 / PED-02: เมื่อเปิดหน้าขึ้นมาครั้งแรก ต้องไม่แสดงเฉลยก่อนที่ผู้ใช้จะเลือกคำตอบ"""
    at = AppTest.from_file(BP_PAGE)
    at.run(timeout=5)
    assert not at.exception
    # Initially, no radio is selected (index=None), so there must be no success alert
    assert len(at.success) == 0

    # There should be an info guiding the student to pick an approach
    assert any("โปรดเลือกแนวทางด้านบน" in info.value for info in at.info)


def test_by_parts_decision_gate_radio_selection():
    """เมื่อผู้เรียนเลือกตัวเลือกที่ถูกต้อง จึงแสดงเฉลยพร้อมวิธีทำ"""
    at = AppTest.from_file(BP_PAGE)
    at.run(timeout=5)
    assert not at.exception

    if at.radio(key="radio_parts_case1"):
        r = at.radio(key="radio_parts_case1")
        # Select correct choice (Option 1)
        r.set_value(r.options[0]).run(timeout=5)
        assert not at.exception
        assert len(at.success) >= 1
        assert "ถูกต้องตามหลักการ" in at.success[0].value
