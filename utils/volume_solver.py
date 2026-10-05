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


def compute_volume(expr_str: str, a: float, b: float, method: str = 'disk') -> dict:
    """คำนวณปริมาตรแบบ disk: V = pi*∫(R²)dx"""
    try:
        a_f, b_f = float(a), float(b)
        if b_f <= a_f:
            raise ValueError("ขอบล่าง a ต้องน้อยกว่าขอบบน b")
        if method.lower() != 'disk':
            raise ValueError(f"วิธี '{method}' ยังไม่รองรับในเวอร์ชันปัจจุบัน (รองรับเฉพาะ 'disk')")
        expr = _parse_input(expr_str)
        vol_val = sp.pi * sp.integrate(expr**2, (X, a_f, b_f))
        if vol_val.has(sp.Integral) or not (getattr(vol_val, "is_real", False) and getattr(vol_val, "is_finite", False)):
            raise ValueError("ไม่สามารถคำนวณปริมาตรจำกัดได้บนช่วงที่กำหนด")

        steps = [
            f"ฟังก์ชันรัศมี: R(x) = {sp.latex(expr)} บนช่วง [{a}, {b}]",
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
