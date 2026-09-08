from typing import Any
import sympy as sp
from sympy.parsing.sympy_parser import (
    convert_xor,
    implicit_multiplication_application,
    parse_expr,
    standard_transformations,
)


TRANSFORMATIONS = standard_transformations + (
    implicit_multiplication_application,
    convert_xor,
)

LOCAL_MATH_DICT = {
    "e": sp.E,
    "E": sp.E,
    "pi": sp.pi,
    "ln": sp.log,
}


def _parse_input(expr_str: str) -> sp.Expr:
    clean_str = expr_str.strip()
    if not clean_str:
        raise ValueError("Empty input string")
    return parse_expr(clean_str, transformations=TRANSFORMATIONS, local_dict=LOCAL_MATH_DICT)


def integrate(expr_str: str) -> dict[str, Any]:
    x = sp.Symbol("x")
    try:
        expr = _parse_input(expr_str)
        result = sp.integrate(expr, x)

        if expr == x:
            steps = ["ใช้กฎกำลัง: ∫ x^n dx = x^(n+1)/(n+1) + C (n ≠ -1)"]
        elif isinstance(expr, sp.Pow) and expr.args[0] == x and expr.args[1].is_number:
            n = expr.args[1]
            if n == -1:
                steps = ["ใช้กฎ: ∫ 1/x dx = ln|x| + C"]
            else:
                steps = ["ใช้กฎกำลัง: ∫ x^n dx = x^(n+1)/(n+1) + C (n ≠ -1)"]
        else:
            steps = ["คำนวณด้วย SymPy (เครื่องมือเชิงสัญลักษณ์)"]

        latex_str = sp.latex(result) + r" + C"
        return {
            "ok": True,
            "result": result,
            "latex": latex_str,
            "steps": steps,
            "error": None,
        }
    except Exception:
        return {
            "ok": False,
            "result": None,
            "latex": "",
            "steps": [],
            "error": "ไม่สามารถอ่านนิพจน์ได้ กรุณาตรวจสอบรูปแบบ เช่น x**2, sin(x), (x**2-4)/(x-2)",
        }


def differentiate(expr_str: str) -> dict[str, Any]:
    x = sp.Symbol("x")
    try:
        expr = _parse_input(expr_str)
        result = sp.diff(expr, x)

        if expr == x or (
            isinstance(expr, sp.Pow) and expr.args[0] == x and expr.args[1].is_number
        ):
            steps = ["ใช้กฎกำลัง: d/dx x^n = n·x^(n-1)"]
        else:
            steps = ["คำนวณด้วย SymPy (เครื่องมือเชิงสัญลักษณ์)"]

        latex_str = sp.latex(result)
        return {
            "ok": True,
            "result": result,
            "latex": latex_str,
            "steps": steps,
            "error": None,
        }
    except Exception:
        return {
            "ok": False,
            "result": None,
            "latex": "",
            "steps": [],
            "error": "ไม่สามารถอ่านนิพจน์ได้ กรุณาตรวจสอบรูปแบบ เช่น x**2, sin(x), (x**2-4)/(x-2)",
        }


def compute_limit(expr_str: str, point: float | int = 0) -> dict[str, Any]:
    x = sp.Symbol("x")
    try:
        expr = _parse_input(expr_str)
        result = sp.limit(expr, x, point)
        steps = ["คำนวณด้วย SymPy (เครื่องมือเชิงสัญลักษณ์)"]

        latex_str = sp.latex(result)
        return {
            "ok": True,
            "result": result,
            "latex": latex_str,
            "steps": steps,
            "error": None,
        }
    except Exception:
        return {
            "ok": False,
            "result": None,
            "latex": "",
            "steps": [],
            "error": "ไม่สามารถอ่านนิพจน์ได้ กรุณาตรวจสอบรูปแบบ เช่น x**2, sin(x), (x**2-4)/(x-2)",
        }
