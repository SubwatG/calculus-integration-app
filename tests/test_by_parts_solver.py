"""tests/test_by_parts_solver.py — การทดสอบ Integration by Parts Solver เฉพาะทาง
"""

import pytest
import sympy as sp

from utils.by_parts_solver import detect_parts_candidate, solve_by_parts


class TestByPartsSolver:
    def test_solve_by_parts_x_exp_x(self):
        res = solve_by_parts("x*exp(x)")
        assert res["ok"] is True
        assert res["status"] == "elementary"
        x = sp.Symbol("x")
        expected = (x - 1) * sp.exp(x)
        assert sp.simplify(res["result"] - expected) == 0
        assert res["parts_info"] is not None
        assert str(res["parts_info"]["u"]) == "x"
        assert str(res["parts_info"]["dv"]) == "exp(x)"
        steps_text = " ".join(res["steps"])
        assert "LIATE" in steps_text
        assert "uv - \\int v \\, du" in steps_text

    def test_solve_by_parts_single_ln_x(self):
        res = solve_by_parts("ln(x)")
        assert res["ok"] is True
        assert res["status"] == "elementary"
        x = sp.Symbol("x")
        expected = x * sp.log(x) - x
        assert sp.simplify(res["result"] - expected) == 0
        assert str(res["parts_info"]["u"]) == "log(x)"
        assert str(res["parts_info"]["dv"]) == "1"

    def test_solve_by_parts_x_sin_x(self):
        res = solve_by_parts("x*sin(x)")
        assert res["ok"] is True
        assert res["status"] == "elementary"
        x = sp.Symbol("x")
        expected = -x * sp.cos(x) + sp.sin(x)
        assert sp.simplify(res["result"] - expected) == 0

    def test_solve_by_parts_warns_when_u_sub_is_better(self):
        # 2x * sqrt(x^2 + 1) is clearly a u-substitution problem
        res = solve_by_parts("2*x*sqrt(x**2 + 1)")
        assert res["ok"] is True
        assert res["status"] == "better_suited_for_substitution"
        assert "u-Substitution" in res["warning"] or "การแทนตัวแปร u" in res["warning"]

    def test_solve_by_parts_cyclic_exp_cos(self):
        res = solve_by_parts("exp(x)*cos(x)")
        assert res["ok"] is True
        assert res["status"] == "elementary"
        steps_text = " ".join(res["steps"])
        assert "Cyclic" in steps_text or "วนลูป" in steps_text
        assert "รอบที่ 1" in steps_text
        assert "รอบที่ 2" in steps_text

    def test_solve_by_parts_cyclic_2_to_x_cos(self):
        res = solve_by_parts("2^x*cos(x)")
        assert res["ok"] is True
        assert res["status"] == "elementary"
        steps_text = " ".join(res["steps"])
        assert "Cyclic" in steps_text or "วนลูป" in steps_text
        assert "รอบที่ 1" in steps_text
        assert "รอบที่ 2" in steps_text
        assert "Solve for I" in steps_text or "แก้สมการ" in steps_text

    def test_solve_by_parts_invalid_input(self):
        res = solve_by_parts("")
        assert res["ok"] is False
        assert res["status"] == "error"

    def test_solve_by_parts_log_absolute_values(self):
        """MATH-08: by parts สำหรับ x*sec(x)**2 และ x*csc(x)**2 ต้องมีค่าสัมบูรณ์ในพจน์ log"""
        x = sp.Symbol("x")
        res_sec = solve_by_parts("x*sec(x)**2")
        assert res_sec["ok"] is True
        assert res_sec["result"] == x * sp.tan(x) + sp.log(sp.Abs(sp.cos(x)))
        assert "|" in res_sec["latex"]

        res_csc = solve_by_parts("x*csc(x)**2")
        assert res_csc["ok"] is True
        assert res_csc["result"] == -x * sp.cot(x) + sp.log(sp.Abs(sp.sin(x)))
        assert "|" in res_csc["latex"]

    def test_solve_by_parts_non_elementary_rejected(self):
        """MATH-10: x*tan(x) และ x*sec(x) ไม่มีปฏิยานุพันธ์มูลฐาน ต้องไม่คืน Integral"""
        res_tan = solve_by_parts("x*tan(x)")
        assert res_tan["ok"] is False
        assert res_tan["result"] is None
        assert res_tan["status"] == "unsupported"
        assert "ไม่มีปฏิยานุพันธ์" in res_tan["error"]

        res_sec = solve_by_parts("x*sec(x)")
        assert res_sec["ok"] is False
        assert res_sec["result"] is None
        assert res_sec["status"] == "unsupported"
        assert "ไม่มีปฏิยานุพันธ์" in res_sec["error"]

    def test_solve_by_parts_sec2_csc2_multiple_angle(self):
        """x*sec(2*x)**2 และ x*csc(2*x)**2 สามารถคำนวณ By Parts ได้"""
        res_sec2 = solve_by_parts("x*sec(2*x)**2")
        assert res_sec2["ok"] is True
        assert res_sec2["result"] is not None
        assert not res_sec2["result"].has(sp.Integral)
        assert r"\tan" in res_sec2["latex"]
        assert r"\cos" in res_sec2["latex"]
        assert "|" in res_sec2["latex"]

        res_csc2 = solve_by_parts("x*csc(2*x)**2")
        assert res_csc2["ok"] is True
        assert res_csc2["result"] is not None
        assert not res_csc2["result"].has(sp.Integral)
        assert "|" in res_csc2["latex"]
