"""utils/volume_solver.py — ปริมาตรของทรงตัน

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


def compute_volume(expr_str: str, a: float, b: float, method: str = 'disk') -> dict:
    """คำนวณปริมาตรแบบ disk หรือ washer: V = pi*∫(R²-r²)dx"""
    try:
        expr = _parse_input(expr_str)
        vol_val = sp.pi * sp.integrate(expr**2, (X, a, b))

        steps = [
            f"ฟังก์ชันรัศมี: r(x) = {sp.latex(expr)} บนช่วง [{a}, {b}]",
            f"สูตรวิธีจาน (Disk Method): V = \\pi \\int_{{{a}}}^{{{b}}} [{sp.latex(expr)}]^2 \\, dx",
            f"คำนวณปริมาตรทรงตัน: V = {sp.latex(vol_val)}",
        ]
        return {
            "ok": True,
            "result": float(vol_val) if vol_val.is_number and vol_val.is_real else None,
            "latex": f"V = \\pi \\int_{{{a}}}^{{{b}}} [{sp.latex(expr)}]^2 \\, dx = {sp.latex(vol_val)}",
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
