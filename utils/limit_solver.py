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
    "inf": sp.oo,
    "infinity": sp.oo,
    "oo": sp.oo,
}

X = sp.Symbol("x")
from utils.sympy_solver import _clean_calculus_input, _get_variable


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


def _parse_target_a(a_val: float | int | str | sp.Expr) -> sp.Expr:
    """แปลงค่าจุด a ที่รับเข้ามาเป็น SymPy Expression (รองรับตัวเลข, สัญลักษณ์ pi, e, และ inf, -inf)"""
    if isinstance(a_val, (int, float)):
        return sp.Rational(str(a_val))
    if isinstance(a_val, sp.Expr):
        return a_val
    s = str(a_val).strip()
    if not s:
        return sp.Integer(0)
    s_clean = s.lower().replace(" ", "")
    if s_clean in ("inf", "+inf", "oo", "+oo", "infinity", "+infinity"):
        return sp.oo
    if s_clean in ("-inf", "-oo", "-infinity"):
        return -sp.oo
    return parse_expr(s, transformations=TRANSFORMATIONS, local_dict=LOCAL_MATH_DICT)


def _check_real_domain(expr: sp.Expr, a: float, delta: float = 0.01, var: sp.Symbol = X) -> tuple[bool, bool]:
    """ตรวจสอบว่าฟังก์ชันนิยามบนระบบจำนวนจริงทางซ้าย a - delta และทางขวา a + delta หรือไม่"""
    left_sample = a - delta
    right_sample = a + delta

    try:
        val_l = expr.subs(var, left_sample)
        im_l = float(sp.im(val_l.evalf()))
        re_l = float(sp.re(val_l.evalf()))
        left_real = abs(im_l) < 1e-9 and math.isfinite(re_l)
    except Exception:
        left_real = False

    try:
        val_r = expr.subs(var, right_sample)
        im_r = float(sp.im(val_r.evalf()))
        re_r = float(sp.re(val_r.evalf()))
        right_real = abs(im_r) < 1e-9 and math.isfinite(re_r)
    except Exception:
        right_real = False

    return left_real, right_real


def _format_point_str(a_sp: sp.Expr) -> str:
    r"""แปลงจุด a_sp เป็นสตริงหรือ LaTeX ที่อ่านง่าย เช่น 2, \pi/2, \infty"""
    if a_sp == sp.oo:
        return "\\infty"
    if a_sp == -sp.oo:
        return "-\\infty"
    try:
        f = float(a_sp.evalf())
        if abs(f - round(f)) < 1e-6:
            return str(int(round(f)))
    except Exception:
        pass
    return sp.latex(a_sp)


def _format_samples(a_sp: sp.Expr) -> tuple[str, str]:
    """สร้างตัวอย่างค่า x ที่เข้าใกล้ a ทางซ้าย (x < a) และทางขวา (x > a) เพื่อให้เห็นภาพชัดเจน"""
    if a_sp == sp.oo:
        return "10, 50, 100", "N/A"
    if a_sp == -sp.oo:
        return "N/A", "-10, -50, -100"
    try:
        a_num = float(a_sp.evalf())
        if abs(a_num - round(a_num)) < 1e-6:
            a_int = int(round(a_num))
            s_left = f"{a_int - 0.1:g}, {a_int - 0.01:g}, {a_int - 0.001:g}"
            s_right = f"{a_int + 0.1:g}, {a_int + 0.01:g}, {a_int + 0.001:g}"
        else:
            s_left = f"{a_num - 0.1:.3g}, {a_num - 0.01:.3g}, {a_num - 0.001:.3g}"
            s_right = f"{a_num + 0.1:.3g}, {a_num + 0.01:.3g}, {a_num + 0.001:.3g}"
        return s_left, s_right
    except Exception:
        return "a - 0.1, a - 0.01", "a + 0.1, a + 0.01"



# ---------------------------------------------------------------------------
# ลำดับชั้นการเฉลยลิมิตเข้าใกล้จุดตามหลักการสอน (Pedagogical Decision Hierarchy)
#   Level 1: Direct Substitution        แทนค่าโดยตรง (ฟังก์ชันต่อเนื่อง ณ จุดนั้น)
#   Level 2: Indeterminate 0/0          แยกตัวประกอบ จัดรูป และตัดทอนตัวร่วม
#   Level 3: Special Trig Limit         lim sin(g)/g = 1 (Fundamental Trig Limit)
#   Level 4: Infinite Limit c/0         วิเคราะห์เครื่องหมายตัวส่วนสองฝั่ง -> ±∞
#   Level 5: Absolute Value / Piecewise แยกพิจารณาลิมิตซ้ายและขวาอย่างชัดเจน
#   Level 6: Oscillating                แกว่งกวัด ไม่มีลิมิต
#   Level 7: End Behavior (±∞)          เส้นกำกับแนวนอน (สาขา a -> ±∞)
# ---------------------------------------------------------------------------


def _safe_simplify(e: sp.Expr) -> sp.Expr:
    """simplify แบบไม่โยน exception (คืนค่าเดิมถ้าล้มเหลว)"""
    try:
        return sp.simplify(e)
    except Exception:
        return e


def _is_zero_expr(e) -> bool:
    """ตรวจว่านิพจน์มีค่าเป็นศูนย์หรือไม่"""
    if e is None:
        return False
    try:
        return bool(_safe_simplify(e) == 0)
    except Exception:
        return False


def _as_finite_float(e) -> float | None:
    r"""คืนค่า float หาก e เป็นจำนวนจริงจำกัด มิฉะนั้นคืนค่า None"""
    if e is None:
        return None
    try:
        if not getattr(e, "is_number", False):
            return None
    except Exception:
        return None
    if getattr(e, "is_finite", None) is not True:
        return None
    try:
        f = float(e.evalf())
    except Exception:
        return None
    return f if math.isfinite(f) else None


def _detect_special_trig_limit(expr: sp.Expr, var_sym: sp.Symbol, a_sp: sp.Expr):
    r"""ตรวจหารูปแบบลิมิตตรีโกณมิติพื้นฐาน lim sin(g)/g = 1

    คืนค่า (g, L) เมื่อ expr = L · sin(g)/g โดยที่ g -> 0 ขณะ var -> a
    มิฉะนั้นคืนค่า None
    """
    try:
        sin_atoms = expr.atoms(sp.sin)
    except Exception:
        return None
    for sin_atom in sin_atoms:
        if not getattr(sin_atom, "args", None):
            continue
        g = sin_atom.args[0]
        if g == 0:
            continue
        try:
            if not _is_zero_expr(g.subs(var_sym, a_sp)):
                continue
            ratio = _safe_simplify(expr / (sp.sin(g) / g))
        except Exception:
            continue
        try:
            if ratio.free_symbols:
                continue
        except Exception:
            continue
        if getattr(ratio, "is_finite", None) is not True:
            continue
        return g, ratio
    return None


def _steps_direct_substitution(expr: sp.Expr, a_str: str, v_lat: str, f_a: sp.Expr):
    r"""Level 1: การแทนค่าโดยตรง (Direct Substitution Property)"""
    expr_tex = sp.latex(expr)
    f_a_tex = sp.latex(f_a)
    steps = [
        f"ตรวจสอบการแทนค่าโดยตรง (Direct Substitution): ฟังก์ชัน $f({v_lat}) = {expr_tex}$ เป็นฟังก์ชันต่อเนื่อง ณ จุด ${v_lat} = {a_str}$ และการแทนค่าตรงไม่เกิดรูปแบบยังไม่กำหนด จึงใช้สมบัติการแทนค่าโดยตรงได้ทันที",
        f"แทนค่า ${v_lat} = {a_str}$ ลงในฟังก์ชัน: $f({a_str}) = {f_a_tex}$",
        f"สรุปผลค่าลิมิต (ลิมิตของฟังก์ชันต่อเนื่องเท่ากับค่าฟังก์ชันที่จุดนั้น): \\lim_{{{v_lat} \\to {a_str}}} \\left({expr_tex}\\right) = f({a_str}) = {f_a_tex}",
    ]
    latex_str = f"\\lim_{{{v_lat} \\to {a_str}}} {expr_tex} = {f_a_tex}"
    return steps, _as_finite_float(f_a), latex_str


def _steps_indeterminate_factoring(expr: sp.Expr, var_sym: sp.Symbol, a_sp: sp.Expr,
                                   a_str: str, v_lat: str, lim_val: sp.Expr):
    r"""Level 2: รูปแบบยังไม่กำหนด 0/0 — แยกตัวประกอบ/จัดรูป แล้วตัดทอนตัวร่วม"""
    expr_tex = sp.latex(expr)
    try:
        num_e, den_e = sp.fraction(sp.together(expr))
    except Exception:
        num_e, den_e = expr, sp.Integer(1)
    num_f = sp.factor(num_e)
    den_f = sp.factor(den_e)
    num_tex = sp.latex(num_f)
    den_tex = sp.latex(den_f)
    did_factor = (num_f != num_e) or (den_f != den_e)

    try:
        reduced = sp.cancel(expr)
    except Exception:
        reduced = expr
    if reduced == expr:
        reduced = _safe_simplify(expr)
    reduce_changed = (reduced != expr)
    reduced_tex = sp.latex(reduced)

    sub_val = None
    try:
        sub_val = _safe_simplify(reduced.subs(var_sym, a_sp))
    except Exception:
        sub_val = None
    val_float = _as_finite_float(sub_val)
    if val_float is None:
        sub_val = _safe_simplify(lim_val)
        val_float = _as_finite_float(sub_val)
    val_tex = sp.latex(sub_val)

    steps = [
        f"ตรวจสอบการแทนค่าเบื้องต้น (Preliminary Substitution): แทน ${v_lat} = {a_str}$ ตรง ๆ ทั้งเศษและส่วนได้รูป $\\frac{{0}}{{0}}$ ซึ่งเป็นรูปแบบยังไม่กำหนด (Indeterminate Form) จึงยังสรุปค่าลิมิตไม่ได้ ต้องจัดรูปพีชคณิตก่อน",
    ]

    if did_factor:
        steps.append(
            f"การจัดรูปพีชคณิต (แยกตัวประกอบ / Factoring): แยกตัวประกอบของทั้งตัวเศษและตัวส่วน\n${expr_tex} = \\frac{{{num_tex}}}{{{den_tex}}}$"
        )
    else:
        steps.append(
            f"การจัดรูปพีชคณิต (แยกตัวประกอบ / Factoring): ตรวจสอบตัวประกอบของตัวเศษและตัวส่วนแล้ว ยังไม่พบตัวร่วมที่ตัดกันได้โดยตรง จึงต้องจัดรูปด้วยเทคนิคอื่นต่อไป\n$f({v_lat}) = {expr_tex}$"
        )

    if reduce_changed:
        steps.append(
            f"การตัดทอนตัวร่วม (Cancelling the Common Factor): เพราะการหา $\\lim_{{{v_lat} \\to {a_str}}}$ หมายถึง ${v_lat} \\neq {a_str}$ (ค่าไม่เท่ากับ {a_str} พอดี) ตัวร่วมจึงไม่เป็นศูนย์และตัดทอนได้อย่างถูกต้อง เหลือรูปอย่างง่าย\n${expr_tex} = {reduced_tex} \\quad (\\text{{เมื่อ }} {v_lat} \\neq {a_str})$"
        )
        steps.append(
            f"แทนค่าลงในรูปที่จัดแล้ว: $\\lim_{{{v_lat} \\to {a_str}}} \\left({reduced_tex}\\right) = {val_tex}$ (แทนค่าโดยตรงได้แล้ว ไม่เกิดรูป $\\frac{{0}}{{0}}$ อีกต่อไป)"
        )
    else:
        steps.append(
            f"การจัดรูปต่อ (คูณด้วยสังยุค / เอกลักษณ์ตรีโกณมิติ): เพราะตัดทอนตัวร่วมตรง ๆ ไม่ได้ ต้องใช้เทคนิคอื่นกำจัดรูป $\\frac{{0}}{{0}}$ โดยอาศัยหลักการเดิมว่า ${v_lat} \\neq {a_str}$ ตลอดเวลาในการเข้าใกล้"
        )
        steps.append(
            f"สรุปค่าลิมิตจากรูปที่จัดแล้ว: $\\lim_{{{v_lat} \\to {a_str}}} \\left({reduced_tex}\\right) = {val_tex}$"
        )

    steps.append(
        f"สรุปผลค่าลิมิต: \\lim_{{{v_lat} \\to {a_str}}} \\left({expr_tex}\\right) = {val_tex}"
    )
    latex_str = f"\\lim_{{{v_lat} \\to {a_str}}} {expr_tex} = {val_tex}"
    return steps, val_float, latex_str


def _steps_special_trig(expr: sp.Expr, a_str: str, v_lat: str, g: sp.Expr, L: sp.Expr):
    r"""Level 3: ลิมิตตรีโกณมิติพื้นฐาน (Fundamental Trigonometric Limit)"""
    expr_tex = sp.latex(expr)
    g_tex = sp.latex(g)
    l_tex = sp.latex(L)
    steps = [
        f"ตรวจสอบการแทนค่าเบื้องต้น: แทน ${v_lat} = {a_str}$ ตรง ๆ ได้ $\\frac{{0}}{{0}}$ (รูปแบบยังไม่กำหนด) แต่โจทย์นี้อยู่ในรูปของลิมิตตรีโกณมิติพื้นฐานที่ทราบค่าได้จากทฤษฎีบท",
        f"ทฤษฎีบทลิมิตตรีโกณมิติพื้นฐาน (Fundamental Trigonometric Limit): $\\lim_{{{g_tex} \\to 0}} \\frac{{\\sin({g_tex})}}{{{g_tex}}} = 1$ (พิสูจน์ได้ด้วยทฤษฎีบทบีบ / Squeeze Theorem) และขณะที่ ${v_lat} \\to {a_str}$ จะได้ ${g_tex} \\to 0$",
        f"จัดรูปโจทย์ให้ตรงกับทฤษฎีบท: ${expr_tex} = {l_tex} \\cdot \\frac{{\\sin({g_tex})}}{{{g_tex}}}$",
        f"สรุปผลค่าลิมิต: \\lim_{{{v_lat} \\to {a_str}}} \\left({expr_tex}\\right) = {l_tex} \\cdot 1 = {l_tex}",
    ]
    latex_str = f"\\lim_{{{v_lat} \\to {a_str}}} {expr_tex} = {l_tex}"
    return steps, _as_finite_float(L), latex_str


def _steps_infinite_asymptote(expr: sp.Expr, a_str: str, v_lat: str,
                              lim_left: sp.Expr, lim_right: sp.Expr,
                              a_dir_left: str, a_dir_right: str,
                              s_left_ex: str, s_right_ex: str):
    r"""Level 4: ลิมิตอนันต์ (c/0 เมื่อ c ≠ 0) และเส้นกำกับแนวดิ่ง

    วิเคราะห์เครื่องหมายของตัวส่วนจากฝั่งซ้ายและฝั่งขวาอย่างชัดเจน
    """
    expr_tex = sp.latex(expr)
    left_tex = sp.latex(lim_left)
    right_tex = sp.latex(lim_right)

    def _side_note(val) -> str:
        if val == sp.oo:
            return f"ค่าของ $f({v_lat})$ เป็นบวกและมีขนาดเพิ่มขึ้นอย่างไม่มีขอบเขต พุ่งขึ้นสู่อนันต์ ($+\\infty$)"
        if val == -sp.oo:
            return f"ค่าของ $f({v_lat})$ ติดลบและมีขนาดเพิ่มขึ้นอย่างไม่มีขอบเขต พุ่งลงสู่ลบอนันต์ ($-\\infty$)"
        return f"ค่าของ $f({v_lat})$ มีแนวโน้มลู่เข้าหาค่าคงที่ {sp.latex(val)}"

    steps = [
        f"ตรวจสอบการแทนค่า: ขณะที่ ${v_lat} \\to {a_str}$ ตัวเศษลู่เข้าหาค่าคงที่ที่ไม่ใช่ศูนย์ ($c \\neq 0$) แต่ตัวส่วนลู่เข้าสู่ $0$ (รูป $\\frac{{c}}{{0}}$) ค่าฟังก์ชันจึงไม่มีขอบเขต ต้องวิเคราะห์เครื่องหมายจากทั้งสองฝั่งของ ${v_lat} = {a_str}$ (เส้นกำกับแนวดิ่ง / Vertical Asymptote)",
        f"พิจารณาลิมิตทางซ้าย (Left-hand limit, ${v_lat} \\to {a_dir_left}$): ลองแทนค่า ${v_lat} = {s_left_ex} \\dots$ เพื่อดูเครื่องหมาย\n{_side_note(lim_left)}\n\\lim_{{{v_lat} \\to {a_dir_left}}} \\left({expr_tex}\\right) = {left_tex}",
        f"พิจารณาลิมิตทางขวา (Right-hand limit, ${v_lat} \\to {a_dir_right}$): ลองแทนค่า ${v_lat} = {s_right_ex} \\dots$ เพื่อดูเครื่องหมาย\n{_side_note(lim_right)}\n\\lim_{{{v_lat} \\to {a_dir_right}}} \\left({expr_tex}\\right) = {right_tex}",
    ]

    if lim_left == lim_right and left_tex == right_tex:
        steps.append(
            f"สรุปผล: เครื่องหมายของตัวส่วนจากทั้งสองฝั่งเหมือนกัน ทำให้ $\\lim_{{{v_lat} \\to {a_dir_left}}} f({v_lat}) = \\lim_{{{v_lat} \\to {a_dir_right}}} f({v_lat}) = {left_tex}$ ลิมิตลู่ออกสู่อนันต์ (Diverges) และเส้นตรง ${v_lat} = {a_str}$ เป็นเส้นกำกับแนวดิ่ง\n\\lim_{{{v_lat} \\to {a_str}}} \\left({expr_tex}\\right) = {left_tex}"
        )
    else:
        steps.append(
            f"สรุปผล: เครื่องหมายของตัวส่วนจากสองฝั่งต่างกัน จึงได้ $\\lim_{{{v_lat} \\to {a_dir_left}}} f({v_lat}) = {left_tex} \\neq \\lim_{{{v_lat} \\to {a_dir_right}}} f({v_lat}) = {right_tex}$ เส้นกราฟแยกออกจากกันคนละทิศทาง จึงสรุปว่าไม่มีลิมิต\n\\lim_{{{v_lat} \\to {a_str}}} \\left({expr_tex}\\right) \\quad \\text{{(does not exist)}}"
        )

    if lim_left == lim_right and left_tex == right_tex:
        latex_str = f"\\lim_{{{v_lat} \\to {a_str}}} {expr_tex} = {left_tex}"
    else:
        latex_str = f"\\lim_{{{v_lat} \\to {a_str}}} {expr_tex} \\quad \\text{{(does not exist)}}"
    return steps, None, latex_str


def _steps_abs_piecewise(expr: sp.Expr, a_str: str, v_lat: str,
                         lim_left: sp.Expr, lim_right: sp.Expr,
                         a_dir_left: str, a_dir_right: str,
                         s_left_ex: str, s_right_ex: str, has_abs: bool):
    r"""Level 5: ฟังก์ชันค่าสัมบูรณ์ / ฟังก์ชันแบ่งช่วง — แยกพิจารณาสองฝั่งอย่างชัดเจน"""
    expr_tex = sp.latex(expr)
    left_tex = sp.latex(lim_left)
    right_tex = sp.latex(lim_right)

    if has_abs:
        why = f"โจทย์มีพจน์ค่าสัมบูรณ์ (Absolute Value) ซึ่งมีนิยามไม่เหมือนกันสองฝั่งของจุด ${v_lat} = {a_str}$ จึงต้องพิจารณาลิมิตทีละฝั่งอย่างชัดเจน"
        left_unwrap = f"เมื่อ ${v_lat} < {a_str}$ นิพจน์ภายในค่าสัมบูรณ์เป็นลบ จึงปลดค่าสัมบูรณ์เป็น $-({v_lat} - {a_str}) = {a_str} - {v_lat}$"
        right_unwrap = f"เมื่อ ${v_lat} > {a_str}$ นิพจน์ภายในค่าสัมบูรณ์เป็นบวก จึงปลดค่าสัมบูรณ์ได้ตรง ๆ เป็น ${v_lat} - {a_str}$"
    else:
        why = f"โจทย์เป็นฟังก์ชันแบ่งช่วง (Piecewise) ที่มีสูตรนิยามไม่เหมือนกันสองฝั่งของจุด ${v_lat} = {a_str}$ จึงต้องพิจารณาลิมิตทีละฝั่ง"
        left_unwrap = f"เลือกใช้สูตรของฟังก์ชันเมื่อ ${v_lat} < {a_str}$"
        right_unwrap = f"เลือกใช้สูตรของฟังก์ชันเมื่อ ${v_lat} > {a_str}$"

    steps = [
        f"ข้อสังเกตสำคัญ: {why}",
        f"พิจารณาลิมิตทางซ้าย (Left-hand limit, ${v_lat} \\to {a_dir_left}$): {left_unwrap} แล้วแทนค่าตัวอย่าง ${v_lat} = {s_left_ex} \\dots$\n\\lim_{{{v_lat} \\to {a_dir_left}}} \\left({expr_tex}\\right) = {left_tex}",
        f"พิจารณาลิมิตทางขวา (Right-hand limit, ${v_lat} \\to {a_dir_right}$): {right_unwrap} แล้วแทนค่าตัวอย่าง ${v_lat} = {s_right_ex} \\dots$\n\\lim_{{{v_lat} \\to {a_dir_right}}} \\left({expr_tex}\\right) = {right_tex}",
    ]

    if lim_left == lim_right and _as_finite_float(lim_left) is not None:
        result = float(lim_left)
        steps.append(
            f"สรุปผล: ลิมิตจากสองฝั่งให้ค่าเดียวกัน ({left_tex} = {right_tex}) กล่าวคือ $\\lim_{{{v_lat} \\to {a_dir_left}}} f({v_lat}) = \\lim_{{{v_lat} \\to {a_dir_right}}} f({v_lat}) = {left_tex}$ จึงสรุปได้ว่าลิมิตสองด้านมีค่าเท่ากับ {left_tex}\n\\lim_{{{v_lat} \\to {a_str}}} \\left({expr_tex}\\right) = {left_tex}"
        )
        latex_str = f"\\lim_{{{v_lat} \\to {a_str}}} {expr_tex} = {left_tex}"
    else:
        result = None
        steps.append(
            f"สรุปผล: ลิมิตจากสองฝั่งให้ค่าไม่เท่ากัน ($\\lim_{{{v_lat} \\to {a_dir_left}}} f({v_lat}) = {left_tex} \\neq \\lim_{{{v_lat} \\to {a_dir_right}}} f({v_lat}) = {right_tex}$) กราฟเกิดรอยกระโดด (Jump Discontinuity) จึงสรุปว่าไม่มีลิมิต\n\\lim_{{{v_lat} \\to {a_str}}} \\left({expr_tex}\\right) \\quad \\text{{(does not exist)}}"
        )
        latex_str = f"\\lim_{{{v_lat} \\to {a_str}}} {expr_tex} \\quad \\text{{(does not exist)}}"
    return steps, result, latex_str


def _steps_generic_finite(expr: sp.Expr, a_str: str, v_lat: str, lim_val: sp.Expr):
    r"""กรณีค่าลิมิตเป็นจำนวนจริง แต่อยู่นอกเหนือหมวดหลัก (เช่น ต้องใช้ทฤษฎีบทบีบ)"""
    expr_tex = sp.latex(expr)
    val_tex = sp.latex(_safe_simplify(lim_val))
    steps = [
        "การจัดรูปเชิงพีชคณิต: โจทย์นี้ไม่อยู่ในรูปแบบการแทนค่าตรง รูปแบบ 0/0 แบบตรีโกณมิติพื้นฐาน หรือแบบค่าสัมบูรณ์ จึงจัดรูปนิพจน์และใช้ทฤษฎีบทที่เกี่ยวข้อง (เช่น ทฤษฎีบทบีบ / การจัดรูปเศษส่วน) ก่อนแทนค่า",
        f"พิจารณาค่าลิมิต: \\lim_{{{v_lat} \\to {a_str}}} \\left({expr_tex}\\right) = {val_tex}",
        f"สรุปผลค่าลิมิต: \\lim_{{{v_lat} \\to {a_str}}} \\left({expr_tex}\\right) = {val_tex}",
    ]
    latex_str = f"\\lim_{{{v_lat} \\to {a_str}}} {expr_tex} = {val_tex}"
    return steps, _as_finite_float(_safe_simplify(lim_val)), latex_str


def compute_limit_near(expr_str: str, a: float | int | str | sp.Expr = 0.0) -> dict:
    r"""คำนวณลิมิต x -> a หรือ var -> a (รองรับจำนวนจริง, สัญลักษณ์ pi, e และอนันต์ inf, -inf)

    ลำดับการเฉลยตามหลักการสอน (Pedagogical Hierarchy):
      Level 1 แทนค่าโดยตรง | Level 2 รูปแบบ 0/0 (แยกตัวประกอบ/ตัดทอน)
      Level 3 ลิมิตตรีโกณมิติพื้นฐาน | Level 4 ลิมิตอนันต์ (เส้นกำกับแนวดิ่ง)
      Level 5 ค่าสัมบูรณ์/ฟังก์ชันแบ่งช่วง | Level 6 แกว่งกวัด | Level 7 พฤติกรรมที่อนันต์
    """
    try:
        clean_str, diff_var = _clean_calculus_input(expr_str)
        expr = _parse_input(clean_str)
        if diff_var is not None:
            var_sym = sp.Symbol(diff_var)
        else:
            var_sym = _get_variable(expr)
        v_lat = sp.latex(var_sym)
        a_sp = _parse_target_a(a)

        # ---------------------------------------------------------
        # Level 7: กรณีลิมิตที่อนันต์ var -> +oo หรือ var -> -oo (คงเดิม)
        # ---------------------------------------------------------
        if a_sp in (sp.oo, -sp.oo):
            is_pos_inf = (a_sp == sp.oo)
            dir_tex = "\\infty" if is_pos_inf else "-\\infty"
            x_desc = (
                f"มีค่าเป็นบวกเพิ่มขึ้นอย่างมหาศาล (${v_lat} \\to +\\infty$)"
                if is_pos_inf
                else f"มีค่าเป็นลบลดลงอย่างมหาศาล (${v_lat} \\to -\\infty$)"
            )

            try:
                lim_val = sp.limit(expr, var_sym, a_sp)
            except Exception:
                lim_val = None

            is_oscillating = isinstance(lim_val, AccumulationBounds)
            if is_oscillating:
                status = "dne"
                result = None
                latex_str = f"\\lim_{{{v_lat} \\to {dir_tex}}} {sp.latex(expr)} \\quad \\text{{(does not exist)}}"
                steps = [
                    f"กำหนดโจทย์ลิมิตที่อนันต์: ศึกษาพฤติกรรมระยะไกล (End Behavior) เมื่อตัวแปร ${v_lat}$ {x_desc}\n\\lim_{{{v_lat} \\to {dir_tex}}} \\left({sp.latex(expr)}\\right)",
                    f"การวิเคราะห์พฤติกรรม: ฟังก์ชันมีการแกว่งกวัดขึ้นลงไม่สิ้นสุด (Oscillating) เมื่อ ${v_lat} \\to {dir_tex}$ จึงไม่ลู่เข้าหาค่าคงที่ใด",
                    f"สรุปผล (ไม่มีลิมิตเนื่องจากการแกว่งกวัด): \\lim_{{{v_lat} \\to {dir_tex}}} \\left({sp.latex(expr)}\\right) \\quad \\text{{(does not exist)}}",
                ]
            elif lim_val in (sp.oo, -sp.oo):
                status = "infinite"
                result = None
                latex_str = f"\\lim_{{{v_lat} \\to {dir_tex}}} {sp.latex(expr)} = {sp.latex(lim_val)}"
                steps = [
                    f"กำหนดโจทย์ลิมิตที่อนันต์: ศึกษาพฤติกรรมระยะไกล (End Behavior) เมื่อตัวแปร ${v_lat}$ {x_desc}\n\\lim_{{{v_lat} \\to {dir_tex}}} \\left({sp.latex(expr)}\\right)",
                    f"การวิเคราะห์พฤติกรรม: ค่าฟังก์ชันเพิ่มขึ้น/ลดลงอย่างไม่มีขอบเขต พุ่งไปสู่ ${sp.latex(lim_val)}$",
                    f"สรุปผล (ลิมิตลู่ออกสู่อนันต์): \\lim_{{{v_lat} \\to {dir_tex}}} \\left({sp.latex(expr)}\\right) = {sp.latex(lim_val)}",
                ]
            elif lim_val is not None and getattr(lim_val, "is_finite", False) and getattr(lim_val, "is_real", False):
                status = "finite"
                result = float(lim_val.evalf())
                latex_str = f"\\lim_{{{v_lat} \\to {dir_tex}}} {sp.latex(expr)} = {sp.latex(lim_val)}"
                steps = [
                    f"กำหนดโจทย์ลิมิตที่อนันต์: ศึกษาพฤติกรรมระยะไกล (End Behavior) เมื่อตัวแปร ${v_lat}$ {x_desc}\n\\lim_{{{v_lat} \\to {dir_tex}}} \\left({sp.latex(expr)}\\right)",
                    f"การวิเคราะห์พฤติกรรมและการจัดรูป: เมื่อ ${v_lat} \\to {dir_tex}$ พจน์ที่มีกำลังต่ำกว่าจะถูกครอบงำด้วยพจน์กำลังสูงสุด ส่งผลให้ค่าฟังก์ชันลู่เข้าสู่ค่าคงที่ ${sp.latex(lim_val)}$ เกิดเป็นเส้นกำกับแนวนอน (Horizontal Asymptote) $y = {sp.latex(lim_val)}$",
                    f"พิจารณาค่าลิมิต: \\lim_{{{v_lat} \\to {dir_tex}}} \\left({sp.latex(expr)}\\right) = {sp.latex(lim_val)}",
                    f"สรุปผลค่าลิมิตที่อนันต์ (เส้นกำกับแนวนอน): \\lim_{{{v_lat} \\to {dir_tex}}} \\left({sp.latex(expr)}\\right) = {sp.latex(lim_val)}",
                ]
            else:
                status = "unsupported"
                result = None
                latex_str = f"\\lim_{{{v_lat} \\to {dir_tex}}} {sp.latex(expr)} \\quad \\text{{(unsupported)}}"
                steps = [
                    f"กำหนดโจทย์ลิมิตที่อนันต์: \\lim_{{{v_lat} \\to {dir_tex}}} \\left({sp.latex(expr)}\\right)",
                    "ไม่สามารถสรุปค่าลิมิตที่อนันต์ได้จากข้อมูลการคำนวณในระบบ",
                ]

            return {
                "ok": True,
                "result": result,
                "latex": latex_str,
                "steps": steps,
                "expr": expr,
                "error": None,
                "status": status,
                "left_limit": lim_val if not is_pos_inf else None,
                "right_limit": lim_val if is_pos_inf else None,
                "is_oscillating": is_oscillating,
                "a_sp": a_sp,
                "is_infinite": True,
                "variable": str(var_sym.name),
            }

        # ---------------------------------------------------------
        # กรณีลิมิตเข้าใกล้จุดจำกัด var -> a (ตัวเลขหรือสัญลักษณ์จำกัด)
        # ---------------------------------------------------------
        a_num = float(a_sp.evalf())
        left_real, right_real = _check_real_domain(expr, a_num, var=var_sym)

        try:
            lim_left = sp.limit(expr, var_sym, a_sp, dir="-")
            lim_right = sp.limit(expr, var_sym, a_sp, dir="+")
            status = _classify_limit(lim_left, lim_right)
        except Exception:
            lim_left, lim_right = None, None
            status = "unsupported"

        # ตรวจสอบว่าโดเมนจำนวนจริงมีเพียงฝั่งเดียวหรือไม่ (One-sided Domain Boundary)
        if not left_real and right_real:
            status = "right_only"
        elif left_real and not right_real:
            status = "left_only"

        # ตรวจสอบการแกว่งกวัดความถี่สูง (Oscillating) เช่น sin(1/var)
        is_oscillating = isinstance(lim_left, AccumulationBounds) or isinstance(lim_right, AccumulationBounds)

        a_str = _format_point_str(a_sp)
        a_dir_left = f"\\left({a_str}\\right)^-" if r"\frac" in a_str else f"{a_str}^-"
        a_dir_right = f"\\left({a_str}\\right)^+" if r"\frac" in a_str else f"{a_str}^+"
        s_left_ex, s_right_ex = _format_samples(a_sp)
        expr_tex = sp.latex(expr)

        steps = [
            f"กำหนดโจทย์ลิมิตที่ต้องการหา: ศึกษาพฤติกรรมของค่าฟังก์ชัน $f({v_lat})$ เมื่อค่าตัวแปร ${v_lat}$ ขยับเข้าใกล้จุด ${v_lat} = {a_str}$ (โดยที่ ${v_lat} \\neq {a_str}$)\n\\lim_{{{v_lat} \\to {a_str}}} \\left({expr_tex}\\right)",
        ]
        result = None
        latex_str = f"\\lim_{{{v_lat} \\to {a_str}}} {expr_tex} \\quad \\text{{(unsupported)}}"

        if status == "right_only":
            steps.append(
                f"ข้อสังเกตโดเมน: ฟังก์ชันไม่นิยามบนระบบจำนวนจริงทางซ้ายของ ${v_lat} = {a_str}$ (เช่น รากที่สองหรือลอการิทึม) จึงพิจารณาเฉพาะลิมิตทางขวา (Right-hand Limit) เท่านั้น"
            )
            steps.append(
                f"พิจารณาลิมิตทางขวา: สัญลักษณ์ ${v_lat} \\to {a_dir_right}$ หมายถึงให้ค่า ${v_lat}$ ค่อย ๆ ขยับเข้าใกล้ ${a_str}$ จากฝั่งขวาบนเส้นจำนวน (โดยที่ ${v_lat} > {a_str}$ เช่น ${v_lat} = {s_right_ex} \\dots$)\n\\lim_{{{v_lat} \\to {a_dir_right}}} \\left({expr_tex}\\right) = {sp.latex(lim_right)}"
            )
            if getattr(lim_right, "is_finite", False) and getattr(lim_right, "is_real", False):
                result = float(lim_right)
            latex_str = f"\\lim_{{{v_lat} \\to {a_dir_right}}} {expr_tex} = {sp.latex(lim_right)}"
        elif status == "left_only":
            steps.append(
                f"ข้อสังเกตโดเมน: ฟังก์ชันไม่นิยามบนระบบจำนวนจริงทางขวาของ ${v_lat} = {a_str}$ จึงพิจารณาเฉพาะลิมิตทางซ้าย (Left-hand Limit) เท่านั้น"
            )
            steps.append(
                f"พิจารณาลิมิตทางซ้าย: สัญลักษณ์ ${v_lat} \\to {a_dir_left}$ หมายถึงให้ค่า ${v_lat}$ ค่อย ๆ ขยับเข้าใกล้ ${a_str}$ จากฝั่งซ้ายบนเส้นจำนวน (โดยที่ ${v_lat} < {a_str}$ เช่น ${v_lat} = {s_left_ex} \\dots$)\n\\lim_{{{v_lat} \\to {a_dir_left}}} \\left({expr_tex}\\right) = {sp.latex(lim_left)}"
            )
            if getattr(lim_left, "is_finite", False) and getattr(lim_left, "is_real", False):
                result = float(lim_left)
            latex_str = f"\\lim_{{{v_lat} \\to {a_dir_left}}} {expr_tex} = {sp.latex(lim_left)}"
        elif is_oscillating:
            # Level 6: Oscillating Singularity (คงแนวทางการอธิบายเดิม)
            status = "dne"
            steps.append(
                f"ข้อสังเกตเชิงมโนทัศน์: ฟังก์ชันมีการแกว่งกวัดไม่สิ้นสุด (Oscillating Singularity) ในช่วง $\\langle -1, 1\\rangle$ เมื่อเข้าใกล้จุด ${v_lat} = {a_str}$ ค่าจึงไม่ลู่เข้าหาจำนวนจริงใดจำนวนหนึ่ง"
            )
            steps.append(
                f"สรุปผล (ไม่มีลิมิตเนื่องจากการแกว่งกวัด): \\lim_{{{v_lat} \\to {a_str}}} \\left({expr_tex}\\right) \\quad \\text{{(does not exist)}}"
            )
            result = None
            latex_str = f"\\lim_{{{v_lat} \\to {a_str}}} {expr_tex} \\quad \\text{{(does not exist)}}"
        else:
            # -----------------------------------------------------
            # ลำดับชั้นการเฉลยตามหลักการสอน (Levels 1-5)
            # -----------------------------------------------------
            try:
                f_a = _safe_simplify(expr.subs(var_sym, a_sp))
            except Exception:
                f_a = None
            f_a_num = _as_finite_float(f_a)

            try:
                num_e, den_e = sp.fraction(sp.together(expr))
            except Exception:
                num_e, den_e = expr, sp.Integer(1)
            try:
                num_at = num_e.subs(var_sym, a_sp)
            except Exception:
                num_at = None
            try:
                den_at = den_e.subs(var_sym, a_sp)
            except Exception:
                den_at = None
            is_00 = _is_zero_expr(num_at) and _is_zero_expr(den_at)

            try:
                has_abs = bool(expr.atoms(sp.Abs))
            except Exception:
                has_abs = False
            try:
                has_piecewise = bool(expr.atoms(sp.Piecewise))
            except Exception:
                has_piecewise = False
            is_jump = has_abs or has_piecewise
            sides_infinite = (lim_left in (sp.oo, -sp.oo)) or (lim_right in (sp.oo, -sp.oo))

            if is_jump:
                # Level 5: ค่าสัมบูรณ์ / ฟังก์ชันแบ่งช่วง
                body_steps, result, latex_str = _steps_abs_piecewise(
                    expr, a_str, v_lat, lim_left, lim_right,
                    a_dir_left, a_dir_right, s_left_ex, s_right_ex, has_abs,
                )
                steps += body_steps
            elif status == "finite" and f_a_num is not None:
                # Level 1: แทนค่าโดยตรง
                body_steps, result, latex_str = _steps_direct_substitution(expr, a_str, v_lat, f_a)
                steps += body_steps
            elif status == "finite":
                trig_pair = _detect_special_trig_limit(expr, var_sym, a_sp)
                if trig_pair is not None:
                    # Level 3: ลิมิตตรีโกณมิติพื้นฐาน
                    g, L_val = trig_pair
                    body_steps, result, latex_str = _steps_special_trig(expr, a_str, v_lat, g, L_val)
                    steps += body_steps
                elif is_00:
                    # Level 2: รูปแบบยังไม่กำหนด 0/0 -> แยกตัวประกอบ/ตัดทอน
                    body_steps, result, latex_str = _steps_indeterminate_factoring(
                        expr, var_sym, a_sp, a_str, v_lat, lim_left,
                    )
                    steps += body_steps
                else:
                    try:
                        lim_val = sp.limit(expr, var_sym, a_sp)
                    except Exception:
                        lim_val = lim_left
                    body_steps, result, latex_str = _steps_generic_finite(expr, a_str, v_lat, lim_val)
                    steps += body_steps
            elif status == "infinite" or (status == "dne" and sides_infinite):
                # Level 4: ลิมิตอนันต์ / เส้นกำกับแนวดิ่ง
                body_steps, result, latex_str = _steps_infinite_asymptote(
                    expr, a_str, v_lat, lim_left, lim_right,
                    a_dir_left, a_dir_right, s_left_ex, s_right_ex,
                )
                steps += body_steps
            elif status == "dne":
                steps.append(
                    f"สรุปผล (ไม่มีลิมิตสองด้านเนื่องจากลิมิตซ้ายไม่เท่ากับลิมิตขวา): เส้นกราฟจากฝั่งซ้ายและฝั่งขวาแยกออกจากกันและไม่มาบรรจบกันที่จุดเดียวกัน\n\\lim_{{{v_lat} \\to {a_dir_left}}} f({v_lat}) = {sp.latex(lim_left)} \\neq \\lim_{{{v_lat} \\to {a_dir_right}}} f({v_lat}) = {sp.latex(lim_right)}\n\\lim_{{{v_lat} \\to {a_str}}} \\left({expr_tex}\\right) \\quad \\text{{(does not exist)}}"
                )
                result = None
                latex_str = f"\\lim_{{{v_lat} \\to {a_str}}} {expr_tex} \\quad \\text{{(does not exist)}}"
            else:
                steps.append("ไม่สามารถสรุปค่าลิมิตสองด้านได้จากข้อมูลการคำนวณในระบบ")
                result = None

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
            "a_sp": a_sp,
            "a_str": a_str,
            "a_dir_left": a_dir_left,
            "a_dir_right": a_dir_right,
            "is_infinite": False,
            "variable": str(var_sym.name),
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
