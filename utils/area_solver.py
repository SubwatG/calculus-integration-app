"""utils/area_solver.py — พื้นที่ระหว่างเส้นโค้ง

คำนวณพื้นที่เรขาคณิต A = ∫_a^b |f(x) - g(x)| dx บนช่วงจริงจำกัด [a, b]
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
    "x": sp.Symbol("x", real=True),
    "e": sp.E,
    "E": sp.E,
    "pi": sp.pi,
    "ln": sp.log,
}

X = sp.Symbol("x", real=True)


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


def _to_rational_bound(val: float | int | str) -> sp.Rational:
    try:
        fval = float(val)
        if not math.isfinite(fval):
            raise ValueError(f"Bound must be finite, got {val}")
    except (TypeError, ValueError) as e:
        raise ValueError(f"Invalid bound {val}: {e}")
    return sp.Rational(str(val))


def _format_bound_latex(val: float | int | sp.Rational) -> str:
    """จัดรูปแบบขอบเขตบน/ล่างเป็น LaTeX ที่กระชับและคมชัด (เช่น 0, 1 แทน 0.0, 1.0 และ 1.02 แทน 51/50)"""
    try:
        f = float(val)
        if f.is_integer():
            return str(int(f))
        return f"{f:g}"
    except Exception:
        return sp.latex(val)


def _polynomial_area(diff: sp.Expr, x: sp.Symbol, lower: sp.Rational, upper: sp.Rational) -> sp.Expr:
    try:
        poly = sp.Poly(diff, x)
    except Exception:
        raise ValueError("Not a single-variable polynomial")
    if any(c.is_Rational is not True for c in poly.all_coeffs()):
        raise ValueError("Unsupported polynomial coefficients")
    poly = poly.set_domain(sp.QQ)
    if poly.is_zero:
        return sp.S.Zero
    roots = sorted(set(poly.real_roots()))
    cuts = [lower] + [r for r in roots if lower < r < upper] + [upper]
    primitive = sp.integrate(diff, x)
    total = sp.S.Zero
    for left, right in zip(cuts, cuts[1:]):
        mid = (left + right) / 2
        sign = sp.sign(diff.subs(x, mid))
        if sign not in (sp.S.One, sp.S.NegativeOne):
            raise ValueError("Cannot certify sign on subinterval")
        total += sign * (primitive.subs(x, right) - primitive.subs(x, left))
    return sp.simplify(total)


def _find_crossings(diff: sp.Expr, a_val: float, b_val: float, var: sp.Symbol = X) -> list[float]:
    """ค้นหาจุดตัด f(x) - g(x) = 0 บนช่วงเปิด (a, b) อย่างรวดเร็วและแม่นยำ"""
    roots = []
    # 1. ตรวจสอบรากพหุนามก่อน
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

    # 3. สแกนการเปลี่ยนเครื่องหมายและทำ Bisection
    xs = [a_val + (b_val - a_val) * i / 60.0 for i in range(61)]
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
        if y1 == 0.0:
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


def compute_area_between(f_str: str, g_str: str, a: float, b: float) -> dict:
    """คำนวณพื้นที่เรขาคณิตระหว่างเส้นโค้ง A = ∫_a^b |f(x) - g(x)| dx"""
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

        v_lat = sp.latex(var_sym)
        diff_expr = sp.simplify(f_expr - g_expr)

        if diff_expr.is_zero or diff_expr == 0:
            return {
                "ok": True,
                "result": 0.0,
                "latex": f"A = \\int_{{{a_disp}}}^{{{b_disp}}} |{sp.latex(diff_expr)}| \\, d{v_lat} = 0",
                "steps": [
                    f"กำหนดฟังก์ชัน: f({v_lat}) = {sp.latex(f_raw)}, \\quad g({v_lat}) = {sp.latex(g_raw)}",
                    f"เส้นโค้งทั้งสองทับกันพอดีทั่วทั้งช่วง: f({v_lat}) - g({v_lat}) = 0",
                    "พื้นที่ระหว่างเส้นโค้ง: A = 0",
                ],
                "expr": diff_expr,
                "f_expr": f_expr,
                "g_expr": g_expr,
                "crossings": [],
                "error": None,
                "variable": str(var_sym.name),
            }

        # ตรวจสอบจุดเอกฐานบนโดเมน
        check_pts = [float(a_sp), float(b_sp), (float(a_sp) + float(b_sp)) / 2.0]
        if float(a_sp) < 0.0 < float(b_sp):
            check_pts.append(0.0)
        for pt in check_pts:
            val_pt = diff_expr.subs(var_sym, pt)
            if val_pt in (sp.zoo, sp.oo, -sp.oo) or getattr(val_pt, "is_infinite", False):
                raise ValueError("ไม่สามารถคำนวณพื้นที่จำกัดได้บนช่วงที่กำหนด (พบจุดเอกฐาน หรือไม่อยู่ในโดเมนจำนวนจริง)")

        area_val = None
        roots = []
        sub_steps = []

        # เส้นทางที่ 1: พหุนามสัมประสิทธิ์ตรรกยะ (แม่นยำ 100% ในรูปเศษส่วน)
        try:
            val_poly = _polynomial_area(diff_expr, var_sym, a_sp, b_sp)
            if not val_poly.has(sp.Integral) and getattr(val_poly, "is_real", False) is True and getattr(val_poly, "is_finite", False) is True:
                area_val = val_poly
        except Exception:
            pass

        # เส้นทางที่ 2: ฟังก์ชันทั่วไป / ฟังก์ชันอดิศัย (แยกช่วงตามจุดตัดเพื่อหลีกเลี่ยงการค้างของ symbolic Abs)
        if area_val is None:
            roots = _find_crossings(diff_expr, float(a_sp), float(b_sp), var=var_sym)
            cuts = sorted([float(a_sp)] + roots + [float(b_sp)])

            total_sub = sp.S.Zero
            piece_ok = True
            for i, (l_c, r_c) in enumerate(zip(cuts, cuts[1:]), start=1):
                try:
                    piece_int = sp.integrate(diff_expr, (var_sym, l_c, r_c))
                    if piece_int.has(sp.Integral) or not (
                        getattr(piece_int, "is_real", False) and getattr(piece_int, "is_finite", False)
                    ):
                    # fallback to numerical evaluation on this piece
                        piece_int = sp.Integral(diff_expr, (var_sym, l_c, r_c)).evalf()
                    piece_area = abs(piece_int)
                    total_sub += piece_area
                    sub_steps.append(
                        f"ช่วงย่อยที่ {i} [{l_c:.4g}, {r_c:.4g}]: A_{i} = \\left|\\int_{{{l_c:.4g}}}^{{{r_c:.4g}}} (f({v_lat})-g({v_lat}))\\,d{v_lat}\\right| \\approx {float(piece_area.evalf()):.4g}"
                    )
                except Exception:
                    piece_ok = False
                    break

            if piece_ok and getattr(total_sub, "is_real", False) is True and getattr(total_sub, "is_finite", False) is True:
                area_val = total_sub

        # เส้นทางที่ 3: Numerical Quadrature fallback
        if area_val is None:
            try:
                num = sp.Integral(sp.Abs(diff_expr), (var_sym, a_sp, b_sp)).evalf()
                if getattr(num, "is_real", False) is True and getattr(num, "is_finite", False) is True:
                    area_val = num
            except Exception:
                pass

        if area_val is None or not (getattr(area_val, "is_real", False) is True and getattr(area_val, "is_finite", False) is True):
            raise ValueError("ไม่สามารถคำนวณพื้นที่จำกัดได้บนช่วงที่กำหนด (อาจมีจุดเอกฐาน หรือไม่อยู่ในโดเมนจำนวนจริง)")

        res_float = float(area_val.evalf() if hasattr(area_val, "evalf") else area_val)

        steps = [
            f"กำหนดฟังก์ชัน: f({v_lat}) = {sp.latex(f_raw)}, \\quad g({v_lat}) = {sp.latex(g_raw)}",
            f"ตั้งสูตรอินทิกรัลพื้นที่เรขาคณิต: A = \\int_{{{a_disp}}}^{{{b_disp}}} |f({v_lat}) - g({v_lat})| \\, d{v_lat}",
            f"หาผลต่างของฟังก์ชัน: f({v_lat}) - g({v_lat}) = {sp.latex(diff_expr)}",
        ]

        if roots:
            roots_str = ", ".join(f"{v_lat} \\approx {r:.4g}" for r in roots)
            steps.append(f"พบจุดตัดของเส้นโค้ง f({v_lat}) = g({v_lat}) ภายในช่วงที่: {roots_str}")
            steps.extend(sub_steps)

        steps.append(
            f"คำนวณพื้นที่เรขาคณิตรวม: A = {sp.latex(area_val)} \\approx {res_float:.6g}"
        )

        return {
            "ok": True,
            "result": res_float,
            "latex": f"A = \\int_{{{a_disp}}}^{{{b_disp}}} |{sp.latex(diff_expr)}| \\, d{v_lat} = {sp.latex(area_val)}",
            "steps": steps,
            "expr": diff_expr,
            "f_expr": f_expr,
            "g_expr": g_expr,
            "crossings": roots,
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
