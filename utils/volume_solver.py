"""utils/volume_solver.py — ปริมาตรของรูปทรงตันจากการหมุนรอบแกน

คำนวณปริมาตรของรูปทรงตันที่เกิดจากการหมุนรอบแกน x แบบ Disk หรือ Washer Method
พร้อมแจกแจงแกนหมุน รัศมีนอก/ใน ทิศทางการกวาด และคำตอบแม่นตรงในรูป k*pi
ตามเกณฑ์ Universal Step Contract
"""
import math
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
from utils.sympy_solver import _clean_calculus_input, _get_variable


def _to_latex(sym_obj) -> str:
    lat = sp.latex(sym_obj)
    return lat.replace(r"\log", r"\ln")


def _parse_input(expr_str: str) -> sp.Expr:
    clean = (expr_str or "").strip()
    if not clean:
        raise ValueError("Empty input string")
    return parse_expr(clean, transformations=TRANSFORMATIONS, local_dict=LOCAL_MATH_DICT)


def compute_volume(
    expr_str: str,
    a: float,
    b: float,
    method: str = "disk",
    inner_expr_str: str | None = None,
) -> dict:
    """คำนวณปริมาตรของรูปทรงตันที่เกิดจากการหมุนรอบแกน x แบบ Disk หรือ Washer Method ตาม Universal Step Contract"""
    clean_outer = (expr_str or "").strip()
    if not clean_outer:
        return {
            "ok": False,
            "result": None,
            "latex": "",
            "steps": [],
            "expr": None,
            "inner_expr": None,
            "method": method,
            "error": "กรุณาระบุฟังก์ชันรัศมี R(x)",
        }

    try:
        a_f, b_f = float(a), float(b)
        if not (math.isfinite(a_f) and math.isfinite(b_f)):
            raise ValueError("ขอบล่าง a และขอบบน b ต้องเป็นจำนวนจริงจำกัด")
        if b_f <= a_f:
            raise ValueError("ขอบล่าง a ต้องน้อยกว่าขอบบน b (ขอบเขตกลับด้านหรือไม่ถูกต้อง)")

        m = (method or "disk").strip().lower()
        if m not in ("disk", "washer"):
            raise ValueError(f"วิธี '{method}' ยังไม่รองรับในระบบ (รองรับเฉพาะ 'disk' และ 'washer')")

        R_expr = _parse_input(clean_outer)
        r_expr = None
        if m == "washer":
            clean_inner = (inner_expr_str or "").strip()
            if not clean_inner:
                raise ValueError(
                    "สำหรับวิธีวงแหวน (Washer Method) ต้องระบุฟังก์ชันรัศมีวงใน r(x) ด้วย (หากไม่มีรัศมีใน ให้เลือกวิธี 'disk')"
                )
            r_expr = _parse_input(clean_inner)

        all_free = R_expr.free_symbols | (r_expr.free_symbols if r_expr is not None else set())
        if not all_free:
            var_sym = X
        elif len(all_free) == 1:
            var_sym = list(all_free)[0]
        else:
            dummy_expr = sum(all_free)
            var_sym = _get_variable(dummy_expr)
        v_lat = _to_latex(var_sym)

        a_sp = sp.Rational(str(a)) if not isinstance(a, sp.Rational) else a
        b_sp = sp.Rational(str(b)) if not isinstance(b, sp.Rational) else b

        def _fmt_bound(v):
            try:
                fv = float(v)
                return str(int(fv)) if fv.is_integer() else f"{fv:g}"
            except Exception:
                return _to_latex(v)

        a_disp = _fmt_bound(a)
        b_disp = _fmt_bound(b)

        if m == "disk":
            integrand = sp.simplify(R_expr**2)
            primitive = sp.integrate(integrand, var_sym)
            int_val = sp.integrate(integrand, (var_sym, a_sp, b_sp))
            vol_val = int_val * sp.pi

            if vol_val.has(sp.Integral) or not (
                getattr(vol_val, "is_real", False) and getattr(vol_val, "is_finite", False)
            ):
                raise ValueError("ไม่สามารถคำนวณปริมาตรจำกัดได้บนช่วงที่กำหนด (อาจมีจุดเอกฐาน)")

            res_float = float(vol_val.evalf())

            steps = [
                f"กำหนดฟังก์ชันและช่วง: รัศมี $R({v_lat}) = {_to_latex(R_expr)}$ บนช่วง $[{a_disp}, {b_disp}]$",
                f"เป้าหมาย / กฎที่ใช้ (Goal / Rule): คำนวณปริมาตรของรูปทรงตันที่เกิดจากการหมุนรอบแกน {v_lat} โดยวิธีจาน (Disk Method) "
                f"ตามสูตร $V = \\pi \\int_{{{a_disp}}}^{{{b_disp}}} [R({v_lat})]^2 \\, d{v_lat}$ "
                f"(เลือกใช้วิธี Disk เนื่องจากพื้นที่ระนาบแนบสนิทกับแกนหมุน ไม่มีช่องว่างตรงกลาง)",
                f"นิพจน์หลังแทนค่า (Substituted expression): ระบุแกนหมุนคือแกน ${v_lat}$ (สมการแนวนอน) "
                f"โดยมีรัศมี $R({v_lat}) = {_to_latex(R_expr)}$ เป็นระยะทางตั้งฉากจากแกนหมุนถึงเส้นโค้ง "
                f"และกวาดจานตามแนวตัวแปรการอินทิเกรต $d{v_lat}$ จาก ${v_lat} = {a_disp}$ ถึง ${v_lat} = {b_disp}$",
                f"พีชคณิตระหว่างทาง (Intermediate algebra): พื้นที่หน้าตัดรูปจาน $A({v_lat}) = \\pi [R({v_lat})]^2 = \\pi [{_to_latex(R_expr)}]^2 = \\pi \\left({_to_latex(integrand)}\\right)$ "
                f"และหาปฏิยานุพันธ์ $\\int [{_to_latex(R_expr)}]^2 \\, d{v_lat} = {_to_latex(primitive)}$",
                f"แทนค่าขอบเขต: $V = \\pi \\left[ {_to_latex(primitive)} \\right]_{{{a_disp}}}^{{{b_disp}}} = \\pi \\left( {_to_latex(int_val)} \\right) = {_to_latex(vol_val)}$",
                f"เงื่อนไขโดเมน (Domain restriction): รัศมี $R({v_lat})$ ต้องเป็นฟังก์ชันต่อเนื่องบนช่วงปิด $[{a_disp}, {b_disp}]$",
                f"ผลลัพธ์แม่นตรง (Exact result): คำนวณปริมาตรทรงตัน: $V = {_to_latex(vol_val)} \\approx {res_float:.6g}$ ลูกบาศก์หน่วย",
            ]

            return {
                "ok": True,
                "result": res_float,
                "latex": f"V = \\pi \\int_{{{a_disp}}}^{{{b_disp}}} [{_to_latex(R_expr)}]^2 \\, d{v_lat} = {_to_latex(vol_val)}",
                "steps": steps,
                "expr": R_expr,
                "inner_expr": None,
                "method": "disk",
                "error": None,
                "variable": str(var_sym.name),
            }

        else:  # washer
            diff_sq = sp.simplify(R_expr**2 - r_expr**2)
            primitive = sp.integrate(diff_sq, var_sym)
            int_val = sp.integrate(diff_sq, (var_sym, a_sp, b_sp))
            vol_val = abs(int_val * sp.pi)

            if vol_val.has(sp.Integral) or not (
                getattr(vol_val, "is_real", False) and getattr(vol_val, "is_finite", False)
            ):
                raise ValueError("ไม่สามารถคำนวณปริมาตรจำกัดได้บนช่วงที่กำหนด (อาจมีจุดเอกฐาน หรือไม่อยู่ในโดเมนจำนวนจริง)")

            res_float = float(vol_val.evalf())

            steps = [
                f"กำหนดฟังก์ชันและช่วง: รัศมีนอก $R({v_lat}) = {_to_latex(R_expr)}$, รัศมีใน $r({v_lat}) = {_to_latex(r_expr)}$ บนช่วง $[{a_disp}, {b_disp}]$",
                f"เป้าหมาย / กฎที่ใช้ (Goal / Rule): คำนวณปริมาตรของรูปทรงตันที่เกิดจากการหมุนรอบแกน {v_lat} โดยวิธีวงแหวน (Washer Method) "
                f"ตามสูตร $V = \\pi \\int_{{{a_disp}}}^{{{b_disp}}} \\left( [R({v_lat})]^2 - [r({v_lat})]^2 \\right) \\, d{v_lat}$ "
                f"(เลือกใช้วิธี Washer เนื่องจากมีช่องว่างหรือรูกลวงระหว่างเส้นโค้งกับแกนหมุน)",
                f"นิพจน์หลังแทนค่า (Substituted expression): ระบุแกนหมุนคือแกน ${v_lat}$ โดยแจกแจงรัศมีทั้งสองแยกกัน:\n"
                f"- รัศมีนอก (Outer radius): $R({v_lat}) = {_to_latex(R_expr)}$ (ระยะจากแกนหมุนถึงขอบนอก)\n"
                f"- รัศมีใน (Inner radius): $r({v_lat}) = {_to_latex(r_expr)}$ (ระยะจากแกนหมุนถึงขอบใน)\n"
                f"และกวาดวงแหวนตามแนวตัวแปรการอินทิเกรต $d{v_lat}$ จาก ${v_lat} = {a_disp}$ ถึง ${v_lat} = {b_disp}$",
                f"พีชคณิตระหว่างทาง (Intermediate algebra): พื้นที่หน้าตัดรูปวงแหวน $A({v_lat}) = \\pi \\left( [R({v_lat})]^2 - [r({v_lat})]^2 \\right) = \\pi \\left( {_to_latex(diff_sq)} \\right)$ "
                f"และหาปฏิยานุพันธ์ $\\int \\left( [R({v_lat})]^2 - [r({v_lat})]^2 \\right) \\, d{v_lat} = {_to_latex(primitive)}$",
                f"แทนค่าขอบเขต: $V = \\pi \\left| \\left[ {_to_latex(primitive)} \\right]_{{{a_disp}}}^{{{b_disp}}} \\right| = {_to_latex(vol_val)}$",
                f"เงื่อนไขโดเมน (Domain restriction): ฟังก์ชันรัศมีมีความต่อเนื่องบนช่วงปิด $[{a_disp}, {b_disp}]$ โดยมีเงื่อนไข $R({v_lat}) \\geq r({v_lat}) \\geq 0$",
                f"ผลลัพธ์แม่นตรง (Exact result): คำนวณปริมาตรทรงตัน: $V = {_to_latex(vol_val)} \\approx {res_float:.6g}$ ลูกบาศก์หน่วย",
            ]

            return {
                "ok": True,
                "result": res_float,
                "latex": f"V = \\pi \\int_{{{a_disp}}}^{{{b_disp}}} \\left([{_to_latex(R_expr)}]^2 - [{_to_latex(r_expr)}]^2\\right) \\, d{v_lat} = {_to_latex(vol_val)}",
                "steps": steps,
                "expr": R_expr,
                "inner_expr": r_expr,
                "method": "washer",
                "error": None,
                "variable": str(var_sym.name),
            }

    except Exception as e:
        return {
            "ok": False,
            "result": None,
            "latex": "",
            "steps": [],
            "expr": None,
            "inner_expr": None,
            "method": method,
            "error": f"ไม่สามารถคำนวณได้: {e}",
        }
