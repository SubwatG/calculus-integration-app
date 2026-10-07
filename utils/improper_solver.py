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


def _find_interior_singularities(expr: sp.Expr, a_val: float, b_val: float) -> list[float]:
    """ค้นหาจุดเอกฐานภายในช่วงเปิด (a, b) จากรากของตัวส่วน"""
    sings = []
    denom = sp.denom(expr)
    if denom != 1:
        try:
            sol = sp.solve(denom, X)
            for s in sol:
                if getattr(s, "is_real", False) and a_val < float(s) < b_val:
                    s_f = float(s)
                    if not any(abs(s_f - ex) < 1e-4 for ex in sings):
                        sings.append(s_f)
        except Exception:
            pass
    return sorted(sings)


def _format_bound_latex(val: float | int | sp.Expr) -> str:
    """จัดรูปแบบขอบเขตบน/ล่าง: ถ้าเป็นจำนวนเต็มแสดงจำนวนเต็ม (เช่น 1, 2) ถ้าเป็นทศนิยมแสดงทศนิยม (เช่น 2.03 แทน 203/100)"""
    try:
        f = float(val)
        if f.is_integer():
            return str(int(f))
        return f"{f:g}"
    except Exception:
        return sp.latex(val)


def compute_improper(expr_str: str, a: float, b: float | None = None) -> dict:
    """คำนวณอินทิกรัลไม่ตรงแบบผ่านลิมิต ตรวจลู่เข้า/ลู่ออก และแจกแจงจุดเอกฐานภายในช่วง"""
    try:
        expr = _parse_input(expr_str)

        f_a = float(a)
        if not math.isfinite(f_a):
            raise ValueError(f"ขอบล่าง a ต้องเป็นจำนวนจริงจำกัด: {a}")
        a_sp = sp.nsimplify(a)

        if b is None:
            upper = sp.oo
            bound_latex = "\\infty"
            f_b = float("inf")
        else:
            f_b = float(b)
            if not math.isfinite(f_b):
                raise ValueError(f"ขอบบน b ต้องเป็นจำนวนจริงจำกัดหรืออนันต์: {b}")
            if f_a >= f_b:
                raise ValueError("ขอบล่าง a ต้องน้อยกว่าขอบบน b")
            upper = sp.nsimplify(b)
            bound_latex = _format_bound_latex(b)

        lower_latex = _format_bound_latex(a)

        # ตรวจสอบจุดเอกฐานภายในช่วง (Interior Singularities)
        interior_sings = []
        if math.isfinite(f_b):
            interior_sings = _find_interior_singularities(expr, f_a, f_b)

        steps = [
            f"กำหนดอินทิกรัลไม่ตรงแบบ: \\int_{{{lower_latex}}}^{{{bound_latex}}} \\left({sp.latex(expr)}\\right) \\, dx",
        ]

        if interior_sings:
            c_val = interior_sings[0]
            c_sp = sp.nsimplify(c_val)
            c_latex = sp.latex(c_sp)
            steps.append(
                f"พบจุดเอกฐานภายในช่วงอินทิเกรต (Interior Singularity) ที่ $x = {c_latex}$ ซึ่งฟังก์ชันไม่ต่อเนื่องและไม่มีขอบเขต"
            )
            steps.append(
                f"แยกช่วงการอินทิเกรตออกเป็นสองตอนตามนิยาม: \\int_{{{lower_latex}}}^{{{bound_latex}}} f(x)\\,dx = \\lim_{{t \\to {c_latex}^-}} \\int_{{{lower_latex}}}^{{t}} f(x)\\,dx + \\lim_{{s \\to {c_latex}^+}} \\int_{{s}}^{{{bound_latex}}} f(x)\\,dx"
            )

            # คำนวณแต่ละฝั่ง
            left_part = sp.integrate(expr, (X, a_sp, c_sp))
            right_part = sp.integrate(expr, (X, c_sp, upper))
            left_status = _classify_improper(left_part)
            right_status = _classify_improper(right_part)

            if left_status == "divergent" or right_status == "divergent":
                status = "divergent"
                result = None
                value_latex = "\\text{diverges}"
                steps.append(
                    f"พิจารณาแต่ละฝั่ง: ฝั่งซ้ายสถานะเป็น {left_status} และฝั่งขวาเป็น {right_status}"
                )
                steps.append(
                    "ตามนิยามทางคณิตศาสตร์ หากมีส่วนย่อยอย่างน้อย 1 ฝั่งลู่ออก อินทิกรัลไม่ตรงแบบทั้งหมดจะถือว่า **ลู่ออก (Diverges)** (ไม่สามารถนำ $\\pm\\infty$ มาหักล้างกันได้)"
                )
            elif left_status == "finite" and right_status == "finite":
                res_val = left_part + right_part
                status = "finite"
                result = float(res_val) if res_val.is_real else None
                value_latex = sp.latex(res_val)
                steps.append(
                    f"ทั้งสองฝั่งลู่เข้าสู่ค่าจริงจำกัด: \\int_{{{lower_latex}}}^{{{bound_latex}}} f(x)\\,dx = {value_latex}"
                )
            else:
                status = "unsupported"
                result = None
                value_latex = "\\text{unsupported}"
        else:
            if math.isfinite(f_b):
                steps.append(
                    f"แปลงเป็นรูปลิมิตของอินทิกรัลจำกัดเขต: \\lim_{{t \\to {bound_latex}}} \\int_{{{lower_latex}}}^{{t}} \\left({sp.latex(expr)}\\right) \\, dx"
                )
            else:
                steps.append(
                    f"แปลงเป็นรูปลิมิตของอินทิกรัลจำกัดเขตบนช่วงอนันต์: \\lim_{{t \\to \\infty}} \\int_{{{lower_latex}}}^{{t}} \\left({sp.latex(expr)}\\right) \\, dx"
                )

            res_val = sp.integrate(expr, (X, a_sp, upper))
            status = _classify_improper(res_val)

            if status == "finite":
                result = float(res_val) if res_val.is_real else None
                value_latex = sp.latex(res_val)
                steps.append(
                    f"คำนวณผลลัพธ์ลิมิต (ลู่เข้าสู่ค่าจริงจำกัด): \\int_{{{lower_latex}}}^{{{bound_latex}}} \\left({sp.latex(expr)}\\right) \\, dx = {value_latex}"
                )
            elif status == "divergent":
                result = None
                value_latex = "\\text{diverges}"
                steps.append(
                    f"คำนวณผลลัพธ์ลิมิต (ปริพันธ์ลู่ออก / ไม่ลู่เข้าสู่ค่าจำกัด): \\int_{{{lower_latex}}}^{{{bound_latex}}} \\left({sp.latex(expr)}\\right) \\, dx = {value_latex}"
                )
            else:
                result = None
                value_latex = "\\text{unsupported}"
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
            "interior_singularities": interior_sings,
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
