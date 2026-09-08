"""utils/improper_solver.py — อินทิกรัลไม่แท้

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


def compute_improper(expr_str: str, a: float, b: float | None = None) -> dict:
    """คำนวณอินทิกรัลไม่ตรงแบบผ่านลิมิต ตรวจลู่เข้า/ลู่ออก"""
    try:
        expr = _parse_input(expr_str)
        upper = sp.oo if b is None else b
        res_val = sp.integrate(expr, (X, a, upper))

        steps = [
            f"กำหนดอินทิกรัลไม่ตรงแบบ: \\int_{{{a}}}^{{\\infty}} {sp.latex(expr)} \\, dx",
            f"แปลงเป็นลิมิต: \\lim_{{t \\to \\infty}} \\int_{{{a}}}^{{t}} {sp.latex(expr)} \\, dx",
            f"คำนวณผลลัพธ์ลิมิต: {sp.latex(res_val)}",
        ]
        return {
            "ok": True,
            "result": float(res_val) if res_val.is_number and res_val.is_real else None,
            "latex": f"\\int_{{{a}}}^{{\\infty}} {sp.latex(expr)} \\, dx = {sp.latex(res_val)}",
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
