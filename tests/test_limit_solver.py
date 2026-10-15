"""Test สำหรับ test_limit_solver.py

ตรวจสอบสองด้าน:
  (1) Backward compatibility — โครงสร้าง dictionary และพฤติกรรมเดิมของ compute_limit_near
  (2) Pedagogical Hierarchy — ขั้นตอนการเฉลยจำแนกตามธรรมชาติของการสอนแคลคูลัส
      Level 1 Direct Substitution        (แทนค่าโดยตรง / ฟังก์ชันต่อเนื่อง)
      Level 2 Indeterminate 0/0          (แยกตัวประกอบ -> ตัดทอน -> แทนค่า)
      Level 3 Special Trig Limit         (lim sin(g)/g = 1)
      Level 4 Infinite Limit c/0         (เส้นกำกับแนวดิ่ง วิเคราะห์เครื่องหมายสองฝั่ง)
      Level 5 Absolute Value / Piecewise (แยกพิจารณาลิมิตซ้าย/ขวา)
      Level 6 Oscillating                (แกว่งกวัด ไม่มีลิมิต)
      Level 7 End Behavior (±∞)          (เส้นกำกับแนวนอน)
"""

import pytest
import sympy as sp

from utils.limit_solver import compute_limit_near
from utils.plotter import plot_limit_near


REQUIRED_KEYS = (
    "ok",
    "result",
    "latex",
    "steps",
    "expr",
    "error",
    "status",
    "variable",
    "left_limit",
    "right_limit",
    "is_oscillating",
    "a_sp",
)


def _steps_text(res: dict) -> str:
    """รวมข้อความทุกขั้นตอนไว้ด้วยกันเพื่อค้นหาคำสำคัญ"""
    return "\n".join(res["steps"])


class TestComputeLimitNear:
    """ชุดทดสอบเดิม (backward compatibility)"""

    def test_compute_limit_near_basic(self):
        res = compute_limit_near("(x**2-4)/(x-2)", 2)
        assert res["ok"] is True
        assert res["result"] == 4.0
        assert res["status"] == "finite"
        assert len(res["steps"]) >= 4

    def test_compute_limit_sin_x_over_x(self):
        res = compute_limit_near("sin(x)/x", 0)
        assert res["ok"] is True
        assert pytest.approx(res["result"]) == 1.0
        assert res["status"] == "finite"

    def test_compute_limit_near_invalid_input(self):
        res = compute_limit_near("", 2)
        assert res["ok"] is False
        assert res["status"] == "error"
        assert res["error"]

    def test_compute_limit_near_has_latex_result(self):
        res = compute_limit_near("(x**2-4)/(x-2)", 2)
        assert res["ok"] is True
        assert "4" in res["latex"]

    def test_plot_limit_near_figure(self):
        expr = sp.sympify("(x**2-4)/(x-2)")
        fig, ax = plot_limit_near(expr, 2.0, delta=0.2)
        assert fig is not None
        assert ax is not None

    def test_two_sided_limit_dne(self):
        res = compute_limit_near("1/x", 0)
        assert res["ok"] is True
        assert res["status"] == "dne"
        assert res["result"] is None
        assert res["left_limit"] == -sp.oo
        assert res["right_limit"] == sp.oo
        assert "\\neq" in res["steps"][-1]
        assert "ไม่มีลิมิต" in res["steps"][-1]

    def test_one_sided_domain_boundary_sqrt(self):
        res = compute_limit_near("sqrt(x)", 0)
        assert res["ok"] is True
        assert res["status"] == "right_only"
        assert res["result"] == 0.0
        assert "ลิมิตทางขวา" in res["steps"][1]

    def test_one_sided_domain_boundary_log(self):
        res = compute_limit_near("log(x)", 0)
        assert res["ok"] is True
        assert res["status"] == "right_only"
        assert res["result"] is None
        assert res["right_limit"] == -sp.oo

    def test_oscillating_singularity_sin_one_over_x(self):
        res = compute_limit_near("sin(1/x)", 0)
        assert res["ok"] is True
        assert res["status"] == "dne"
        assert res["is_oscillating"] is True
        assert any("แกว่งกวัด" in step for step in res["steps"])

    def test_equal_infinite_sides(self):
        res = compute_limit_near("1/x**2", 0)
        assert res["ok"] is True
        assert res["status"] == "infinite"
        assert res["result"] is None
        assert res["left_limit"] == res["right_limit"] == sp.oo

    def test_compute_limit_near_variable_t(self):
        res = compute_limit_near("sin(t)/t", 0)
        assert res["ok"] is True
        assert res["variable"] == "t"
        assert res["result"] == 1.0
        assert "\\lim_{t \\to 0}" in res["latex"]

    def test_return_keys_backward_compatible(self):
        res = compute_limit_near("(x**2-4)/(x-2)", 2)
        for key in REQUIRED_KEYS:
            assert key in res, f"missing key: {key}"
        assert res["a_str"] == "2"
        assert res["a_dir_left"] and res["a_dir_right"]
        assert res["is_infinite"] is False
        assert res["expr"] is not None


class TestPedagogicalHierarchy:
    """ชุดทดสอบใหม่: ขั้นตอนการเฉลยตามลำดับการสอน"""

    # ---------------- Level 1: Direct Substitution ----------------
    def test_level1_direct_substitution_polynomial(self):
        res = compute_limit_near("3*x+1", 2)
        assert res["ok"] is True
        assert res["status"] == "finite"
        assert res["result"] == 7.0
        text = _steps_text(res)
        assert "การแทนค่าโดยตรง" in text
        assert "f(2)" in text          # แสดงการคำนวณ f(a)
        # ต้องไม่ใช้ข้อความสองด้านแบบแข็งทื่อ
        assert "พิจารณาลิมิตทางซ้าย" not in text
        assert "พิจารณาลิมิตทางขวา" not in text

    def test_level1_direct_substitution_continuous_function(self):
        res = compute_limit_near("cos(x)", 0)
        assert res["status"] == "finite"
        assert res["result"] == 1.0
        text = _steps_text(res)
        assert "การแทนค่าโดยตรง" in text
        assert "f(0)" in text
        assert "พิจารณาลิมิตทางซ้าย" not in text

    # ---------------- Level 2: Indeterminate 0/0 ----------------
    def test_level2_indeterminate_shows_preliminary_00(self):
        res = compute_limit_near("(x**2-9)/(x-3)", 3)
        assert res["status"] == "finite"
        assert res["result"] == 6.0
        text = _steps_text(res)
        assert "ยังไม่กำหนด" in text                     # ระบุ Indeterminate Form
        assert "\\frac{0}{0}" in text                    # แสดงการแทนค่าเบื้องต้น = 0/0

    def test_level2_indeterminate_factoring_and_cancelling(self):
        res = compute_limit_near("(x**2-9)/(x-3)", 3)
        text = _steps_text(res)
        assert "แยกตัวประกอบ" in text
        assert "ตัดทอน" in text
        assert "x - 3" in text                           # เห็นตัวร่วมที่ถูกตัดทอน
        assert "x - 3" in text and "x + 3" in text       # ตัวประกอบของเศษและตัวส่วน
        # ไม่ใช้ข้อความสองด้านแบบแข็งทื่อกับโจทย์ 0/0 ที่แยกตัวประกอบได้
        assert "พิจารณาลิมิตทางซ้าย" not in text
        assert "พิจารณาลิมิตทางขวา" not in text

    def test_level2_cancel_justification_x_neq_a(self):
        res = compute_limit_near("(x**2-4)/(x-2)", 2)
        assert res["result"] == 4.0
        text = _steps_text(res)
        assert "x \\neq 2" in text                       # เหตุผลว่าตัดทอนได้เพราะ x != 2
        assert "\\lim_{x \\to 2}" in text
        assert res["latex"].endswith("= 4")

    def test_level2_substitutes_into_reduced_form(self):
        res = compute_limit_near("(x**3-8)/(x-2)", 2)
        assert res["status"] == "finite"
        assert pytest.approx(res["result"]) == 12.0
        text = _steps_text(res)
        assert "แยกตัวประกอบ" in text
        assert "ตัดทอน" in text

    # ---------------- Level 3: Special Trig Limit ----------------
    def test_level3_special_trig_limit(self):
        res = compute_limit_near("sin(x)/x", 0)
        assert res["status"] == "finite"
        assert pytest.approx(res["result"]) == 1.0
        text = _steps_text(res)
        assert "ตรีโกณมิติ" in text
        assert "Squeeze" in text or "ทฤษฎีบทบีบ" in text
        assert "แยกตัวประกอบ" not in text                # ไม่ใช่เส้นทาง 0/0 แบบแยกตัวประกอบ

    def test_level3_special_trig_limit_with_coefficient(self):
        res = compute_limit_near("sin(3*x)/x", 0)
        assert res["status"] == "finite"
        assert pytest.approx(res["result"]) == 3.0
        assert "ตรีโกณมิติ" in _steps_text(res)

    # ---------------- Level 4: Infinite Limit / Asymptote ----------------
    def test_level4_infinite_asymptote_opposite_signs_dne(self):
        res = compute_limit_near("1/x", 0)
        assert res["status"] == "dne"
        assert res["result"] is None
        text = _steps_text(res)
        assert "เส้นกำกับแนวดิ่ง" in text
        assert "พิจารณาลิมิตทางซ้าย" in text
        assert "พิจารณาลิมิตทางขวา" in text
        assert "ไม่มีลิมิต" in res["steps"][-1]
        assert "\\neq" in res["steps"][-1]

    def test_level4_infinite_asymptote_same_sign(self):
        res = compute_limit_near("1/x**2", 0)
        assert res["status"] == "infinite"
        assert res["result"] is None
        text = _steps_text(res)
        assert "เส้นกำกับแนวดิ่ง" in text
        assert "ลู่ออกสู่อนันต์" in text or "Diverges" in text
        assert "พิจารณาลิมิตทางซ้าย" in text and "พิจารณาลิมิตทางขวา" in text

    # ---------------- Level 5: Absolute Value / Piecewise ----------------
    def test_level5_absolute_value_dne(self):
        res = compute_limit_near("abs(x)/x", 0)
        assert res["status"] == "dne"
        assert res["result"] is None
        text = _steps_text(res)
        assert "ค่าสัมบูรณ์" in text
        assert "พิจารณาลิมิตทางซ้าย" in text
        assert "พิจารณาลิมิตทางขวา" in text
        assert "ไม่มีลิมิต" in res["steps"][-1]

    def test_level5_absolute_value_shifted_dne(self):
        res = compute_limit_near("abs(x-2)/(x-2)", 2)
        assert res["status"] == "dne"
        assert res["result"] is None
        text = _steps_text(res)
        assert "ค่าสัมบูรณ์" in text
        assert "ไม่มีลิมิต" in res["steps"][-1]

    def test_level5_absolute_value_continuous_point(self):
        res = compute_limit_near("abs(x)", 0)
        assert res["status"] == "finite"
        assert res["result"] == 0.0
        assert "ค่าสัมบูรณ์" in _steps_text(res)

    # ---------------- Level 6 & 7: ต้องคงเดิม ----------------
    def test_level6_oscillating_intact(self):
        res = compute_limit_near("sin(1/x)", 0)
        assert res["is_oscillating"] is True
        assert res["status"] == "dne"
        assert "แกว่งกวัด" in _steps_text(res)

    def test_level7_end_behavior_intact(self):
        res = compute_limit_near("1/x", "inf")
        assert res["status"] == "finite"
        assert res["result"] == 0.0
        text = _steps_text(res)
        assert "End Behavior" in text
        assert "เส้นกำกับแนวนอน" in text

    def test_level7_end_behavior_negative_inf(self):
        res = compute_limit_near("1/x", "-inf")
        assert res["status"] == "finite"
        assert res["result"] == 0.0
        assert "End Behavior" in _steps_text(res)

    # ---------------- ความสมบูรณ์ของ LaTeX ในขั้นตอน ----------------
    def test_steps_latex_delimiters_balanced(self):
        cases = [
            ("(x**2-4)/(x-2)", 2),
            ("sin(x)/x", 0),
            ("sin(t)/t", 0),
            ("3*x+1", 2),
            ("1/x", 0),
            ("1/x**2", 0),
            ("abs(x)/x", 0),
            ("sqrt(x)", 0),
            ("log(x)", 0),
            ("sin(1/x)", 0),
            ("1/x", "inf"),
        ]
        for expr, a in cases:
            res = compute_limit_near(expr, a)
            assert res["ok"] is True, (expr, res.get("error"))
            assert res["steps"], expr
            for step in res["steps"]:
                assert step.count("$") % 2 == 0, (expr, step)

    def test_every_case_has_header_step(self):
        for expr, a in [("(x**2-4)/(x-2)", 2), ("1/x", 0), ("sin(1/x)", 0), ("sqrt(x)", 0)]:
            res = compute_limit_near(expr, a)
            assert "กำหนดโจทย์ลิมิต" in res["steps"][0]
