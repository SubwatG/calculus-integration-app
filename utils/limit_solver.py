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
from sympy.parsing.sympy_parser import (
    implicit_multiplication_application,
    parse_expr,
    standard_transformations,
)

TRANSFORMATIONS = standard_transformations + (
    implicit_multiplication_application,
)

X = sp.Symbol("x")


def _parse_input(expr_str: str) -> sp.Expr:
    clean = (expr_str or "").strip()
    if not clean:
        raise ValueError("Empty input string")
    return parse_expr(clean, transformations=TRANSFORMATIONS)


def compute_limit_near(expr_str: str, a: float) -> dict:
    """คำนวณลิมิตสองด้าน x -> a และแสดงขั้นตอน"""
    try:
        expr = _parse_input(expr_str)
        lim_val = sp.limit(expr, X, a)
        lim_left = sp.limit(expr, X, a, dir="-")
        lim_right = sp.limit(expr, X, a, dir="+")

        steps = [
            f"กำหนดโจทย์: \\lim_{{x \\to {a}}} {sp.latex(expr)}",
            f"พิจารณาลิมิตทางซ้าย: \\lim_{{x \\to {a}^-}} {sp.latex(expr)} = {sp.latex(lim_left)}",
            f"พิจารณาลิมิตทางขวา: \\lim_{{x \\to {a}^+}} {sp.latex(expr)} = {sp.latex(lim_right)}",
            f"สรุปค่าลิมิตสองด้าน: \\lim_{{x \\to {a}}} {sp.latex(expr)} = {sp.latex(lim_val)}",
        ]
        return {
            "ok": True,
            "result": float(lim_val) if lim_val.is_number and lim_val.is_real else None,
            "latex": f"\\lim_{{x \\to {a}}} {sp.latex(expr)} = {sp.latex(lim_val)}",
            "steps": steps,
            "expr": expr,
            "error": None,
        }
    except Exception as e:
        return {
            "ok": False,
            "result": None,
            "latex": "",
            "steps": [],
            "expr": None,
            "error": f"ไม่สามารถคำนวณได้: {e}",
        }
