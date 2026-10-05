from typing import Any
import sympy as sp
from sympy.calculus.accumulationbounds import AccumulationBounds
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


def _classify_limit(left: sp.Expr, right: sp.Expr) -> str:
    if isinstance(left, AccumulationBounds) or isinstance(right, AccumulationBounds):
        return "dne"
    if getattr(left, "is_extended_real", None) is not True or getattr(right, "is_extended_real", None) is not True:
        return "unsupported"
    if left == right:
        return "infinite" if left in (sp.oo, -sp.oo) else "finite"
    if getattr(left, "is_number", False) is True and getattr(right, "is_number", False) is True:
        return "dne"
    return "unsupported"


def compute_limit(expr_str: str, point: float | int = 0) -> dict[str, Any]:
    x = sp.Symbol("x")
    try:
        expr = _parse_input(expr_str)
        try:
            left = sp.limit(expr, x, point, dir="-")
            right = sp.limit(expr, x, point, dir="+")
            status = _classify_limit(left, right)
        except Exception:
            left, right = None, None
            status = "unsupported"

        if status == "finite":
            result = sp.limit(expr, x, point)
            latex_str = sp.latex(result)
            steps = ["คำนวณด้วย SymPy (เครื่องมือเชิงสัญลักษณ์)"]
        elif status == "infinite":
            result = left
            latex_str = sp.latex(result)
            steps = ["ลิมิตทั้งสองข้างลู่ไปสู่อนันต์เดียวกัน"]
        elif status == "dne":
            result = None
            latex_str = f"\\lim_{{x \\to {point}}} {sp.latex(expr)} \\quad \\text{{(does not exist)}}"
            steps = [f"ลิมิตซ้าย ({sp.latex(left)}) ไม่เท่ากับลิมิตขวา ({sp.latex(right)}) จึงไม่มีลิมิตสองด้าน"]
        else:
            result = None
            latex_str = f"\\lim_{{x \\to {point}}} {sp.latex(expr)} \\quad \\text{{(unsupported)}}"
            steps = ["ระบบไม่สามารถตัดสินหรือระบุค่าลิมิตได้"]

        return {
            "ok": True,
            "result": result,
            "latex": latex_str,
            "steps": steps,
            "error": None,
            "status": status,
            "left_limit": left,
            "right_limit": right,
        }
    except Exception:
        return {
            "ok": False,
            "result": None,
            "latex": "",
            "steps": [],
            "error": "ไม่สามารถอ่านนิพจน์ได้ กรุณาตรวจสอบรูปแบบ เช่น x**2, sin(x), (x**2-4)/(x-2)",
            "status": "error",
            "left_limit": None,
            "right_limit": None,
        }
