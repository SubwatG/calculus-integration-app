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
    "inf": sp.oo,
    "infinity": sp.oo,
    "oo": sp.oo,
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


def _parse_bound(val: float | int | str | sp.Expr | None, is_upper: bool = False) -> sp.Expr:
    if val is None:
        return sp.oo if is_upper else -sp.oo
    if isinstance(val, (int, float)):
        return sp.Rational(str(val))
    if isinstance(val, sp.Expr):
        return val
    s = str(val).strip().lower().replace(" ", "")
    if s in ("inf", "+inf", "oo", "+oo", "infinity", "+infinity"):
        return sp.oo
    if s in ("-inf", "-oo", "-infinity"):
        return -sp.oo
    return parse_expr(str(val).strip(), transformations=TRANSFORMATIONS, local_dict=LOCAL_MATH_DICT)


def _format_bound_latex(val: float | int | str | sp.Expr | None) -> str:
    """จัดรูปแบบขอบเขตบน/ล่าง: ถ้าเป็นจำนวนเต็มแสดงจำนวนเต็ม ถ้าเป็นทศนิยมแสดงทศนิยม ถ้าเป็นสัญลักษณ์แสดง LaTeX"""
    if val is None or val == sp.oo:
        return "\\infty"
    if val == -sp.oo:
        return "-\\infty"
    try:
        f = float(val)
        if f.is_integer():
            return str(int(f))
        return f"{f:g}"
    except Exception:
        pass
    try:
        sp_v = sp.sympify(val)
        if sp_v == sp.oo:
            return "\\infty"
        if sp_v == -sp.oo:
            return "-\\infty"
        return sp.latex(sp_v)
    except Exception:
        return str(val)


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


def compute_improper(expr_str: str, a: float | int | str | sp.Expr = 0.0, b: float | int | str | sp.Expr | None = None) -> dict:
    """คำนวณอินทิกรัลไม่ตรงแบบผ่านลิมิต ตรวจลู่เข้า/ลู่ออก (รองรับช่วงกึ่งอนันต์, สองทาง (-oo, oo) และจุดเอกฐาน)"""
    try:
        expr = _parse_input(expr_str)

        lower = _parse_bound(a, is_upper=False)
        upper = _parse_bound(b, is_upper=True)

        lower_latex = _format_bound_latex(lower)
        bound_latex = _format_bound_latex(upper)

        steps = [
            f"กำหนดอินทิกรัลไม่ตรงแบบ: \\int_{{{lower_latex}}}^{{{bound_latex}}} \\left({sp.latex(expr)}\\right) \\, dx",
        ]

        interior_sings: list[float] = []

        # -------------------------------------------------------------
        # กรณีที่ 1: สองฝั่งเป็นอนันต์ (-oo, oo)
        # -------------------------------------------------------------
        if lower == -sp.oo and upper == sp.oo:
            # เลือกจุดแบ่ง c = 0 (หรือถ้า 0 เป็นจุดเอกฐานให้เลือก c = 1)
            c_val = 0
            denom = sp.denom(expr)
            if denom.subs(X, 0) == 0:
                c_val = 1

            steps.append(
                f"เนื่องจากขอบเขตอินทิเกรตเป็นอนันต์ทั้งสองฝั่ง $(-\\infty, \\infty)$ จึงแยกช่วงที่จุด $c = {c_val}$ ตามนิยาม:\n\\int_{{-\\infty}}^{{\\infty}} f(x)\\,dx = \\lim_{{s \\to -\\infty}} \\int_{{s}}^{{{c_val}}} f(x)\\,dx + \\lim_{{t \\to \\infty}} \\int_{{{c_val}}}^{{t}} f(x)\\,dx"
            )

            left_part = sp.integrate(expr, (X, -sp.oo, c_val))
            right_part = sp.integrate(expr, (X, c_val, sp.oo))
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
                    "ตามนิยามทางคณิตศาสตร์ หากมีส่วนย่อยอย่างน้อย 1 ฝั่งลู่ออก อินทิกรัลทั้งหมดจะถือว่า **ลู่ออก (Diverges)**"
                )
            elif left_status == "finite" and right_status == "finite":
                res_val = left_part + right_part
                status = "finite"
                result = float(res_val.evalf()) if getattr(res_val, "is_real", False) else None
                value_latex = sp.latex(res_val)
                steps.append(
                    f"ทั้งสองฝั่งลู่เข้าสู่ค่าจริงจำกัด:\n\\int_{{-\\infty}}^{{\\infty}} \\left({sp.latex(expr)}\\right) \\, dx = {value_latex}"
                )
            else:
                status = "unsupported"
                result = None
                value_latex = "\\text{unsupported}"

            int_sym = r"\int_{-\infty}^{\infty}"
            latex_str = f"{int_sym} {sp.latex(expr)} \\, dx = {value_latex}"
            return {
                "ok": True,
                "result": result,
                "latex": latex_str,
                "steps": steps,
                "expr": expr,
                "error": None,
                "status": status,
                "interior_singularities": [],
            }

        # -------------------------------------------------------------
        # กรณีที่ 2: ขอบล่างเป็น -oo และขอบบนจำกัด
        # -------------------------------------------------------------
        if lower == -sp.oo and upper != sp.oo:
            steps.append(
                f"แปลงเป็นรูปลิมิตของอินทิกรัลจำกัดเขตเมื่อขอบล่างเป็น $-\\infty$:\n\\lim_{{s \\to -\\infty}} \\int_{{s}}^{{{bound_latex}}} \\left({sp.latex(expr)}\\right) \\, dx"
            )
            res_val = sp.integrate(expr, (X, -sp.oo, upper))
            status = _classify_improper(res_val)
            if status == "finite":
                result = float(res_val.evalf()) if getattr(res_val, "is_real", False) else None
                value_latex = sp.latex(res_val)
                steps.append(f"อินทิกรัลลู่เข้าสู่ค่าจำกัด: {value_latex}")
            elif status == "divergent":
                result = None
                value_latex = "\\text{diverges}"
                steps.append("อินทิกรัลลู่ออก (Diverges) ไม่ลู่เข้าสู่ค่าจริงจำกัด")
            else:
                result = None
                value_latex = "\\text{unsupported}"

            latex_str = f"\\int_{{{lower_latex}}}^{{{bound_latex}}} {sp.latex(expr)} \\, dx = {value_latex}"
            return {
                "ok": True,
                "result": result,
                "latex": latex_str,
                "steps": steps,
                "expr": expr,
                "error": None,
                "status": status,
                "interior_singularities": [],
            }

        # -------------------------------------------------------------
        # กรณีที่ 3: ขอบล่างจำกัด และขอบบนเป็น oo
        # -------------------------------------------------------------
        if lower != -sp.oo and upper == sp.oo:
            steps.append(
                f"แปลงเป็นรูปลิมิตของอินทิกรัลจำกัดเขตบนช่วงอนันต์:\n\\lim_{{t \\to \\infty}} \\int_{{{lower_latex}}}^{{t}} \\left({sp.latex(expr)}\\right) \\, dx"
            )
            res_val = sp.integrate(expr, (X, lower, sp.oo))
            status = _classify_improper(res_val)
            if status == "finite":
                result = float(res_val.evalf()) if getattr(res_val, "is_real", False) else None
                value_latex = sp.latex(res_val)
                steps.append(f"อินทิกรัลลู่เข้าสู่ค่าจำกัด: {value_latex}")
            elif status == "divergent":
                result = None
                value_latex = "\\text{diverges}"
                steps.append("อินทิกรัลลู่ออก (Diverges) ไม่ลู่เข้าสู่ค่าจริงจำกัด")
            else:
                result = None
                value_latex = "\\text{unsupported}"

            latex_str = f"\\int_{{{lower_latex}}}^{{{bound_latex}}} {sp.latex(expr)} \\, dx = {value_latex}"
            return {
                "ok": True,
                "result": result,
                "latex": latex_str,
                "steps": steps,
                "expr": expr,
                "error": None,
                "status": status,
                "interior_singularities": [],
            }

        # -------------------------------------------------------------
        # กรณีที่ 4: ขอบล่างและขอบบนจำกัดทั้งคู่ (ตรวจสอบจุดเอกฐานภายใน)
        # -------------------------------------------------------------
        f_a = float(lower.evalf())
        f_b = float(upper.evalf())
        if f_a >= f_b:
            raise ValueError("ขอบล่าง a ต้องน้อยกว่าขอบบน b")

        interior_sings = _find_interior_singularities(expr, f_a, f_b)

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

            left_part = sp.integrate(expr, (X, lower, c_sp))
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
                result = float(res_val.evalf()) if getattr(res_val, "is_real", False) else None
                value_latex = sp.latex(res_val)
                steps.append(
                    f"ทั้งสองฝั่งลู่เข้าสู่ค่าจริงจำกัด: \\int_{{{lower_latex}}}^{{{bound_latex}}} f(x)\\,dx = {value_latex}"
                )
            else:
                status = "unsupported"
                result = None
                value_latex = "\\text{unsupported}"
        else:
            steps.append(
                f"แปลงเป็นรูปลิมิตของอินทิกรัลจำกัดเขต: \\lim_{{t \\to {bound_latex}}} \\int_{{{lower_latex}}}^{{t}} \\left({sp.latex(expr)}\\right) \\, dx"
            )
            res_val = sp.integrate(expr, (X, lower, upper))
            status = _classify_improper(res_val)

            if status == "finite":
                result = float(res_val.evalf()) if getattr(res_val, "is_real", False) else None
                value_latex = sp.latex(res_val)
                steps.append(f"อินทิกรัลลู่เข้าสู่ค่าจำกัด: {value_latex}")
            elif status == "divergent":
                result = None
                value_latex = "\\text{diverges}"
                steps.append("อินทิกรัลลู่ออก (Diverges) ไม่ลู่เข้าสู่ค่าจริงจำกัด")
            else:
                result = None
                value_latex = "\\text{unsupported}"

        latex_str = f"\\int_{{{lower_latex}}}^{{{bound_latex}}} {sp.latex(expr)} \\, dx = {value_latex}"
        return {
            "ok": True,
            "result": result,
            "latex": latex_str,
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
            "interior_singularities": [],
        }
