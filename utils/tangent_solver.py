"""utils/tangent_solver.py — เส้นสัมผัสและอนุพันธ์

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


H = sp.Symbol("h", real=True)


def _parse_input(expr_str: str) -> sp.Expr:
    clean = (expr_str or "").strip()
    if not clean:
        raise ValueError("Empty input string")
    return parse_expr(clean, transformations=TRANSFORMATIONS, local_dict=LOCAL_MATH_DICT)


def compute_tangent(expr_str: str, a: float) -> dict:
    """คำนวณความชันเส้นสัมผัส f'(a) และสมการเส้นสัมผัส y = f'(a)(x-a) + f(a)"""
    try:
        expr = _parse_input(expr_str)
        a_f = float(a)

        try:
            fa_sym = expr.subs(X, a_f)
        except Exception as e:
            return {
                "ok": False,
                "result": None,
                "latex": "",
                "steps": [],
                "expr": expr,
                "error": f"ไม่สามารถแทนค่า f({a_f}) ได้: {e}",
                "status": "error",
            }

        if not (getattr(fa_sym, "is_real", False) and getattr(fa_sym, "is_finite", False)):
            return {
                "ok": False,
                "result": None,
                "latex": "",
                "steps": [
                    f"พิจารณาจุดที่ต้องการหาสัมผัส: x = {a_f}",
                    f"แทนค่าในฟังก์ชัน: f({a_f}) ไม่นิยาม หรือไม่เป็นจำนวนจริงจำกัด",
                ],
                "expr": expr,
                "error": f"ฟังก์ชัน f(x) ไม่นิยามที่จุด x = {a_f} (หรือไม่อยู่ในโดเมนจำนวนจริง)",
                "status": "undefined_point",
            }

        df = sp.diff(expr, X)
        try:
            slope_sym = df.subs(X, a_f)
        except Exception:
            slope_sym = sp.nan

        if slope_sym.is_real and slope_sym.is_finite:
            status = "finite"
            slope = float(slope_sym)
            tangent_eq = slope_sym * (X - a_f) + fa_sym
            latex_str = f"y = {sp.latex(sp.simplify(tangent_eq))}"
            steps = [
                f"กำหนดฟังก์ชันและจุดที่พิจารณา: f(x) = {sp.latex(expr)}, \\quad a = {a_f}",
                f"คำนวณพิกัด y ของจุดสัมผัส: f({a_f}) = {sp.latex(fa_sym)} \\implies (x_0, y_0) = ({a_f}, {sp.latex(fa_sym)})",
                f"หาอนุพันธ์เพื่อหาความชันของฟังก์ชัน: f'(x) = \\frac{{d}}{{dx}}\\left[{sp.latex(expr)}\\right] = {sp.latex(df)}",
                f"แทนค่าจุด a เพื่อหาความชันเส้นสัมผัส m: m = f'({a_f}) = {sp.latex(slope_sym)}",
                f"แทนค่าในสูตรสมการเส้นสัมผัส y - y_0 = m(x - x_0): y - ({sp.latex(fa_sym)}) = {sp.latex(slope_sym)}(x - {a_f})",
                f"จัดรูปสมการเส้นสัมผัสในรูปชัดแจ้ง: y = {sp.latex(sp.simplify(tangent_eq))}",
            ]
        else:
            diff_quot = (expr.subs(X, a_f + H) - fa_sym) / H
            try:
                left_m = sp.limit(diff_quot, H, 0, dir="-")
                right_m = sp.limit(diff_quot, H, 0, dir="+")
            except Exception:
                left_m, right_m = sp.nan, sp.nan

            if left_m == right_m:
                if left_m in (sp.oo, -sp.oo):
                    status = "vertical"
                    slope = None
                    latex_str = f"x = {a_f}"
                    steps = [
                        f"กำหนดฟังก์ชันและจุดที่พิจารณา: f(x) = {sp.latex(expr)}, \\quad a = {a_f}",
                        f"คำนวณพิกัดจุดสัมผัส: (x_0, y_0) = ({a_f}, {sp.latex(fa_sym)})",
                        f"พิจารณาลิมิตของอัตราการเปลี่ยนแปลงเฉลี่ย: \\lim_{{h \\to 0}} \\frac{{f({a_f}+h) - f({a_f})}}{{h}} = {sp.latex(left_m)}",
                        "ความชันลู่ไปสู่อนันต์ แสดงว่าเป็นเส้นสัมผัสแนวดิ่ง (Vertical Tangent Line)",
                        f"สมการเส้นสัมผัสแนวดิ่ง: x = {a_f}",
                    ]
                elif getattr(left_m, "is_real", False) and getattr(left_m, "is_finite", False):
                    status = "finite"
                    slope = float(left_m)
                    tangent_eq = left_m * (X - a_f) + fa_sym
                    latex_str = f"y = {sp.latex(sp.simplify(tangent_eq))}"
                    steps = [
                        f"กำหนดฟังก์ชันและจุดที่พิจารณา: f(x) = {sp.latex(expr)}, \\quad a = {a_f}",
                        f"คำนวณพิกัดจุดสัมผัส: (x_0, y_0) = ({a_f}, {sp.latex(fa_sym)})",
                        f"คำนวณความชันผ่านนิยามลิมิตของอัตราการเปลี่ยนแปลงเฉลี่ย: m = \\lim_{{h \\to 0}} \\frac{{f({a_f}+h) - f({a_f})}}{{h}} = {sp.latex(left_m)}",
                        f"แทนค่าในสูตรสมการเส้นสัมผัส y - y_0 = m(x - x_0): y - ({sp.latex(fa_sym)}) = {sp.latex(left_m)}(x - {a_f})",
                        f"จัดรูปสมการเส้นสัมผัส: y = {sp.latex(sp.simplify(tangent_eq))}",
                    ]
                else:
                    status = "unsupported"
                    slope = None
                    latex_str = r"\text{(unsupported)}"
                    steps = ["ระบบไม่สามารถระบุเส้นสัมผัสได้อย่างแน่ชัด"]
            elif left_m != right_m:
                status = "non_differentiable"
                slope = None
                latex_str = r"\text{(does not exist)}"
                steps = [
                    f"กำหนดฟังก์ชันและจุดที่พิจารณา: f(x) = {sp.latex(expr)}, \\quad a = {a_f}",
                    f"คำนวณพิกัดจุดบนกราฟ: (x_0, y_0) = ({a_f}, {sp.latex(fa_sym)})",
                    f"พิจารณาอนุพันธ์ทางซ้าย: f'_-({a_f}) = \\lim_{{h \\to 0^-}} \\frac{{f({a_f}+h) - f({a_f})}}{{h}} = {sp.latex(left_m)}",
                    f"พิจารณาอนุพันธ์ทางขวา: f'_+({a_f}) = \\lim_{{h \\to 0^+}} \\frac{{f({a_f}+h) - f({a_f})}}{{h}} = {sp.latex(right_m)}",
                    f"เนื่องจากอนุพันธ์ทางซ้าย ({sp.latex(left_m)}) \\neq อนุพันธ์ทางขวา ({sp.latex(right_m)}) ฟังก์ชันจึงไม่สามารถหาอนุพันธ์ได้ที่จุดนี้ (จุดมุมแหลม / Corner Point) และไม่มีเส้นสัมผัส",
                ]
            else:
                status = "unsupported"
                slope = None
                latex_str = r"\text{(unsupported)}"
                steps = ["ระบบไม่สามารถระบุเส้นสัมผัสได้อย่างแน่ชัด"]

        return {
            "ok": True,
            "result": slope,
            "latex": latex_str,
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
