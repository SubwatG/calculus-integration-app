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


def _parse_input(expr_str: str) -> sp.Expr:
    clean = (expr_str or "").strip()
    if not clean:
        raise ValueError("Empty input string")
    return parse_expr(clean, transformations=TRANSFORMATIONS, local_dict=LOCAL_MATH_DICT)


def compute_tangent(expr_str: str, a: float) -> dict:
    """คำนวณความชันเส้นสัมผัส f'(a) และสมการเส้นสัมผัส y = f'(a)(x-a) + f(a)"""
    try:
        expr = _parse_input(expr_str)
        df = sp.diff(expr, X)
        fa = expr.subs(X, a)
        slope = df.subs(X, a)
        tangent_eq = slope * (X - a) + fa

        steps = [
            f"กำหนดฟังก์ชันและจุดที่พิจารณา: f(x) = {sp.latex(expr)}, \\quad a = {a}",
            f"คำนวณพิกัด y ของจุดสัมผัส: f({a}) = {sp.latex(fa)} \\implies (x_0, y_0) = ({a}, {sp.latex(fa)})",
            f"หาอนุพันธ์เพื่อหาความชันของฟังก์ชัน: f'(x) = \\frac{{d}}{{dx}}\\left[{sp.latex(expr)}\\right] = {sp.latex(df)}",
            f"แทนค่าจุด a เพื่อหาความชันเส้นสัมผัส m: m = f'({a}) = {sp.latex(slope)}",
            f"แทนค่าในสูตรสมการเส้นสัมผัส y - y_0 = m(x - x_0): y - ({sp.latex(fa)}) = {sp.latex(slope)}(x - {a})",
            f"จัดรูปสมการเส้นสัมผัสในรูปชัดแจ้ง: y = {sp.latex(sp.simplify(tangent_eq))}",
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
