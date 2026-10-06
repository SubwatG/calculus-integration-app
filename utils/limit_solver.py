"""utils/limit_solver.py — ลิมิตเข้าใกล้จุด

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


def _classify_limit(left: sp.Expr, right: sp.Expr) -> str:
    if isinstance(left, AccumulationBounds) or isinstance(right, AccumulationBounds):
        return "dne"
    if getattr(left, "is_extended_real", None) is not True or getattr(right, "is_extended_real", None) is not True:
        return "unsupported"
    if left == right:
        return "infinite" if left in (sp.oo, -sp.oo) else "finite"
    if getattr(left, "is_number", False) is True and getattr(right, "is_number", False) is True:
        return "dne"
    return "unsupported"


def _parse_input(expr_str: str) -> sp.Expr:
    clean = (expr_str or "").strip()
    if not clean:
        raise ValueError("Empty input string")
    return parse_expr(clean, transformations=TRANSFORMATIONS, local_dict=LOCAL_MATH_DICT)


def _check_real_domain(expr: sp.Expr, a: float, delta: float = 0.01) -> tuple[bool, bool]:
    """ตรวจสอบว่าฟังก์ชันนิยามบนระบบจำนวนจริงทางซ้าย a - delta และทางขวา a + delta หรือไม่"""
    left_sample = a - delta
    right_sample = a + delta

    try:
        val_l = expr.subs(X, left_sample)
        im_l = float(sp.im(val_l.evalf()))
        re_l = float(sp.re(val_l.evalf()))
        left_real = abs(im_l) < 1e-9 and math.isfinite(re_l)
    except Exception:
        left_real = False

    try:
        val_r = expr.subs(X, right_sample)
        im_r = float(sp.im(val_r.evalf()))
        re_r = float(sp.re(val_r.evalf()))
        right_real = abs(im_r) < 1e-9 and math.isfinite(re_r)
    except Exception:
        right_real = False

    return left_real, right_real


def compute_limit_near(expr_str: str, a: float) -> dict:
    """คำนวณลิมิตสองด้าน x -> a และแสดงขั้นตอน พร้อมตรวจจับขอบเขตโดเมนด้านเดียวและการแกว่งกวัด"""
    try:
        expr = _parse_input(expr_str)
        left_real, right_real = _check_real_domain(expr, a)

        try:
            lim_left = sp.limit(expr, X, a, dir="-")
            lim_right = sp.limit(expr, X, a, dir="+")
            status = _classify_limit(lim_left, lim_right)
        except Exception:
            lim_left, lim_right = None, None
            status = "unsupported"

        # ตรวจสอบว่าโดเมนจำนวนจริงมีเพียงฝั่งเดียวหรือไม่ (One-sided Domain Boundary)
        if not left_real and right_real:
            status = "right_only"
        elif left_real and not right_real:
            status = "left_only"

        # ตรวจสอบการแกว่งกวัดความถี่สูง (Oscillating) เช่น sin(1/x)
        is_oscillating = isinstance(lim_left, AccumulationBounds) or isinstance(lim_right, AccumulationBounds)

        steps = [
            f"กำหนดโจทย์ลิมิตที่ต้องการหา: \\lim_{{x \\to {a}}} \\left({sp.latex(expr)}\\right)",
        ]

        if status == "right_only":
            steps.append(
                f"ข้อสังเกตโดเมน: ฟังก์ชันไม่นิยามบนระบบจำนวนจริงทางซ้ายของ $x = {a}$ (เช่น รากที่สองหรือลอการิทึม) จึงพิจารณาเฉพาะลิมิตทางขวา (Right-hand Limit) เท่านั้น"
            )
            steps.append(
                f"พิจารณาลิมิตทางขวา: \\lim_{{x \\to {a}^+}} \\left({sp.latex(expr)}\\right) = {sp.latex(lim_right)}"
            )
            if getattr(lim_right, "is_finite", False) and getattr(lim_right, "is_real", False):
                result = float(lim_right)
                latex_str = f"\\lim_{{x \\to {a}^+}} {sp.latex(expr)} = {sp.latex(lim_right)}"
            else:
                result = None
                latex_str = f"\\lim_{{x \\to {a}^+}} {sp.latex(expr)} = {sp.latex(lim_right)}"
        elif status == "left_only":
            steps.append(
                f"ข้อสังเกตโดเมน: ฟังก์ชันไม่นิยามบนระบบจำนวนจริงทางขวาของ $x = {a}$ จึงพิจารณาเฉพาะลิมิตทางซ้าย (Left-hand Limit) เท่านั้น"
            )
            steps.append(
                f"พิจารณาลิมิตทางซ้าย: \\lim_{{x \\to {a}^-}} \\left({sp.latex(expr)}\\right) = {sp.latex(lim_left)}"
            )
            if getattr(lim_left, "is_finite", False) and getattr(lim_left, "is_real", False):
                result = float(lim_left)
                latex_str = f"\\lim_{{x \\to {a}^-}} {sp.latex(expr)} = {sp.latex(lim_left)}"
            else:
                result = None
                latex_str = f"\\lim_{{x \\to {a}^-}} {sp.latex(expr)} = {sp.latex(lim_left)}"
        else:
            steps.append(
                f"พิจารณาลิมิตทางซ้าย (Left-hand limit): \\lim_{{x \\to {a}^-}} \\left({sp.latex(expr)}\\right) = {sp.latex(lim_left)}"
            )
            steps.append(
                f"พิจารณาลิมิตทางขวา (Right-hand limit): \\lim_{{x \\to {a}^+}} \\left({sp.latex(expr)}\\right) = {sp.latex(lim_right)}"
            )

            if is_oscillating:
                steps.append(
                    f"ข้อสังเกตเชิงมโนทัศน์: ฟังก์ชันมีการแกว่งกวัดไม่สิ้นสุด (Oscillating Singularity) ในช่วง $\\langle -1, 1\\rangle$ เมื่อเข้าใกล้จุด $x = {a}$ ค่าจึงไม่ลู่เข้าหาจำนวนจริงใดจำนวนหนึ่ง"
                )
                steps.append(
                    f"สรุปผล (ไม่มีลิมิตเนื่องจากการแกว่งกวัด): \\lim_{{x \\to {a}}} \\left({sp.latex(expr)}\\right) \\quad \\text{{(does not exist)}}"
                )
                result = None
                latex_str = f"\\lim_{{x \\to {a}}} {sp.latex(expr)} \\quad \\text{{(does not exist)}}"
            elif status == "finite":
                lim_val = sp.limit(expr, X, a)
                steps.append(
                    f"เปรียบเทียบและสรุปค่าลิมิตสองด้าน: \\lim_{{x \\to {a}^-}} f(x) = \\lim_{{x \\to {a}^+}} f(x) = {sp.latex(lim_val)} \\implies \\lim_{{x \\to {a}}} \\left({sp.latex(expr)}\\right) = {sp.latex(lim_val)}"
                )
                result = float(lim_val) if lim_val.is_number and lim_val.is_real else None
                latex_str = f"\\lim_{{x \\to {a}}} {sp.latex(expr)} = {sp.latex(lim_val)}"
            elif status == "infinite":
                lim_val = lim_left
                steps.append(
                    f"สรุปผล (ทั้งสองข้างลู่ไปอนันต์ค่าเดียวกัน): \\lim_{{x \\to {a}}} \\left({sp.latex(expr)}\\right) = {sp.latex(lim_val)}"
                )
                result = None
                latex_str = f"\\lim_{{x \\to {a}}} {sp.latex(expr)} = {sp.latex(lim_val)}"
            elif status == "dne":
                steps.append(
                    f"สรุปผล (ลิมิตซ้ายไม่เท่ากับลิมิตขวา จึงไม่มีลิมิตสองด้าน): \\lim_{{x \\to {a}^-}} f(x) = {sp.latex(lim_left)} \\neq \\lim_{{x \\to {a}^+}} f(x) = {sp.latex(lim_right)}"
                )
                result = None
                latex_str = f"\\lim_{{x \\to {a}}} {sp.latex(expr)} \\quad \\text{{(does not exist)}}"
            else:
                steps.append(
                    "ไม่สามารถสรุปค่าลิมิตสองด้านได้จากข้อมูลการคำนวณในระบบ"
                )
                result = None
                latex_str = f"\\lim_{{x \\to {a}}} {sp.latex(expr)} \\quad \\text{{(unsupported)}}"

        return {
            "ok": True,
            "result": result,
            "latex": latex_str,
            "steps": steps,
            "expr": expr,
            "error": None,
            "status": status,
            "left_limit": lim_left,
            "right_limit": lim_right,
            "is_oscillating": is_oscillating,
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
            "left_limit": None,
            "right_limit": None,
        }
