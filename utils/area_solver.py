"""utils/area_solver.py — พื้นที่ระหว่างเส้นโค้ง

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


def compute_area_between(f_str: str, g_str: str, a: float, b: float) -> dict:
    """หาจุดตัด f(x)=g(x) แล้วคำนวณ A = ∫(f-g)dx

    Args:
        f_str: เส้นโค้งบน, g_str: เส้นโค้งล่าง, a, b

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
