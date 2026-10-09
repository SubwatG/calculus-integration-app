"""ตัวอย่าง test สำหรับ utils.sympy_solver

ครอบ logic บริสุทธิ์ (ไม่ต้องเปิด Streamlit)
เพิ่ม test ใหม่ในไฟล์นี้หรือสร้างไฟล์ test_*.py เพิ่มได้

หมายเหตุ: utils.sympy_solver เก็บ `result` เป็น sympy.Expr ไม่ใช่ string
จึงเปรียบเทียบกับ sympy expression (sp.sympify / sp.Rational) เสมอ
"""

import sympy as sp
import pytest

from utils.sympy_solver import compute_limit, detect_variable, differentiate, integrate


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
        assert res["status"] == "finite"

    def test_limit_to_zero_dne(self):
        res = compute_limit("1/x", 0)
        assert res["ok"] is True
        assert res["status"] == "dne"
        assert res["result"] is None
        assert res["left_limit"] == -sp.oo
        assert res["right_limit"] == sp.oo

    def test_limit_equal_infinite(self):
        res = compute_limit("1/x**2", 0)
        assert res["ok"] is True
        assert res["status"] == "infinite"
        assert res["left_limit"] == res["right_limit"] == sp.oo

    def test_invalid_input(self):
        res = compute_limit("", 0)
        assert res["ok"] is False
        assert res["status"] == "error"


class TestAutoDetectVariable:
    def test_detect_variable_single(self):
        assert detect_variable("3*t**2 + 2*t") == "t"
        assert detect_variable("sin(u)") == "u"
        assert detect_variable("y**3 - 4*y") == "y"
        assert detect_variable("theta**2") == "theta"

    def test_detect_variable_default_constant(self):
        assert detect_variable("5") == "x"
        assert detect_variable("pi") == "x"
        assert detect_variable("") == "x"

    def test_integrate_auto_detect_t(self):
        res = integrate("3*t**2 + 2*t")
        assert res["ok"] is True
        assert res["variable"] == "t"
        assert expr_eq(res["result"], "t**3 + t**2")
        assert "dt" in res["latex"]
        assert "dt" in res["steps"][0]

    def test_integrate_auto_detect_u(self):
        res = integrate("sin(u)")
        assert res["ok"] is True
        assert res["variable"] == "u"
        assert expr_eq(res["result"], "-cos(u)")
        assert "du" in res["latex"]

    def test_differentiate_auto_detect_t(self):
        res = differentiate("3*t**2 + 2*t")
        assert res["ok"] is True
        assert res["variable"] == "t"
        assert expr_eq(res["result"], "6*t + 2")
        assert "\\frac{d}{dt}" in res["latex"]

    def test_compute_limit_auto_detect_t(self):
        res = compute_limit("t**2", 3)
        assert res["ok"] is True
        assert res["variable"] == "t"
        assert expr_eq(res["result"], "9")
        assert "\\lim_{t \\to 3}" in res["latex"]

    def test_differential_stripping_and_detection(self):
        res = integrate("3*t**2 dt")
        assert res["ok"] is True
        assert res["variable"] == "t"
        assert expr_eq(res["result"], "t**3")
        assert "dt" in res["latex"]

    def test_single_dt_integration(self):
        res = integrate("dt")
        assert res["ok"] is True
        assert res["variable"] == "t"
        assert expr_eq(res["result"], "t")

    def test_parameter_constant_priority(self):
        # In k*t, t should be detected as the independent variable over constant k
        res = integrate("k*t")
        assert res["ok"] is True
        assert res["variable"] == "t"
        assert expr_eq(res["result"], "k*t**2 / 2")

        # In c*t, t should be preferred over c
        res2 = integrate("c*t")
        assert res2["ok"] is True
        assert res2["variable"] == "t"
        assert expr_eq(res2["result"], "c*t**2 / 2")


