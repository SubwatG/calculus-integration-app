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
    """คำนวณปริมาตรแบบ disk หรือ washer: V = pi*∫(R²-r²)dx

    Args:
        expr_str: ฟังก์ชันรัศมี R(x) (และ r(x) สำหรับ washer), a, b, method

    TODO: implement ให้ครบตาม blueprint ของ riemann_solver
    """
    try:
        # TODO: ใส่ logic การคำนวณจริงที่นี่
        raise NotImplementedError("ยังไม่ implement ให้นักศึกษาเติม")
    except Exception as e:
        return {
            "ok": False,
            "result": None,
            "latex": "",
            "steps": [],
            "expr": None,
            "error": f"ยังไม่พร้อมใช้งาน: {e}",
        }
