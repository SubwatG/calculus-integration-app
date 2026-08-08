"""ตัวอย่าง test สำหรับ utils.sympy_solver

ครอบ logic บริสุทธิ์ (ไม่ต้องเปิด Streamlit)
เพิ่ม test ใหม่ในไฟล์นี้หรือสร้างไฟล์ test_*.py เพิ่มได้

หมายเหตุ: utils.sympy_solver เก็บ `result` เป็น sympy.Expr ไม่ใช่ string
จึงเปรียบเทียบกับ sympy expression (sp.sympify / sp.Rational) เสมอ
"""

import sympy as sp
import pytest

from utils.sympy_solver import compute_limit, differentiate, integrate


def expr_eq(result, expected: str) -> bool:
    """เปรียบเทียบ sympy.Expr กับ string โดยไม่สนใจรูปการจัดเรียง"""
    return sp.simplify(result - sp.sympify(expected)) == 0


class TestIntegrate:
    def test_power_rule(self):
        res = integrate("x**4")
        assert res["ok"] is True
        assert expr_eq(res["result"], "x**5/5")

    def test_constant(self):
        res = integrate("5")
        assert res["ok"] is True
        assert expr_eq(res["result"], "5*x")

    def test_sum_rule(self):
        res = integrate("3*x**2 - 4*x + 5")
        assert res["ok"] is True
        # x^3 - 2x^2 + 5x
        assert expr_eq(res["result"], "x**3 - 2*x**2 + 5*x")

    def test_reciprocal_is_log(self):
        res = integrate("1/x")
        assert res["ok"] is True
        # SymPy ให้ log(x) (ขอบเขตจำนวนจริงบวก)
        assert "log" in sp.sstr(res["result"])

    def test_invalid_input_returns_error(self):
        res = integrate("")
        assert res["ok"] is False
        assert res["error"]


class TestDifferentiate:
    def test_power_rule(self):
        res = differentiate("x**4")
        assert res["ok"] is True
        assert expr_eq(res["result"], "4*x**3")

    def test_invalid_input(self):
        res = differentiate("")
        assert res["ok"] is False


class TestComputeLimit:
    def test_basic_limit(self):
        res = compute_limit("x**2", 3)
        assert res["ok"] is True
        assert expr_eq(res["result"], "9")

    def test_limit_to_zero(self):
        res = compute_limit("1/x", 0)
        assert res["ok"] is True
        # SymPy ให้ zoo (complex infinity) หรือ oo แล้วแต่รุ่น
        assert str(res["result"]) in ("zoo", "oo", "-oo")

    def test_invalid_input(self):
        res = compute_limit("", 0)
        assert res["ok"] is False
