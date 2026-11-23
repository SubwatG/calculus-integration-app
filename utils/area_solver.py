"""utils/area_solver.py : พื้นที่ระหว่างเส้นโค้ง

คำนวณพื้นที่เรขาคณิต A = ∫_a^b |f(x) - g(x)| dx บนช่วงจริงจำกัด [a, b]
พร้อมแสดงขั้นตอนการหาจุดตัด การแบ่งช่วงย่อย และการปลดเครื่องหมายค่าสัมบูรณ์
ตามเกณฑ์ Universal Step Contract
"""
import math
import re
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
    "x": sp.Symbol("x", real=True),
    "e": sp.E,
    "E": sp.E,
    "pi": sp.pi,
    "ln": sp.log,
}

X = sp.Symbol("x", real=True)


def _to_latex(sym_obj, order: str = "none") -> str:
    try:
        lat = sp.latex(sym_obj, inv_trig_style="full", order=order, ln_notation=True)
    except Exception:
        lat = sp.latex(sym_obj, inv_trig_style="full", ln_notation=True)
    lat = lat.replace(r"\log", r"\ln")
    lat = re.sub(r"\\operatorname\{a(sin|cos|tan)\}", r"\\arc\1", lat)
    lat = re.sub(r"\\operatorname\{arc(cot|sec|csc)\}", r"\\arc\1", lat)
    lat = re.sub(r"(?<![a-zA-Z\\])a(sin|cos|tan)(?=\s*[\(\{\[_0-9]|\b)", r"\\arc\1", lat)
    lat = re.sub(r'\\sqrt\[(\d+)\]\{\\left\|\{?([a-zA-Z0-9_]+)\}?\\right\|\}[\s~]*\\operatorname\{sign\}\{\\left\(\2\s*\\right\)\}', r'\\sqrt[\1]{\2}', lat)
    lat = re.sub(r'\\sqrt\[(\d+)\]\{\|([a-zA-Z0-9_]+)\|\}[\s~]*\\operatorname\{sign\}\(\2\)', r'\\sqrt[\1]{\2}', lat)
    lat = re.sub(r'\\sqrt\{\\left\|\{?([a-zA-Z0-9_]+)\}?\\right\|\}[\s~]*\\operatorname\{sign\}\{\\left\(\1\s*\\right\)\}', r'\\sqrt{\1}', lat)
    return lat


def _simplify_piecewise_on_interval(expr: sp.Expr, var: sp.Symbol, left: float, right: float) -> sp.Expr:
    """คลี่คลาย Piecewise ที่เกิดจากการอินทิเกรต real_root ให้เหลือเฉพาะฟังก์ชันที่สอดคล้องกับช่วงจริง"""
    if not expr.has(sp.Piecewise):
        return expr
    mid = (left + right) / 2.0
    def _resolve(node):
        if isinstance(node, sp.Piecewise):
            for e, c in node.args:
                if c is True:
                    return e
                try:
                    if bool(c.subs(var, mid)):
                        return e
                except Exception:
                    pass
            return node.args[0][0]
        return node
    return expr.replace(lambda n: isinstance(n, sp.Piecewise), _resolve)


def _format_evaluated_value(val_sym, val_float: float) -> str:
    """จัดรูปแบบผลลัพธ์การคำนวณ: คืนค่าเป็นเศษส่วนแท้หากมีตัวส่วนเรียบร้อย หรือทศนิยมกระชับ ไม่แสดงเศษส่วนยาวเหยียด"""
    try:
        if isinstance(val_sym, sp.Integer) or (isinstance(val_sym, sp.Rational) and val_sym.q < 5000):
            return _to_latex(val_sym)
        if hasattr(val_sym, "is_rational") and val_sym.is_rational:
            rat = sp.Rational(val_sym)
            if rat.q < 5000:
                return _to_latex(rat)
    except Exception:
        pass
    try:
        lat = _to_latex(val_sym)
        has_huge_digits = any(len(d) > 5 for d in re.findall(r"\d+", lat))
        if not has_huge_digits and lat.count("/") <= 1:
            return lat
    except Exception:
        pass
    return f"{val_float:.4f}"


def _parse_input(expr_str: str) -> sp.Expr:
    clean = (expr_str or "").strip()
    if not clean:
        raise ValueError("Empty input string")
    return parse_expr(clean, transformations=TRANSFORMATIONS, local_dict=LOCAL_MATH_DICT)


def _convert_real_roots(expr: sp.Expr) -> sp.Expr:
    """แปลงเลขชี้กำลังเศษส่วนที่เป็นส่วนคี่ เช่น x**(1/3) ให้เป็น real_root เพื่อรักษาสมบัติจำนวนจริงบนย่านลบ"""
    def _replace(node):
        if isinstance(node, sp.Pow) and isinstance(node.exp, sp.Rational):
            p, q = node.exp.p, node.exp.q
            if q % 2 == 1:
                return sp.real_root(node.base, q) ** p
        return node

    return expr.replace(
        lambda n: isinstance(n, sp.Pow) and isinstance(n.exp, sp.Rational) and n.exp.q % 2 == 1,
        _replace,
    )


def _simplify_piecewise_on_interval(expr: sp.Expr, var: sp.Symbol, left: float, right: float) -> sp.Expr:
    """หากผลลัพธ์การอินทิเกรตมี Piecewise ให้เลือกกิ่งเงื่อนไขที่ครอบคลุมช่วง [left, right]"""
    if expr is None or not isinstance(expr, sp.Basic):
        return expr
    if not expr.has(sp.Piecewise):
        return expr
    mid = (float(left) + float(right)) / 2.0

    def _replace_pw(node):
        if isinstance(node, sp.Piecewise):
            for branch_expr, cond in node.args:
                if cond == True or cond == sp.true:
                    return branch_expr
                try:
                    c_val = cond.subs(var, mid)
                    if c_val == True or c_val == sp.true:
                        return branch_expr
                except Exception:
                    pass
            if node.args:
                return node.args[0][0]
        return node

    try:
        return expr.replace(lambda n: isinstance(n, sp.Piecewise), _replace_pw)
    except Exception:
        return expr


def _to_rational_bound(val: float | int | str) -> sp.Rational:
    try:
        fval = float(val)
        if not math.isfinite(fval):
            raise ValueError(f"Bound must be finite, got {val}")
    except (TypeError, ValueError) as e:
        raise ValueError(f"Invalid bound {val}: {e}")
    return sp.Rational(str(val))


def _format_bound_latex(val: float | int | sp.Rational) -> str:
    """จัดรูปแบบขอบเขตบน/ล่างเป็น LaTeX ที่กระชับและคมชัด"""
    try:
        f = float(val)
        if f.is_integer():
            return str(int(f))
        return f"{f:g}"
    except Exception:
        return _to_latex(val)


def _check_domain_validity(expr: sp.Expr, var: sp.Symbol, a_val: float, b_val: float, n_samples: int = 401) -> bool:
    """ตรวจสอบว่าฟังก์ชันมีค่าจริงและจำกัดตลอดช่วงปิด [a, b]"""
    # 1. ตรวจสอบจุดเอกฐานจากตัวส่วน
    denom = sp.denom(expr.rewrite(sp.cos))
    if denom != 1:
        try:
            for r in sp.solve(denom, var):
                if getattr(r, "is_real", False) and a_val <= float(r) <= b_val:
                    return False
        except Exception:
            pass

    # 2. ตรวจสอบแบบ vector ด้วย numpy lambdify
    try:
        import numpy as np
        import warnings
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            fn = sp.lambdify(var, expr, modules=["numpy", {"real_root": np.cbrt}])
            xs = np.linspace(a_val, b_val, n_samples)
            ys = fn(xs)
            if np.iscomplexobj(ys):
                if np.any(np.abs(np.imag(ys)) > 1e-9):
                    return False
            if not np.all(np.isfinite(ys)) or np.any(np.isnan(ys)):
                return False
            return True
    except Exception:
        pass

    # 3. Fallback จุดต่อจุด
    for i in range(n_samples + 1):
        xv = a_val + (b_val - a_val) * i / n_samples
        try:
            val = expr.subs(var, xv).evalf()
            if getattr(val, "is_infinite", False) or val in (sp.zoo, sp.oo, -sp.oo, sp.nan):
                return False
            c = complex(val)
            if abs(c.imag) > 1e-9 or not math.isfinite(c.real) or abs(c.real) > 1e12:
                return False
        except Exception:
            return False
    return True


def _find_crossings(diff: sp.Expr, a_val: float, b_val: float, var: sp.Symbol = X) -> list[float]:
    """ค้นหาจุดตัด f(x) - g(x) = 0 บนช่วงเปิด (a, b)"""
    roots = []
    # 1. ตรวจสอบรากพหุนาม
    try:
        poly = sp.Poly(diff, var)
        if all(c.is_Rational for c in poly.all_coeffs()):
            poly = poly.set_domain(sp.QQ)
            for r in poly.real_roots():
                rf = float(r)
                if a_val < rf < b_val and not any(abs(rf - ex) < 1e-4 for ex in roots):
                    roots.append(rf)
            return sorted(roots)
    except Exception:
        pass

    # 2. กรณีฟังก์ชันที่มีรากคี่หรือจุด x = 0 อยู่กลางช่วง
    if a_val < 0.0 < b_val and (diff.has(sp.real_root) or diff.has(sp.sign) or diff.has(sp.Abs)):
        roots.append(0.0)

    # 3. สแกนการเปลี่ยนเครื่องหมายด้วยความหนาแน่นสูง (รองรับฟังก์ชันความถี่สูง)
    n_samples = 2401
    try:
        import numpy as np
        import warnings
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            fn = sp.lambdify(var, diff, modules=["numpy", {"real_root": np.cbrt}])
            xs_np = np.linspace(a_val, b_val, n_samples)
            ys_np = fn(xs_np)
            if np.iscomplexobj(ys_np):
                ys_np = np.real_if_close(ys_np)

            for i in range(n_samples - 1):
                y1 = float(ys_np[i])
                y2 = float(ys_np[i + 1])
                x1 = float(xs_np[i])
                x2 = float(xs_np[i + 1])
                if not math.isfinite(y1) or not math.isfinite(y2):
                    continue
                if abs(y1) < 1e-12:
                    if a_val < x1 < b_val and not any(abs(x1 - r) < 1e-4 for r in roots):
                        roots.append(x1)
                elif y1 * y2 < 0.0:
                    xl, xr = x1, x2
                    yl, yr = y1, y2
                    xm = (xl + xr) / 2.0
                    for _ in range(25):
                        xm = (xl + xr) / 2.0
                        try:
                            ym = float(fn(xm))
                        except Exception:
                            break
                        if abs(ym) < 1e-12 or (xr - xl) < 1e-9:
                            break
                        if yl * ym <= 0.0:
                            xr, yr = xm, ym
                        else:
                            xl, yl = xm, ym
                    if a_val < xm < b_val and not any(abs(xm - r) < 1e-4 for r in roots):
                        roots.append(xm)
            if roots:
                return sorted(roots)
    except Exception:
        pass

    # Fallback สแกน 1,001 จุด
    xs = [a_val + (b_val - a_val) * i / 1000.0 for i in range(1001)]
    ys = []
    for xi in xs:
        try:
            val_y = float(diff.subs(var, xi).evalf())
            ys.append(val_y)
        except Exception:
            ys.append(float("nan"))

    for i in range(len(xs) - 1):
        y1, y2 = ys[i], ys[i + 1]
        if math.isnan(y1) or math.isnan(y2):
            continue
        if abs(y1) < 1e-12:
            if a_val < xs[i] < b_val and not any(abs(xs[i] - r) < 1e-4 for r in roots):
                roots.append(float(xs[i]))
        elif y1 * y2 < 0.0:
            xl, xr = float(xs[i]), float(xs[i + 1])
            yl, yr = y1, y2
            xm = (xl + xr) / 2.0
            for _ in range(30):
                xm = (xl + xr) / 2.0
                try:
                    ym = float(diff.subs(var, xm).evalf())
                except Exception:
                    break
                if abs(ym) < 1e-12 or (xr - xl) < 1e-9:
                    break
                if yl * ym <= 0.0:
                    xr, yr = xm, ym
                else:
                    xl, yl = xm, ym
            if a_val < xm < b_val and not any(abs(xm - r) < 1e-4 for r in roots):
                roots.append(xm)

    return sorted(roots)


def find_curve_intersections(f_str: str, g_str: str, span: tuple[float, float] = (-15.0, 15.0)) -> dict:
    """ค้นหาจุดตัด f(x) = g(x) ทั้งหมด เพื่อแสดงให้ผู้ใช้เห็นก่อนเลือกช่วงอินทิเกรต

    วิเคราะห์ว่าเส้นโค้งทั้งสองปิดล้อมพื้นที่จำกัดโดยธรรมชาติหรือไม่
    """
    try:
        f_raw = _parse_input(f_str)
        g_raw = _parse_input(g_str)
        f_expr = _convert_real_roots(f_raw)
        g_expr = _convert_real_roots(g_raw)
        all_free = f_expr.free_symbols | g_expr.free_symbols
        var_sym = list(all_free)[0] if all_free else X
        v_name = var_sym.name
        diff_expr = sp.expand(f_expr - g_expr)

        if diff_expr.is_zero or diff_expr == 0:
            return {
                "ok": True,
                "count": -1,
                "roots": [],
                "roots_latex": [],
                "can_enclose_area": False,
                "natural_bounds": None,
                "sub_intervals": [],
                "message": "เส้นโค้งทั้งสองทับกันพอดีทุกจุด (ไม่มีพื้นที่ปิดล้อมระหว่างเส้นโค้ง)",
                "variable": v_name,
                "f_expr": f_expr,
                "g_expr": g_expr,
                "error": None,
            }

        roots = []
        is_poly = False
        try:
            poly = sp.Poly(diff_expr, var_sym)
            if all(c.is_Rational for c in poly.all_coeffs()):
                is_poly = True
                poly_q = poly.set_domain(sp.QQ)
                for r in poly_q.real_roots():
                    rf = float(r)
                    if not any(abs(rf - ex) < 1e-4 for ex in roots):
                        roots.append(rf)
        except Exception:
            is_poly = False

        if not is_poly or len(roots) < 2 or diff_expr.has(sp.real_root):
            extra = _find_crossings(diff_expr, span[0], span[1], var=var_sym)
            for r in extra:
                if not any(abs(r - ex) < 1e-4 for ex in roots):
                    roots.append(r)

        roots = sorted(roots)
        roots_latex = [_format_bound_latex(r) for r in roots]
        count = len(roots)
        can_enclose = (count >= 2)
        natural_bounds = (roots[0], roots[-1]) if can_enclose else None
        sub_intervals = [(roots[i], roots[i + 1]) for i in range(count - 1)] if can_enclose else []

        if count >= 2:
            r_str = ", ".join(f"${v_name} = {rl}$" for rl in roots_latex)
            msg = f"พบจุดตัด {count} จุดที่ {r_str} เส้นโค้งทั้งสองตัดกันและปิดล้อมพื้นที่จำกัดโดยธรรมชาติ"
        elif count == 1:
            msg = f"พบจุดตัดเพียง 1 จุดที่ ${v_name} = {roots_latex[0]}$ เส้นโค้งไม่ปิดล้อมพื้นที่จำกัดด้วยตัวเองตามธรรมชาติ จำเป็นต้องกำหนดขอบเขต $a$ และ $b$ เพื่อหาพื้นที่ในช่วงที่สนใจ"
        else:
            msg = "ไม่พบจุดตัดระหว่างเส้นโค้งทั้งสอง (กราฟไม่ตัดกัน) จึงไม่เกิดพื้นที่ปิดล้อมโดยธรรมชาติ จำเป็นต้องกำหนดขอบเขต $a$ และ $b$ เพิ่มเติม (เช่น เส้นขอบที่โจทย์กำหนด) เพื่อคำนวณพื้นที่"

        return {
            "ok": True,
            "count": count,
            "roots": roots,
            "roots_latex": roots_latex,
            "can_enclose_area": can_enclose,
            "natural_bounds": natural_bounds,
            "sub_intervals": sub_intervals,
            "message": msg,
            "variable": v_name,
            "f_expr": f_expr,
            "g_expr": g_expr,
            "error": None,
        }
    except Exception as e:
        return {
            "ok": False,
            "count": 0,
            "roots": [],
            "roots_latex": [],
            "can_enclose_area": False,
            "natural_bounds": None,
            "sub_intervals": [],
            "message": f"ไม่สามารถวิเคราะห์จุดตัดได้: {e}",
            "variable": "x",
            "f_expr": None,
            "g_expr": None,
            "error": str(e),
        }


def compute_area_between(f_str: str, g_str: str, a: float, b: float) -> dict:
    """คำนวณพื้นที่เรขาคณิตระหว่างเส้นโค้ง A = ∫_a^b |f(x) - g(x)| dx พร้อมแจกแจงขั้นตอนละเอียด"""
    try:
        a_sp = _to_rational_bound(a)
        b_sp = _to_rational_bound(b)
        if a_sp >= b_sp:
            raise ValueError("ขอบล่าง a ต้องน้อยกว่าขอบบน b")

        a_disp = _format_bound_latex(a_sp)
        b_disp = _format_bound_latex(b_sp)

        f_raw = _parse_input(f_str)
        g_raw = _parse_input(g_str)

        f_expr = _convert_real_roots(f_raw)
        g_expr = _convert_real_roots(g_raw)

        all_free = f_expr.free_symbols | g_expr.free_symbols
        if not all_free:
            var_sym = X
        elif len(all_free) == 1:
            var_sym = list(all_free)[0]
        else:
            if any(s.name == "x" for s in all_free):
                var_sym = [s for s in all_free if s.name == "x"][0]
            else:
                var_sym = sorted(all_free, key=lambda s: s.name)[0]
            extra = all_free - {var_sym}
            if extra:
                raise ValueError(f"พบตัวแปรมากกว่า 1 ตัวแปรในสมการ: {all_free} (กรุณาใช้ตัวแปรเดียวกันสำหรับ f และ g)")

        v_lat = _to_latex(var_sym)
        # กระจายพจน์ผลต่าง ไม่ดึงตัวประกอบออกเป็น x(1-x) เพื่อให้อ่านเข้าใจง่าย
        diff_expr = sp.expand(f_expr - g_expr)

        if diff_expr.is_zero or diff_expr == 0:
            return {
                "ok": True,
                "result": 0.0,
                "latex": f"A = \\int_{{{a_disp}}}^{{{b_disp}}} |{_to_latex(diff_expr, order='none')}| \\, d{v_lat} = 0",
                "steps": [
                    f"กำหนดฟังก์ชัน: $f({v_lat}) = {_to_latex(f_raw, order='none')}, \\quad g({v_lat}) = {_to_latex(g_raw, order='none')}$ บนช่วง $[{a_disp}, {b_disp}]$",
                    f"เส้นโค้งทั้งสองทับกันพอดีทั่วทั้งช่วง: $f({v_lat}) - g({v_lat}) = 0$",
                    "พื้นที่ระหว่างเส้นโค้ง: $A = 0$",
                ],
                "expr": diff_expr,
                "f_expr": f_expr,
                "g_expr": g_expr,
                "crossings": [],
                "error": None,
                "variable": str(var_sym.name),
            }

        # ตรวจสอบความถูกต้องของโดเมนบนช่วงปิด [a, b] (ต้องเป็นจำนวนจริงและมีค่าจำกัดตลอดช่วง)
        if not _check_domain_validity(f_expr, var_sym, float(a_sp), float(b_sp)) or \
           not _check_domain_validity(g_expr, var_sym, float(a_sp), float(b_sp)):
            raise ValueError("ไม่สามารถคำนวณพื้นที่ได้เนื่องจากฟังก์ชันไม่อยู่ในโดเมนของจำนวนจริง หรือมีจุดไม่ต่อเนื่องแบบอนันต์บนช่วงที่กำหนด")

        # -------------------------------------------------------------
        # ค้นหาจุดตัด f(x) - g(x) = 0 ทั้งหมดบนช่วงเปิด (a, b)
        # -------------------------------------------------------------
        interior_roots_sym = []
        is_poly = False
        try:
            poly = sp.Poly(diff_expr, var_sym)
            if all(c.is_Rational for c in poly.all_coeffs()):
                is_poly = True
                poly_q = poly.set_domain(sp.QQ)
                interior_roots_sym = [r for r in poly_q.real_roots() if a_sp < r < b_sp]
        except Exception:
            is_poly = False

        if not is_poly or not interior_roots_sym or diff_expr.has(sp.real_root):
            float_roots = _find_crossings(diff_expr, float(a_sp), float(b_sp), var=var_sym)
            for r in float_roots:
                if not any(abs(float(ir) - r) < 1e-4 for ir in interior_roots_sym):
                    interior_roots_sym.append(sp.Rational(str(round(r, 6))))

        # จุดแบ่งทั้งหมด
        cuts = [a_sp] + sorted(set(interior_roots_sym)) + [b_sp]
        crossings_float = [float(r) for r in cuts[1:-1]]

        sub_steps = []
        total_area = sp.S.Zero
        piece_areas = []

        # หาปฏิยานุพันธ์หลักล่วงหน้าครั้งเดียวเพื่อประสิทธิภาพสูง (ลดเวลาจาก O(N) integrate เหลือ O(1))
        antideriv_f_minus_g = None
        try:
            anti_cand = sp.integrate(diff_expr, var_sym)
            if not anti_cand.has(sp.Integral):
                antideriv_f_minus_g = anti_cand
        except Exception:
            antideriv_f_minus_g = None

        for i, (left, right) in enumerate(zip(cuts, cuts[1:]), start=1):
            left_disp = _format_bound_latex(left)
            right_disp = _format_bound_latex(right)
            mid = (left + right) / 2
            mid_val = diff_expr.subs(var_sym, mid)
            is_pos = True
            try:
                is_pos = (float(mid_val.evalf()) >= 0)
            except Exception:
                is_pos = True

            if is_pos:
                integrand = sp.expand(f_expr - g_expr)
                curve_order_desc = f"$f({v_lat}) \\geq g({v_lat})$ (เส้นโค้ง $f$ อยู่บน $g$)"
                antideriv = antideriv_f_minus_g
            else:
                integrand = sp.expand(g_expr - f_expr)
                curve_order_desc = f"$g({v_lat}) \\geq f({v_lat})$ (เส้นโค้ง $g$ อยู่บน $f$ สลับเป็น $g - f$)"
                antideriv = -antideriv_f_minus_g if antideriv_f_minus_g is not None else None

            piece_integral = None
            if antideriv is not None:
                try:
                    piece_integral = antideriv.subs(var_sym, right) - antideriv.subs(var_sym, left)
                except Exception:
                    piece_integral = None

            if piece_integral is None or piece_integral.has(sp.Integral) or not (
                getattr(piece_integral, "is_real", False) and getattr(piece_integral, "is_finite", False)
            ):
                piece_integral = sp.integrate(integrand, (var_sym, left, right))
                if piece_integral.has(sp.Integral) or not (
                    getattr(piece_integral, "is_real", False) and getattr(piece_integral, "is_finite", False)
                ):
                    piece_integral = sp.Integral(integrand, (var_sym, left, right)).evalf()

            try:
                num_val = complex(piece_integral.evalf())
                if abs(num_val.imag) > 1e-9:
                    raise ValueError("ผลการอินทิเกรตไม่เป็นจำนวนจริง (ฟังก์ชันอยู่นอกโดเมนของจำนวนจริง)")
            except ValueError:
                raise
            except Exception:
                pass

            piece_area = abs(piece_integral)
            total_area += piece_area
            piece_areas.append(piece_area)

            if len(cuts) <= 9 or i <= 3 or i == len(cuts) - 1:
                piece_float = float(piece_area.evalf() if hasattr(piece_area, "evalf") else piece_area)
                piece_disp = _format_evaluated_value(piece_area, piece_float)
                if antideriv is None:
                    antideriv = sp.integrate(integrand, var_sym)
                if not antideriv.has(sp.Integral):
                    antideriv = _simplify_piecewise_on_interval(antideriv, var_sym, float(left), float(right))
                    anti_lat = _to_latex(antideriv, order="none")
                    sub_steps.append(
                        f"ช่วงย่อยที่ {i} $[{left_disp}, {right_disp}]$ ({curve_order_desc}): "
                        f"$A_{i} = \\int_{{{left_disp}}}^{{{right_disp}}} \\left({_to_latex(integrand, order='none')}\\right) \\, d{v_lat} = \\left[ {anti_lat} \\right]_{{{left_disp}}}^{{{right_disp}}} = {piece_disp}$"
                    )
                else:
                    sub_steps.append(
                        f"ช่วงย่อยที่ {i} $[{left_disp}, {right_disp}]$ ({curve_order_desc}): "
                        f"$A_{i} = \\int_{{{left_disp}}}^{{{right_disp}}} \\left({_to_latex(integrand, order='none')}\\right) \\, d{v_lat} = {piece_disp}$"
                    )
            elif i == 4 and len(cuts) > 9:
                sub_steps.append(f"... (คำนวณช่วงย่อยที่ 4 ถึง {len(cuts) - 2} ในลักษณะเดียวกัน) ...")

        res_float = float(total_area.evalf() if hasattr(total_area, "evalf") else total_area)
        total_disp = _format_evaluated_value(total_area, res_float)

        # -------------------------------------------------------------
        # สร้าง Steps ตาม Universal Step Contract
        # -------------------------------------------------------------
        if crossings_float:
            formula_step = (
                f"ตั้งสูตรหาพื้นที่:\n"
                f"A = \\int_{{{a_disp}}}^{{{b_disp}}} |f({v_lat}) - g({v_lat})| \\, d{v_lat}\n"
                f"(เนื่องจากเส้นโค้งตัดกันภายในช่วง จึงต้องหาจุดตัดเพื่อแบ่งช่วงย่อย และนำฟังก์ชันบนลบฟังก์ชันล่างในแต่ละช่วงย่อย)"
            )
            latex_ans = f"A = \\int_{{{a_disp}}}^{{{b_disp}}} |{_to_latex(diff_expr, order='none')}| \\, d{v_lat} = {total_disp}"
        else:
            mid_full = (a_sp + b_sp) / 2
            mid_val = diff_expr.subs(var_sym, mid_full)
            try:
                is_top = (float(mid_val.evalf()) >= 0)
            except Exception:
                is_top = True
            if is_top:
                formula_step = (
                    f"ตั้งสูตรหาพื้นที่:\n"
                    f"A = \\int_{{{a_disp}}}^{{{b_disp}}} [f({v_lat}) - g({v_lat})] \\, d{v_lat}\n"
                    f"(เส้นโค้ง $f$ อยู่เหนือ $g$ ตลอดช่วง จึงคำนวณ $|f({v_lat}) - g({v_lat})| = f({v_lat}) - g({v_lat})$)"
                )
                latex_ans = f"A = \\int_{{{a_disp}}}^{{{b_disp}}} \\left[{_to_latex(f_raw, order='none')} - ({_to_latex(g_raw, order='none')})\\right] \\, d{v_lat} = {total_disp}"
            else:
                formula_step = (
                    f"ตั้งสูตรหาพื้นที่:\n"
                    f"A = \\int_{{{a_disp}}}^{{{b_disp}}} [g({v_lat}) - f({v_lat})] \\, d{v_lat}\n"
                    f"(เส้นโค้ง $g$ อยู่เหนือ $f$ ตลอดช่วง จึงคำนวณ $|f({v_lat}) - g({v_lat})| = g({v_lat}) - f({v_lat})$)"
                )
                latex_ans = f"A = \\int_{{{a_disp}}}^{{{b_disp}}} \\left[{_to_latex(g_raw, order='none')} - ({_to_latex(f_raw, order='none')})\\right] \\, d{v_lat} = {total_disp}"

        steps = [
            f"กำหนดฟังก์ชันและช่วงที่พิจารณา: บนช่วง $[{a_disp}, {b_disp}]$\nf({v_lat}) = {_to_latex(f_raw, order='none')}, \\quad g({v_lat}) = {_to_latex(g_raw, order='none')}",
            formula_step,
            f"หาผลต่างของฟังก์ชัน:\nf({v_lat}) - g({v_lat}) = {_to_latex(diff_expr, order='none')}",
        ]

        if crossings_float:
            roots_str = ", ".join(f"${v_lat} = {_format_bound_latex(r)}$" for r in cuts[1:-1])
            steps.append(
                f"หาจุดตัดของเส้นโค้ง: แก้สมการ $f({v_lat}) - g({v_lat}) = 0$ พบจุดตัดภายในช่วงที่ {roots_str} "
                f"จึงแบ่งการคำนวณออกเป็น {len(cuts) - 1} ช่วงย่อยเพื่อนำฟังก์ชันบนลบฟังก์ชันล่างในแต่ละช่วง"
            )
            steps.extend(sub_steps)
            # รวมผลบวกทุกช่วงย่อย
            if len(cuts) <= 9:
                sum_str = " + ".join(f"A_{i}" for i in range(1, len(cuts)))
                pieces_val_str = " + ".join(f"{_format_evaluated_value(p, float(p.evalf()))}" for p in piece_areas)
                steps.append(
                    f"รวมพื้นที่ทุกช่วงย่อย: $A = {sum_str} = {pieces_val_str} = {total_disp}$"
                )
            else:
                sum_str = f"A_1 + A_2 + A_3 + \\dots + A_{{{len(cuts)-1}}}"
                first_vals = " + ".join(f"{_format_evaluated_value(piece_areas[k], float(piece_areas[k].evalf()))}" for k in range(3))
                last_val = f"{_format_evaluated_value(piece_areas[-1], float(piece_areas[-1].evalf()))}"
                steps.append(
                    f"รวมพื้นที่ทุกช่วงย่อย: $A = {sum_str} = {first_vals} + \\dots + {last_val} = {total_disp}$"
                )
        else:
            # ไม่มีจุดตัดภายในช่วง
            mid_full = (a_sp + b_sp) / 2
            mid_val = diff_expr.subs(var_sym, mid_full)
            try:
                is_pos = (float(mid_val.evalf()) >= 0)
            except Exception:
                is_pos = True
            if is_pos:
                integrand = sp.expand(f_expr - g_expr)
                steps.append(
                    f"ตรวจสอบฟังก์ชันบน-ล่างและหาจุดตัด: แก้สมการ $f({v_lat}) - g({v_lat}) = 0$ ไม่พบจุดตัดภายในช่วงเปิด $({a_disp}, {b_disp})$ "
                    f"โดยบนช่วงนี้ $f({v_lat}) \\geq g({v_lat})$ (กราฟ $f$ อยู่เหนือ $g$ ตลอดช่วง) "
                    f"จึงคำนวณปริพันธ์เส้นบนลบเส้นล่าง: $f({v_lat}) - g({v_lat}) = {_to_latex(integrand, order='none')}$"
                )
            else:
                integrand = sp.expand(g_expr - f_expr)
                steps.append(
                    f"ตรวจสอบฟังก์ชันบน-ล่างและหาจุดตัด: แก้สมการ $f({v_lat}) - g({v_lat}) = 0$ ไม่พบจุดตัดภายในช่วงเปิด $({a_disp}, {b_disp})$ "
                    f"โดยบนช่วงนี้ $g({v_lat}) \\geq f({v_lat})$ (เส้นโค้ง $g$ อยู่เหนือ $f$ ตลอดช่วง) "
                    f"จึงคำนวณปริพันธ์เส้นบนลบเส้นล่าง: $g({v_lat}) - f({v_lat}) = {_to_latex(integrand, order='none')}$"
                )

            antideriv = sp.integrate(integrand, var_sym)
            if not antideriv.has(sp.Integral):
                antideriv = _simplify_piecewise_on_interval(antideriv, var_sym, float(a_sp), float(b_sp))
                anti_lat = _to_latex(antideriv, order="none")
                steps.append(
                    f"คำนวณปริพันธ์บนช่วง:\nA = \\int_{{{a_disp}}}^{{{b_disp}}} \\left({_to_latex(integrand, order='none')}\\right) \\, d{v_lat} = \\left[ {anti_lat} \\right]_{{{a_disp}}}^{{{b_disp}}} = {total_disp}"
                )
            else:
                steps.append(
                    f"คำนวณปริพันธ์บนช่วง:\nA = \\int_{{{a_disp}}}^{{{b_disp}}} \\left({_to_latex(integrand, order='none')}\\right) \\, d{v_lat} = {total_disp}"
                )

        steps.append(
            f"สรุปผลลัพธ์: พื้นที่รวม $A = {total_disp} \\approx {res_float:.6g}$ ตารางหน่วย"
        )

        return {
            "ok": True,
            "result": res_float,
            "latex": latex_ans,
            "steps": steps,
            "expr": diff_expr,
            "f_expr": f_expr,
            "g_expr": g_expr,
            "crossings": crossings_float,
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
            "f_expr": None,
            "g_expr": None,
            "crossings": [],
            "error": f"ไม่สามารถคำนวณได้: {e}",
        }
