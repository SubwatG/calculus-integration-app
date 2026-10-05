"""utils/limit_solver.py — ลิมิตเข้าใกล้จุด

skeleton สำหรับนักศึกษา project
TODO: ใส่ logic จริงให้ test ใน tests/ ผ่าน
อ้างอิง blueprint: utils/riemann_solver.py และ docs/interactive-lessons-plan.md

โครงสร้างผลลัพธ์ (เหมือน utils/riemann_solver.py):
  {
      "ok": bool,
      "result": float | None,
      "latex": str,          # สูตรผลลัพธ์ LaTeX
      "steps": list[str],    # ขั้นตอน LaTeX
      "expr": sympy.Expr,    # นิพจน์ที่ parse แล้ว
      "error": str | None,
  }
"""
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

X = sp.Symbol("x")


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


def _parse_input(expr_str: str) -> sp.Expr:
    clean = (expr_str or "").strip()
    if not clean:
        raise ValueError("Empty input string")
    return parse_expr(clean, transformations=TRANSFORMATIONS, local_dict=LOCAL_MATH_DICT)


def compute_limit_near(expr_str: str, a: float) -> dict:
    """คำนวณลิมิตสองด้าน x -> a และแสดงขั้นตอน"""
    try:
        expr = _parse_input(expr_str)
        try:
            lim_left = sp.limit(expr, X, a, dir="-")
            lim_right = sp.limit(expr, X, a, dir="+")
            status = _classify_limit(lim_left, lim_right)
        except Exception:
            lim_left, lim_right = None, None
            status = "unsupported"

        steps = [
            f"กำหนดโจทย์ลิมิตที่ต้องการหา: \\lim_{{x \\to {a}}} \\left({sp.latex(expr)}\\right)",
            f"พิจารณาลิมิตทางซ้าย (Left-hand limit): \\lim_{{x \\to {a}^-}} \\left({sp.latex(expr)}\\right) = {sp.latex(lim_left)}",
            f"พิจารณาลิมิตทางขวา (Right-hand limit): \\lim_{{x \\to {a}^+}} \\left({sp.latex(expr)}\\right) = {sp.latex(lim_right)}",
        ]

        if status == "finite":
            lim_val = sp.limit(expr, X, a)
            steps.append(
                f"เปรียบเทียบและสรุปค่าลิมิตสองด้าน: \\lim_{{x \\to {a}^-}} f(x) = \\lim_{{x \\to {a}^+}} f(x) = {sp.latex(lim_val)} \\implies \\lim_{{x \\to {a}}} \\left({sp.latex(expr)}\\right) = {sp.latex(lim_val)}"
            )
            result = float(lim_val) if lim_val.is_number and lim_val.is_real else None
            latex_str = f"\\lim_{{x \\to {a}}} {sp.latex(expr)} = {sp.latex(lim_val)}"
        elif status == "infinite":
            lim_val = lim_left
            steps.append(
                f"สรุปผล (ทั้งสองข้างลู่ไปอนันต์ค่าเดียวกัน): \\lim_{{x \\to {a}}} \\left({sp.latex(expr)}\\right) = {sp.latex(lim_val)}"
            )
            result = None
            latex_str = f"\\lim_{{x \\to {a}}} {sp.latex(expr)} = {sp.latex(lim_val)}"
        elif status == "dne":
            steps.append(
                f"สรุปผล (ลิมิตซ้ายไม่เท่ากับลิมิตขวา จึงไม่มีลิมิตสองด้าน): \\lim_{{x \\to {a}^-}} f(x) = {sp.latex(lim_left)} \\neq \\lim_{{x \\to {a}^+}} f(x) = {sp.latex(lim_right)}"
            )
            result = None
            latex_str = f"\\lim_{{x \\to {a}}} {sp.latex(expr)} \\quad \\text{{(does not exist)}}"
        else:
            steps.append(
                "ไม่สามารถสรุปค่าลิมิตสองด้านได้จากข้อมูลการคำนวณในระบบ"
            )
            result = None
            latex_str = f"\\lim_{{x \\to {a}}} {sp.latex(expr)} \\quad \\text{{(unsupported)}}"

        return {
            "ok": True,
            "result": result,
            "latex": latex_str,
            "steps": steps,
            "expr": expr,
            "error": None,
            "status": status,
            "left_limit": lim_left,
            "right_limit": lim_right,
        }
    except Exception as e:
        return {
            "ok": False,
            "result": None,
            "latex": "",
            "steps": [],
            "expr": None,
            "error": f"ไม่สามารถคำนวณได้: {e}",
            "status": "error",
            "left_limit": None,
            "right_limit": None,
        }
