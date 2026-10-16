"""Test สำหรับ test_substitution_solver.py

TODO: นักศึกษา implement solver ให้ test นี้ผ่าน
ค่าคาดหวังอ้างอิงจาก docs/interactive-lessons-plan.md
"""

import pytest
import sympy as sp

from utils.substitution_solver import solve_substitution


class TestSolveSubstitution:
    def test_solve_substitution_basic(self):
        res = solve_substitution('2*x*exp(x**2)')
        assert res["ok"] is True
        assert res["status"] == "elementary"
        assert res["u_candidate"] is not None
        assert res["result"] is not None
        assert len(res["steps"]) >= 3

    def test_solve_substitution_detects_u_candidate(self):
        res = solve_substitution('(2*x + 1)*(x**2 + x)**5')
        assert res["ok"] is True
        assert res["status"] == "elementary"
        assert str(res["u_candidate"]) == "x**2 + x"
        assert str(res["du_candidate"]) == "2*x + 1"

    def test_solve_substitution_non_elementary_gaussian(self):
        res = solve_substitution('exp(-x**2)')
        assert res["ok"] is True
        assert res["status"] == "non_elementary"
        assert res["warning"] is not None
        assert "erf" in str(res["result"])
        assert "Non-Elementary" in res["steps"][1]

    def test_solve_substitution_non_elementary_sinc(self):
        res = solve_substitution('sin(x)/x')
        assert res["ok"] is True
        assert res["status"] == "non_elementary"
        assert "Si" in str(res["result"])

    def test_solve_substitution_invalid_input(self):
        res = solve_substitution('')
        assert res["ok"] is False
        assert res["status"] == "error"
        assert res["error"]

    def test_solve_substitution_has_latex_result(self):
        res = solve_substitution('2*x*exp(x**2)')
        assert res["ok"] is True
        assert res["latex"]

    def test_solve_substitution_variable_t(self):
        res = solve_substitution('2*t*exp(t**2)')
        assert res["ok"] is True
        assert res["variable"] == "t"
        assert str(res["u_candidate"]) == "t**2"
        assert "dt" in res["latex"]

    def test_solve_substitution_u_sub_detailed_steps(self):
        res = solve_substitution("2*x*cos(x**2)")
        assert res["ok"] is True
        assert res["status"] == "elementary"
        x = sp.Symbol("x")
        assert sp.simplify(res["result"] - sp.sin(x**2)) == 0
        steps_text = " ".join(res["steps"])
        assert "การเปลี่ยนตัวแปร" in steps_text or "u-Substitution" in steps_text
        assert "u = x^{2}" in steps_text or "x^{2}" in str(res["u_candidate"])
        assert "du = 2 x" in steps_text or "2 x" in steps_text
        assert "แทนค่ากลับ" in steps_text or "u = x^{2}" in steps_text
        assert "+ C" in res["latex"]
        assert "+ C" in steps_text

    def test_solve_substitution_by_parts_x_ln_x(self):
        res = solve_substitution("x*ln(x)")
        assert res["ok"] is True
        assert res["status"] == "elementary"
        x = sp.Symbol("x")
        expected = (x**2 * sp.log(x)) / 2 - (x**2) / 4
        assert sp.simplify(res["result"] - expected) == 0
        steps_text = " ".join(res["steps"])
        assert "การอินทิเกรตทีละส่วน" in steps_text or "By Parts" in steps_text
        assert "u = \\ln(x)" in steps_text or "u = \\log(x)" in steps_text or "\\ln" in steps_text
        assert "dv = x" in steps_text
        assert "du = \\frac{1}{x}" in steps_text or "1/x" in steps_text
        assert "v = " in steps_text and "\\frac{x^{2}}{2}" in steps_text
        assert "uv - \\int" in steps_text or "uv - \\int v \\, du" in steps_text
        assert "x > 0" in steps_text or "โดเมน" in steps_text
        assert "+ C" in res["latex"]
        assert "+ C" in steps_text

    def test_solve_substitution_by_parts_ln_x(self):
        res = solve_substitution("ln(x)")
        assert res["ok"] is True
        assert res["status"] == "elementary"
        x = sp.Symbol("x")
        expected = x * sp.log(x) - x
        assert sp.simplify(res["result"] - expected) == 0
        steps_text = " ".join(res["steps"])
        assert "dv = 1" in steps_text or "dv = dx" in steps_text or "dv = 1 \\, dx" in steps_text
        assert "x > 0" in steps_text or "โดเมน" in steps_text

    def test_solve_substitution_by_parts_x_exp_x(self):
        res = solve_substitution("x*exp(x)")
        assert res["ok"] is True
        assert res["status"] == "elementary"
        x = sp.Symbol("x")
        expected = (x - 1) * sp.exp(x)
        assert sp.simplify(res["result"] - expected) == 0
        steps_text = " ".join(res["steps"])
        assert "u = x" in steps_text
        assert "e^{x}" in steps_text or "exp(x)" in steps_text

    def test_solve_substitution_non_elementary_exp_x2(self):
        res = solve_substitution("exp(x**2)")
        assert res["ok"] is True
        assert res["status"] == "non_elementary"
        assert res["result"].has(sp.erfi)
        steps_text = " ".join(res["steps"])
        assert "Non-Elementary" in steps_text


def test_substitution_page_apptest_render():
    from streamlit.testing.v1 import AppTest
    at = AppTest.from_file("pages/substitution.py")
    at.run()
    assert not at.exception
    btn = [b for b in at.button if b.key == "btn_substitution_calc"][0]
    at.session_state["substitution_expr"] = "x*ln(x)"
    btn.click().run()
    assert not at.exception
    all_text = " ".join([m.value for m in at.markdown] + [info.value for info in at.info])
    assert "By Parts" in all_text or "การอินทิเกรตทีละส่วน" in all_text
