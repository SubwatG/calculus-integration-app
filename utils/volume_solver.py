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
    """คำนวณปริมาตรของรูปทรงตันที่เกิดจากการหมุนรอบแกน x แบบ Disk หรือ Washer Method"""
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
            raise ValueError("ขอบล่าง a ต้องน้อยกว่าขอบบน b")

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
        v_lat = sp.latex(var_sym)

        if m == "disk":
            vol_val = sp.pi * sp.integrate(R_expr**2, (var_sym, a_f, b_f))
            if vol_val.has(sp.Integral) or not (
                getattr(vol_val, "is_real", False) and getattr(vol_val, "is_finite", False)
            ):
                raise ValueError("ไม่สามารถคำนวณปริมาตรจำกัดได้บนช่วงที่กำหนด (อาจมีจุดเอกฐาน)")

            steps = [
                f"ฟังก์ชันรัศมี: R({v_lat}) = {sp.latex(R_expr)} บนช่วง [{a}, {b}]",
                f"สูตรวิธีจาน (Disk Method): V = \\pi \\int_{{{a}}}^{{{b}}} [{sp.latex(R_expr)}]^2 \\, d{v_lat}",
                f"คำนวณปริมาตรทรงตัน: V = {sp.latex(vol_val)}",
            ]
            return {
                "ok": True,
                "result": float(vol_val) if vol_val.is_number and vol_val.is_real else None,
                "latex": f"V = \\pi \\int_{{{a}}}^{{{b}}} [{sp.latex(R_expr)}]^2 \\, d{v_lat} = {sp.latex(vol_val)}",
                "steps": steps,
                "expr": R_expr,
                "inner_expr": None,
                "method": "disk",
                "error": None,
                "variable": str(var_sym.name),
            }
        else:  # washer
            diff_sq = sp.simplify(R_expr**2 - r_expr**2)

            # Direct integration of difference of squares
            val_direct = sp.pi * sp.integrate(diff_sq, (var_sym, a_f, b_f))
            if val_direct.has(sp.Integral) or not (
                getattr(val_direct, "is_real", False) and getattr(val_direct, "is_finite", False)
            ):
                raise ValueError(
                    "ไม่สามารถคำนวณปริมาตรจำกัดได้บนช่วงที่กำหนด (อาจมีจุดเอกฐาน หรือไม่อยู่ในโดเมนจำนวนจริง)"
                )

            vol_val = abs(val_direct)
            steps = [
                f"กำหนดรัศมีนอก R({v_lat}) = {sp.latex(R_expr)}, \\quad รัศมีใน r({v_lat}) = {sp.latex(r_expr)} บนช่วง [{a}, {b}]",
                f"สูตรวิธีวงแหวน (Washer Method): V = \\pi \\int_{{{a}}}^{{{b}}} \\left( [R({v_lat})]^2 - [r({v_lat})]^2 \\right) \\, d{v_lat}",
                f"พื้นที่หน้าตัดวงแหวน: A({v_lat}) = \\pi \\left( [{sp.latex(R_expr)}]^2 - [{sp.latex(r_expr)}]^2 \\right) = \\pi \\left( {sp.latex(diff_sq)} \\right)",
                f"คำนวณปริมาตรทรงตัน: V = {sp.latex(vol_val)}",
            ]
            return {
                "ok": True,
                "result": float(vol_val) if vol_val.is_number and vol_val.is_real else None,
                "latex": f"V = \\pi \\int_{{{a}}}^{{{b}}} \\left([{sp.latex(R_expr)}]^2 - [{sp.latex(r_expr)}]^2\\right) \\, d{v_lat} = {sp.latex(vol_val)}",
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
