"""utils/area_solver.py: Area between curves solver.

Computes geometric area A = ∫_a^b |f(x) - g(x)| dx on bounded real interval [a, b],
providing step-by-step intersection finding, subinterval splitting, and sign analysis
under the Universal Step Contract.
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


def _format_evaluated_value(val_sym, val_float: float) -> str:
    """Format evaluated value concisely as exact fraction or short decimal."""
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
        raise ValueError("กรุณาระบุฟังก์ชัน (ข้อความเป็นค่าว่าง)")
    return parse_expr(clean, transformations=TRANSFORMATIONS, local_dict=LOCAL_MATH_DICT)


def _convert_real_roots(expr: sp.Expr) -> sp.Expr:
    """Convert odd-denominator fractional powers (e.g. x**(1/3)) to real_root for real branch."""
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
    """Select the Piecewise branch that covers the subinterval [left, right]."""
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
    except (TypeError, ValueError):
        raise ValueError(f"ขอบเขตต้องเป็นตัวเลขจริง (เช่น 0 ถึง 3.14) ระบบอ่านค่า '{val}' ไม่ได้")
    if not math.isfinite(fval):
        raise ValueError(f"ขอบเขตต้องเป็นจำนวนจริงจำกัด (ได้รับ '{val}')")
    try:
        return sp.Rational(str(val))
    except Exception:
        return sp.Rational(str(fval))


def _format_bound_latex(val: float | int | sp.Rational) -> str:
    """Format upper/lower integration bound as concise LaTeX."""
    try:
        f = float(val)
        if f.is_integer():
            return str(int(f))
        return f"{f:g}"
    except Exception:
        return _to_latex(val)


def _check_domain_validity(expr: sp.Expr, var: sp.Symbol, a_val: float, b_val: float, n_samples: int = 401) -> bool:
    """Check that function values are real and finite across the closed interval [a, b]."""
    # 1. Check poles and denominator roots
    denom = sp.denom(expr.rewrite(sp.cos))
    if denom != 1:
        try:
            for r in sp.solve(denom, var):
                if getattr(r, "is_real", False) and a_val <= float(r) <= b_val:
                    return False
        except Exception:
            pass

    # 2. Vectorized check using numpy lambdify
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

    # 3. Pointwise fallback check
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
    """Find intersection points f(x) - g(x) = 0 on open interval (a, b)."""
    roots = []
    # 1. Check polynomial real roots
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

    # 2. Odd-degree root or x = 0 origin crossing
    if a_val < 0.0 < b_val and (diff.has(sp.real_root) or diff.has(sp.sign) or diff.has(sp.Abs)):
        roots.append(0.0)

    # 3. Dense sign-change scan (supports high-frequency functions)
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

    # Fallback 1,001-point scan
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


def _eval_interval_sign(diff_expr: sp.Expr, var_sym: sp.Symbol, left: sp.Rational, right: sp.Rational) -> int:
    """Evaluate sign of diff_expr on open interval (left, right).

    Returns 1 if strictly positive, -1 if strictly negative, or falls back to testing offsets.
    """
    mid = (left + right) / 2
    try:
        val = float(diff_expr.subs(var_sym, mid).evalf())
        if abs(val) > 1e-12:
            return 1 if val > 0 else -1
    except Exception:
        pass
    # If midpoint is zero or near-zero (e.g. at tangency root), test quarter points
    for fraction in (0.25, 0.75, 0.1, 0.9):
        pt = left + (right - left) * fraction
        try:
            val = float(diff_expr.subs(var_sym, pt).evalf())
            if abs(val) > 1e-12:
                return 1 if val > 0 else -1
        except Exception:
            pass
    return 1


def _classify_interior_roots(
    diff_expr: sp.Expr,
    var_sym: sp.Symbol,
    a_sp: sp.Rational,
    b_sp: sp.Rational,
    interior_roots: list[sp.Rational],
) -> tuple[list[sp.Rational], list[sp.Rational]]:
    """Classify interior roots into true crossings (sign change) and tangency points (no sign change)."""
    sorted_roots = sorted(set(interior_roots))
    if not sorted_roots:
        return [], []

    z_points = [a_sp] + sorted_roots + [b_sp]
    interval_signs = [
        _eval_interval_sign(diff_expr, var_sym, z_points[i], z_points[i + 1])
        for i in range(len(z_points) - 1)
    ]

    true_crossings = []
    tangent_points = []
    for i, r in enumerate(sorted_roots):
        s_left = interval_signs[i]
        s_right = interval_signs[i + 1]
        if s_left * s_right < 0:
            true_crossings.append(r)
        else:
            tangent_points.append(r)

    return true_crossings, tangent_points


def find_curve_intersections(f_str: str, g_str: str, span: tuple[float, float] = (-15.0, 15.0)) -> dict:
    """Find all curve intersection points f(x) = g(x) to assist user in selecting bounds.

    Analyzes whether the two curves enclose a naturally bounded region.
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
    """Compute geometric area between curves A = ∫_a^b |f(x) - g(x)| dx with detailed steps."""
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
        # Expand difference expression without factoring for clear readability
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

        # Validate domain on closed interval [a, b] (must be real and finite throughout)
        if not _check_domain_validity(f_expr, var_sym, float(a_sp), float(b_sp)) or \
           not _check_domain_validity(g_expr, var_sym, float(a_sp), float(b_sp)):
            raise ValueError("ไม่สามารถคำนวณพื้นที่ได้เนื่องจากฟังก์ชันไม่อยู่ในโดเมนของจำนวนจริง หรือมีจุดไม่ต่อเนื่องแบบอนันต์บนช่วงที่กำหนด")

        # -------------------------------------------------------------
        # Find all intersection points f(x) - g(x) = 0 on open interval (a, b)
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

        # Classify interior roots into true crossings (sign change) and tangency points (no sign change)
        true_crossings_sym, tangent_points_sym = _classify_interior_roots(
            diff_expr, var_sym, a_sp, b_sp, interior_roots_sym
        )

        # Definite integral subintervals are split strictly at true crossings
        cuts = [a_sp] + sorted(set(true_crossings_sym)) + [b_sp]
        crossings_float = [float(r) for r in true_crossings_sym]
        tangent_points_float = [float(r) for r in tangent_points_sym]

        sub_steps = []
        total_area = sp.S.Zero
        piece_areas = []

        # Precompute antiderivative once for performance (reduces O(N) integrate to O(1))
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
            sign_interval = _eval_interval_sign(diff_expr, var_sym, left, right)
            is_pos = (sign_interval >= 0)

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
        # Build steps according to Universal Step Contract
        # -------------------------------------------------------------
        if crossings_float:
            num_sub = len(cuts) - 1
            if num_sub <= 3:
                sub_sum_sym = " + ".join(
                    f"\\int_{{{_format_bound_latex(cuts[i])}}}^{{{_format_bound_latex(cuts[i+1])}}} (f_{{\\text{{บน}}}} - f_{{\\text{{ล่าง}}}}) \\, d{v_lat}"
                    for i in range(num_sub)
                )
            else:
                sub_sum_sym = f"\\sum_{{i=1}}^{{{num_sub}}} \\int_{{x_{{i}}}}^{{x_{{i+1}}}} (f_{{\\text{{บน}}}} - f_{{\\text{{ล่าง}}}}) \\, d{v_lat}"

            formula_step = (
                f"ตั้งสูตรหาพื้นที่:\n"
                f"A = {sub_sum_sym}\n"
                f"(เนื่องจากเส้นโค้งตัดกันภายในช่วง จึงแบ่งเป็น {num_sub} ช่วงย่อยและนำฟังก์ชันบนลบฟังก์ชันล่างในแต่ละช่วงย่อย)"
            )
            latex_ans = f"A = {sub_sum_sym} = {total_disp}"
        else:
            sign_interval = _eval_interval_sign(diff_expr, var_sym, a_sp, b_sp)
            is_top = (sign_interval >= 0)
            if is_top:
                reason = (
                    f"(เส้นโค้ง $f$ อยู่เหนือหรือสัมผัส $g$ ตลอดช่วง จึงคำนวณ |f({v_lat}) - g({v_lat})| = f({v_lat}) - g({v_lat}))"
                    if tangent_points_float
                    else f"(เส้นโค้ง $f$ อยู่เหนือ $g$ ตลอดช่วง จึงคำนวณ |f({v_lat}) - g({v_lat})| = f({v_lat}) - g({v_lat}))"
                )
                formula_step = (
                    f"ตั้งสูตรหาพื้นที่:\n"
                    f"A = \\int_{{{a_disp}}}^{{{b_disp}}} [f({v_lat}) - g({v_lat})] \\, d{v_lat}\n"
                    f"{reason}"
                )
                latex_ans = f"A = \\int_{{{a_disp}}}^{{{b_disp}}} \\left[{_to_latex(f_raw, order='none')} - ({_to_latex(g_raw, order='none')})\\right] \\, d{v_lat} = {total_disp}"
            else:
                reason = (
                    f"(เส้นโค้ง $g$ อยู่เหนือหรือสัมผัส $f$ ตลอดช่วง จึงคำนวณ |f({v_lat}) - g({v_lat})| = g({v_lat}) - f({v_lat}))"
                    if tangent_points_float
                    else f"(เส้นโค้ง $g$ อยู่เหนือ $f$ ตลอดช่วง จึงคำนวณ |f({v_lat}) - g({v_lat})| = g({v_lat}) - f({v_lat}))"
                )
                formula_step = (
                    f"ตั้งสูตรหาพื้นที่:\n"
                    f"A = \\int_{{{a_disp}}}^{{{b_disp}}} [g({v_lat}) - f({v_lat})] \\, d{v_lat}\n"
                    f"{reason}"
                )
                latex_ans = f"A = \\int_{{{a_disp}}}^{{{b_disp}}} \\left[{_to_latex(g_raw, order='none')} - ({_to_latex(f_raw, order='none')})\\right] \\, d{v_lat} = {total_disp}"

        steps = [
            f"กำหนดฟังก์ชันและช่วงที่พิจารณา: บนช่วง $[{a_disp}, {b_disp}]$\nf({v_lat}) = {_to_latex(f_raw, order='none')}, \\quad g({v_lat}) = {_to_latex(g_raw, order='none')}",
            formula_step,
            f"หาผลต่างของฟังก์ชัน:\nf({v_lat}) - g({v_lat}) = {_to_latex(diff_expr, order='none')}",
        ]

        if crossings_float:
            roots_str = ", ".join(f"${v_lat} = {_format_bound_latex(r)}$" for r in true_crossings_sym)
            if tangent_points_sym:
                tang_str = ", ".join(f"${v_lat} = {_format_bound_latex(r)}$" for r in tangent_points_sym)
                note_tang = f" (และพบจุดสัมผัสที่ไม่ตัดสลับฝั่งที่ {tang_str})"
            else:
                note_tang = ""
            steps.append(
                f"หาจุดตัดของเส้นโค้ง: แก้สมการ $f({v_lat}) - g({v_lat}) = 0$ พบจุดตัดสลับฝั่งภายในช่วงที่ {roots_str}{note_tang} "
                f"จึงแบ่งการคำนวณออกเป็น {len(cuts) - 1} ช่วงย่อยเพื่อนำฟังก์ชันบนลบฟังก์ชันล่างในแต่ละช่วง"
            )
            steps.extend(sub_steps)
            # Sum all sub-interval areas
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
            # No interior crossings
            sign_interval = _eval_interval_sign(diff_expr, var_sym, a_sp, b_sp)
            is_pos = (sign_interval >= 0)
            if is_pos:
                integrand = sp.expand(f_expr - g_expr)
                if tangent_points_float:
                    tang_str = ", ".join(f"${v_lat} = {_format_bound_latex(r)}$" for r in tangent_points_sym)
                    steps.append(
                        f"ตรวจสอบฟังก์ชันบน-ล่างและหาจุดตัด: แก้สมการ $f({v_lat}) - g({v_lat}) = 0$ พบจุดสัมผัสที่ {tang_str} "
                        f"โดยเส้นโค้งสัมผัสกันแต่ไม่ตัดสลับฝั่ง ทำให้ $f({v_lat}) \\geq g({v_lat})$ ตลอดช่วง "
                        f"จึงไม่ต้องแบ่งช่วงย่อย และคำนวณปริพันธ์เส้นบนลบเส้นล่าง: $f({v_lat}) - g({v_lat}) = {_to_latex(integrand, order='none')}$"
                    )
                else:
                    steps.append(
                        f"ตรวจสอบฟังก์ชันบน-ล่างและหาจุดตัด: แก้สมการ $f({v_lat}) - g({v_lat}) = 0$ ไม่พบจุดตัดภายในช่วงเปิด $({a_disp}, {b_disp})$ "
                        f"โดยบนช่วงนี้ $f({v_lat}) \\geq g({v_lat})$ (กราฟ $f$ อยู่เหนือ $g$ ตลอดช่วง) "
                        f"จึงคำนวณปริพันธ์เส้นบนลบเส้นล่าง: $f({v_lat}) - g({v_lat}) = {_to_latex(integrand, order='none')}$"
                    )
            else:
                integrand = sp.expand(g_expr - f_expr)
                if tangent_points_float:
                    tang_str = ", ".join(f"${v_lat} = {_format_bound_latex(r)}$" for r in tangent_points_sym)
                    steps.append(
                        f"ตรวจสอบฟังก์ชันบน-ล่างและหาจุดตัด: แก้สมการ $f({v_lat}) - g({v_lat}) = 0$ พบจุดสัมผัสที่ {tang_str} "
                        f"โดยเส้นโค้งสัมผัสกันแต่ไม่ตัดสลับฝั่ง ทำให้ $g({v_lat}) \\geq f({v_lat})$ ตลอดช่วง "
                        f"จึงไม่ต้องแบ่งช่วงย่อย และคำนวณปริพันธ์เส้นบนลบเส้นล่าง: $g({v_lat}) - f({v_lat}) = {_to_latex(integrand, order='none')}$"
                    )
                else:
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
            "touch_points": tangent_points_float,
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
