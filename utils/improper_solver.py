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
import math
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


def _parse_input(expr_str: str) -> sp.Expr:
    clean = (expr_str or "").strip()
    if not clean:
        raise ValueError("Empty input string")
    return parse_expr(clean, transformations=TRANSFORMATIONS, local_dict=LOCAL_MATH_DICT)


def _classify_improper(res_val: sp.Expr) -> str:
    """Improper-integral status: finite, divergent, unsupported, error."""
    if isinstance(res_val, sp.Integral):
        return "unsupported"
    if res_val is sp.nan or res_val.has(sp.zoo, sp.nan):
        return "divergent"
    if isinstance(res_val, AccumulationBounds):
        return "divergent"
    if res_val.has(sp.oo, -sp.oo):
        return "divergent"
    if getattr(res_val, "is_finite", False) is True and getattr(res_val, "is_real", False) is True:
        return "finite"
    return "unsupported"


def compute_improper(expr_str: str, a: float, b: float | None = None) -> dict:
    """คำนวณอินทิกรัลไม่ตรงแบบผ่านลิมิต ตรวจลู่เข้า/ลู่ออก"""
    try:
        expr = _parse_input(expr_str)

        f_a = float(a)
        if not math.isfinite(f_a):
            raise ValueError(f"ขอบล่าง a ต้องเป็นจำนวนจริงจำกัด: {a}")
        a_sp = sp.nsimplify(a)

        if b is None:
            upper = sp.oo
            bound_latex = "\\infty"
        else:
            f_b = float(b)
            if not math.isfinite(f_b):
                raise ValueError(f"ขอบบน b ต้องเป็นจำนวนจริงจำกัดหรืออนันต์: {b}")
            if f_a >= f_b:
                raise ValueError("ขอบล่าง a ต้องน้อยกว่าขอบบน b")
            upper = sp.nsimplify(b)
            bound_latex = sp.latex(upper)

        lower_latex = sp.latex(a_sp)
        res_val = sp.integrate(expr, (X, a_sp, upper))
        status = _classify_improper(res_val)

        if status == "finite":
            result = float(res_val) if res_val.is_real else None
            value_latex = sp.latex(res_val)
        elif status == "divergent":
            result = None
            value_latex = "\\text{diverges}"
        else:
            result = None
            value_latex = "\\text{unsupported}"

        steps = [
            f"กำหนดอินทิกรัลไม่ตรงแบบ: \\int_{{{lower_latex}}}^{{{bound_latex}}} \\left({sp.latex(expr)}\\right) \\, dx",
            f"แปลงเป็นรูปลิมิตของอินทิกรัลจำกัดเขต: \\lim_{{t \\to {bound_latex}}} \\int_{{{lower_latex}}}^{{t}} \\left({sp.latex(expr)}\\right) \\, dx",
        ]
        if status == "finite":
            steps.append(
                f"คำนวณผลลัพธ์ลิมิต (ลู่เข้าสู่ค่าจริงจำกัด): \\int_{{{lower_latex}}}^{{{bound_latex}}} \\left({sp.latex(expr)}\\right) \\, dx = {value_latex}"
            )
        elif status == "divergent":
            steps.append(
                f"คำนวณผลลัพธ์ลิมิต (ปริพันธ์ลู่ออก / ไม่ลู่เข้าสู่ค่าจำกัด): \\int_{{{lower_latex}}}^{{{bound_latex}}} \\left({sp.latex(expr)}\\right) \\, dx = {value_latex}"
            )
        else:
            steps.append(
                f"คำนวณผลลัพธ์ลิมิต: \\int_{{{lower_latex}}}^{{{bound_latex}}} \\left({sp.latex(expr)}\\right) \\, dx = {value_latex}"
            )

        return {
            "ok": True,
            "result": result,
            "latex": f"\\int_{{{lower_latex}}}^{{{bound_latex}}} {sp.latex(expr)} \\, dx = {value_latex}",
            "steps": steps,
            "expr": expr,
            "error": None,
            "status": status,
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
        }
