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


def compute_area_between(f_str: str, g_str: str, a: float, b: float) -> dict:
    """หาจุดตัด f(x)=g(x) แล้วคำนวณ A = ∫(f-g)dx"""
    try:
        f_expr = _parse_input(f_str)
        g_expr = _parse_input(g_str)
        diff_expr = f_expr - g_expr
        area_val = sp.integrate(diff_expr, (X, a, b))

        steps = [
            f"กำหนดฟังก์ชันขอบเขตบนและล่าง: f(x) = {sp.latex(f_expr)}, \\quad g(x) = {sp.latex(g_expr)}",
            f"ตั้งสูตรอินทิกรัลพื้นที่ระหว่างเส้นโค้ง: A = \\int_{{{a}}}^{{{b}}} [f(x) - g(x)] \\, dx",
            f"แทนค่าฟังก์ชันและหาผลต่าง: A = \\int_{{{a}}}^{{{b}}} \\left[{sp.latex(f_expr)} - \\left({sp.latex(g_expr)}\\right)\\right] \\, dx = \\int_{{{a}}}^{{{b}}} \\left({sp.latex(diff_expr)}\\right) \\, dx",
            f"คำนวณพื้นที่ปิดล้อมสุทธิ: A = {sp.latex(area_val)}",
        ]
        return {
            "ok": True,
            "result": float(area_val) if area_val.is_number and area_val.is_real else None,
            "latex": f"A = \\int_{{{a}}}^{{{b}}} [{sp.latex(diff_expr)}] \\, dx = {sp.latex(area_val)}",
            "steps": steps,
            "expr": diff_expr,
            "f_expr": f_expr,
            "g_expr": g_expr,
            "error": None,
        }
    except Exception as e:
        return {
            "ok": False,
            "result": None,
            "latex": "",
            "steps": [],
            "expr": None,
            "f_expr": None,
            "g_expr": None,
            "error": f"ไม่สามารถคำนวณได้: {e}",
        }
