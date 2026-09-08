"""utils/tangent_solver.py — เส้นสัมผัสและอนุพันธ์

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


def compute_tangent(expr_str: str, a: float) -> dict:
    """คำนวณความชันเส้นสัมผัส f'(a) และสมการเส้นสัมผัส y = f'(a)(x-a) + f(a)"""
    try:
        expr = _parse_input(expr_str)
        df = sp.diff(expr, X)
        fa = expr.subs(X, a)
        slope = df.subs(X, a)
        tangent_eq = slope * (X - a) + fa

        steps = [
            f"กำหนดฟังก์ชัน: f(x) = {sp.latex(expr)} ที่จุด a = {a}",
            f"หาอนุพันธ์: f'(x) = {sp.latex(df)}",
            f"คำนวณความชัน: m = f'({a}) = {sp.latex(slope)}",
            f"สมการเส้นสัมผัส: y = {sp.latex(sp.simplify(tangent_eq))}",
        ]
        return {
            "ok": True,
            "result": float(slope) if slope.is_number and slope.is_real else None,
            "latex": f"y = {sp.latex(sp.simplify(tangent_eq))}",
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
