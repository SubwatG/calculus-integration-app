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


def _format_point_str(a: float) -> str:
    """แปลงจุด a เป็นสตริงที่อ่านง่าย เช่น 2 แทน 2.0"""
    if abs(a - round(a)) < 1e-6:
        return str(int(round(a)))
    return f"{a:g}"


def _format_samples(a: float) -> tuple[str, str]:
    """สร้างตัวอย่างค่า x ที่เข้าใกล้ a ทางซ้าย (x < a) และทางขวา (x > a) เพื่อให้เห็นภาพชัดเจน"""
    if abs(a - round(a)) < 1e-6:
        a_int = int(round(a))
        s_left = f"{a_int - 0.1:g}, {a_int - 0.01:g}, {a_int - 0.001:g}"
        s_right = f"{a_int + 0.1:g}, {a_int + 0.01:g}, {a_int + 0.001:g}"
    else:
        s_left = f"{a - 0.1:g}, {a - 0.01:g}, {a - 0.001:g}"
        s_right = f"{a + 0.1:g}, {a + 0.01:g}, {a + 0.001:g}"
    return s_left, s_right


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

        a_str = _format_point_str(a)
        s_left_ex, s_right_ex = _format_samples(a)

        steps = [
            f"กำหนดโจทย์ลิมิตที่ต้องการหา: ศึกษาพฤติกรรมของค่าฟังก์ชัน $f(x)$ เมื่อค่าตัวแปร $x$ ขยับเข้าใกล้จุด $x = {a_str}$ (โดยที่ $x \\neq {a_str}$)\n\\lim_{{x \\to {a_str}}} \\left({sp.latex(expr)}\\right)",
        ]

        if status == "right_only":
            steps.append(
                f"ข้อสังเกตโดเมน: ฟังก์ชันไม่นิยามบนระบบจำนวนจริงทางซ้ายของ $x = {a_str}$ (เช่น รากที่สองหรือลอการิทึม) จึงพิจารณาเฉพาะลิมิตทางขวา (Right-hand Limit) เท่านั้น"
            )
            steps.append(
                f"พิจารณาลิมิตทางขวา: สัญลักษณ์ $x \\to {a_str}^+$ หมายถึงให้ค่า $x$ ค่อย ๆ ขยับเข้าใกล้ {a_str} จากฝั่งขวาบนเส้นจำนวน (โดยที่ $x > {a_str}$ เช่น $x = {s_right_ex} \\dots$)\n\\lim_{{x \\to {a_str}^+}} \\left({sp.latex(expr)}\\right) = {sp.latex(lim_right)}"
            )
            if getattr(lim_right, "is_finite", False) and getattr(lim_right, "is_real", False):
                result = float(lim_right)
                latex_str = f"\\lim_{{x \\to {a_str}^+}} {sp.latex(expr)} = {sp.latex(lim_right)}"
            else:
                result = None
                latex_str = f"\\lim_{{x \\to {a_str}^+}} {sp.latex(expr)} = {sp.latex(lim_right)}"
        elif status == "left_only":
            steps.append(
                f"ข้อสังเกตโดเมน: ฟังก์ชันไม่นิยามบนระบบจำนวนจริงทางขวาของ $x = {a_str}$ จึงพิจารณาเฉพาะลิมิตทางซ้าย (Left-hand Limit) เท่านั้น"
            )
            steps.append(
                f"พิจารณาลิมิตทางซ้าย: สัญลักษณ์ $x \\to {a_str}^-$ หมายถึงให้ค่า $x$ ค่อย ๆ ขยับเข้าใกล้ {a_str} จากฝั่งซ้ายบนเส้นจำนวน (โดยที่ $x < {a_str}$ เช่น $x = {s_left_ex} \\dots$)\n\\lim_{{x \\to {a_str}^-}} \\left({sp.latex(expr)}\\right) = {sp.latex(lim_left)}"
            )
            if getattr(lim_left, "is_finite", False) and getattr(lim_left, "is_real", False):
                result = float(lim_left)
                latex_str = f"\\lim_{{x \\to {a_str}^-}} {sp.latex(expr)} = {sp.latex(lim_left)}"
            else:
                result = None
                latex_str = f"\\lim_{{x \\to {a_str}^-}} {sp.latex(expr)} = {sp.latex(lim_left)}"
        else:
            left_note = ""
            if lim_left == sp.oo:
                left_note = f"เมื่อ $x < {a_str}$ และเข้าใกล้ {a_str} มาก ๆ ค่า $f(x)$ จะมีค่าบวกเพิ่มขึ้นอย่างไม่มีขอบเขต พุ่งขึ้นสู่อนันต์ ($+\\infty$)"
            elif lim_left == -sp.oo:
                left_note = f"เมื่อ $x < {a_str}$ และเข้าใกล้ {a_str} มาก ๆ ตัวส่วนมีค่าน้อยมากฝั่งลบ ทำให้ค่า $f(x)$ ติดลบมหาศาล พุ่งลงสู่ลบอนันต์ ($-\\infty$)"
            elif lim_left is not None:
                left_note = f"เมื่อค่า $x$ ขยับเข้าใกล้ {a_str} ทางซ้าย ค่าของ $f(x)$ มีแนวโน้มลู่เข้าหาค่าคงที่ {sp.latex(lim_left)}"

            steps.append(
                f"พิจารณาลิมิตทางซ้าย (Left-hand limit): สัญลักษณ์ $x \\to {a_str}^-$ หมายถึงให้ค่า $x$ ค่อย ๆ ขยับเข้าใกล้ {a_str} จากฝั่งซ้ายของเส้นจำนวน (ค่าน้อยกว่า {a_str} เสมอ หรือ $x < {a_str}$ เช่น $x = {s_left_ex} \\dots$)\n{left_note}\n\\lim_{{x \\to {a_str}^-}} \\left({sp.latex(expr)}\\right) = {sp.latex(lim_left)}"
            )

            right_note = ""
            if lim_right == sp.oo:
                right_note = f"เมื่อ $x > {a_str}$ และเข้าใกล้ {a_str} มาก ๆ ค่า $f(x)$ จะมีค่าบวกเพิ่มขึ้นอย่างไม่มีขอบเขต พุ่งขึ้นสู่อนันต์ ($+\\infty$)"
            elif lim_right == -sp.oo:
                right_note = f"เมื่อ $x > {a_str}$ และเข้าใกล้ {a_str} มาก ๆ ตัวส่วนมีค่าน้อยมากฝั่งลบ ทำให้ค่า $f(x)$ ติดลบมหาศาล พุ่งลงสู่ลบอนันต์ ($-\\infty$)"
            elif lim_right is not None:
                right_note = f"เมื่อค่า $x$ ขยับเข้าใกล้ {a_str} ทางขวา ค่าของ $f(x)$ มีแนวโน้มลู่เข้าหาค่าคงที่ {sp.latex(lim_right)}"

            steps.append(
                f"พิจารณาลิมิตทางขวา (Right-hand limit): สัญลักษณ์ $x \\to {a_str}^+$ หมายถึงให้ค่า $x$ ค่อย ๆ ขยับเข้าใกล้ {a_str} จากฝั่งขวาของเส้นจำนวน (ค่ามากกว่า {a_str} เสมอ หรือ $x > {a_str}$ เช่น $x = {s_right_ex} \\dots$)\n{right_note}\n\\lim_{{x \\to {a_str}^+}} \\left({sp.latex(expr)}\\right) = {sp.latex(lim_right)}"
            )

            if is_oscillating:
                steps.append(
                    f"ข้อสังเกตเชิงมโนทัศน์: ฟังก์ชันมีการแกว่งกวัดไม่สิ้นสุด (Oscillating Singularity) ในช่วง $\\langle -1, 1\\rangle$ เมื่อเข้าใกล้จุด $x = {a_str}$ ค่าจึงไม่ลู่เข้าหาจำนวนจริงใดจำนวนหนึ่ง"
                )
                steps.append(
                    f"สรุปผล (ไม่มีลิมิตเนื่องจากการแกว่งกวัด): \\lim_{{x \\to {a_str}}} \\left({sp.latex(expr)}\\right) \\quad \\text{{(does not exist)}}"
                )
                result = None
                latex_str = f"\\lim_{{x \\to {a_str}}} {sp.latex(expr)} \\quad \\text{{(does not exist)}}"
            elif status == "finite":
                lim_val = sp.limit(expr, X, a)
                lim_val_latex = sp.latex(lim_val)
                steps.append(
                    f"เปรียบเทียบและสรุปค่าลิมิตสองด้าน: กฎพื้นฐานคือ ลิมิตสองด้านจะมีค่าได้ก็ต่อเมื่อ ลิมิตซ้ายและขวาต้องมุ่งสู่จำนวนจริงเดียวกัน\nเนื่องจาก $\\lim_{{x \\to {a_str}^-}} f(x) = \\lim_{{x \\to {a_str}^+}} f(x) = {lim_val_latex}$ (เส้นกราฟจากทั้งสองฝั่งวิ่งมาบรรจบกันที่ระดับความสูงเดียวกัน) จึงสรุปได้ว่ามีลิมิตสองด้าน\n\\lim_{{x \\to {a_str}^-}} f(x) = \\lim_{{x \\to {a_str}^+}} f(x) = {lim_val_latex} \\implies \\lim_{{x \\to {a_str}}} \\left({sp.latex(expr)}\\right) = {lim_val_latex}"
                )
                result = float(lim_val) if lim_val.is_number and lim_val.is_real else None
                latex_str = f"\\lim_{{x \\to {a_str}}} {sp.latex(expr)} = {sp.latex(lim_val)}"
            elif status == "infinite":
                lim_val = lim_left
                lim_val_latex = sp.latex(lim_val)
                steps.append(
                    f"สรุปผล (ทั้งสองข้างลู่ไปอนันต์ค่าเดียวกัน): เส้นกราฟทั้งฝั่งซ้ายและฝั่งขวาพุ่งไปสู่ค่าเดียวกันคือ ${lim_val_latex}$ แต่เนื่องจากอนันต์ไม่ใช่จำนวนจริงจำกัด ในทางคณิตศาสตร์จึงถือว่าลิมิตลู่ออก (Diverges)\n\\lim_{{x \\to {a_str}}} \\left({sp.latex(expr)}\\right) = {lim_val_latex}"
                )
                result = None
                latex_str = f"\\lim_{{x \\to {a_str}}} {sp.latex(expr)} = {sp.latex(lim_val)}"
            elif status == "dne":
                steps.append(
                    f"สรุปผล (ไม่มีลิมิตสองด้านเนื่องจากลิมิตซ้ายไม่เท่ากับลิมิตขวา): เส้นกราฟจากฝั่งซ้ายและฝั่งขวาแยกออกจากกันและไม่มาบรรจบกันที่จุดเดียวกัน\n\\lim_{{x \\to {a_str}^-}} f(x) = {sp.latex(lim_left)} \\neq \\lim_{{x \\to {a_str}^+}} f(x) = {sp.latex(lim_right)}\n\\lim_{{x \\to {a_str}}} \\left({sp.latex(expr)}\\right) \\quad \\text{{(does not exist)}}"
                )
                result = None
                latex_str = f"\\lim_{{x \\to {a_str}}} {sp.latex(expr)} \\quad \\text{{(does not exist)}}"
            else:
                steps.append(
                    "ไม่สามารถสรุปค่าลิมิตสองด้านได้จากข้อมูลการคำนวณในระบบ"
                )
                result = None
                latex_str = f"\\lim_{{x \\to {a_str}}} {sp.latex(expr)} \\quad \\text{{(unsupported)}}"

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
