"""
utils/plotter.py — ฟังก์ชันวาดกราฟสำหรับบทเรียน interactive แคลคูลัส

ใช้ matplotlib (Agg) คืน (fig, ax) สำหรับ st.pyplot
label ในกราฟเป็นภาษาอังกฤษ เพื่อความน่าเชื่อถือของ matplotlib
สีอ้างอิงจาก stat-distribution-solver/modules/theme.py (KU green palette)
"""

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import numpy as np
import sympy as sp

from utils.riemann_solver import X

# Playful Bauhaus Pop Palette (Geometric, Vibrant & Crisp)
CURVE = "#E11D48"      # Bauhaus Vibrant Rose / Magenta
FILL = "#FCE7F3"       # Soft Pastel Pink Shading
RECT = "#FDE047"       # Bauhaus Sunny Yellow for Riemann blocks
RECT_EDGE = "#18181B"  # Crisp Black Geometric Edge
GRID = "#E2E8F0"       # Subtle structural grid
TEXT = "#18181B"       # Stark Charcoal Black


def _as_curve(values, xs: np.ndarray) -> np.ndarray:
    """Broadcast scalar or array output to xs shape; keep nonfinite as nan for masked fills."""
    arr = np.asarray(values)
    if np.iscomplexobj(arr):
        arr = np.where(np.imag(arr) == 0, np.real(arr), np.nan)
    arr = np.asarray(arr, dtype=float)
    if arr.ndim == 0:
        arr = np.full(xs.shape, float(arr), dtype=float)
    elif arr.shape != xs.shape:
        arr = np.full(xs.shape, float(arr.flat[0]) if arr.size == 1 else np.nan, dtype=float)
    return np.where(np.isfinite(arr), arr, np.nan)


def plot_riemann(
    expr: sp.Expr,
    a: float,
    b: float,
    n: int,
    method: str = "left",
    exact: float | None = None,
) -> tuple:
    """วาดกราฟ f(x) พร้อมสี่เหลี่ยมผลรวมรีมันน์

    expr: sympy expression (ผ่านการ parse แล้ว)
    a, b: ขอบเขตช่วง
    n: จำนวนสี่เหลี่ยม
    method: left | right | midpoint
    exact: ค่าอินทิกรัลจริง (ถ้ามี) แสดงใน title

    Returns (fig, ax)
    """
    f = sp.lambdify(X, expr, modules=["numpy"])
    dx = (b - a) / n
    pad = (b - a) * 0.05

    xs_smooth = np.linspace(a - pad, b + pad, 400)
    with np.errstate(all="ignore"):
        ys_smooth = _as_curve(f(xs_smooth), xs_smooth)

    # sample points ตามวิธี
    if method == "left":
        xs_rect = np.array([a + i * dx for i in range(n)])
    elif method == "right":
        xs_rect = np.array([a + (i + 1) * dx for i in range(n)])
    else:  # midpoint
        xs_rect = np.array([a + (i + 0.5) * dx for i in range(n)])

    with np.errstate(all="ignore"):
        ys_rect = _as_curve(f(xs_rect), xs_rect)

    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.plot(xs_smooth, ys_smooth, color=CURVE, lw=2, label="y = f(x)")
    ax.axhline(0, color="#999", lw=0.8)

    # สี่เหลี่ยม: ใช้ x ของเหลี่ยมนั้นเป็นฐาน
    for i in range(n):
        if method == "left":
            x0 = a + i * dx
        elif method == "right":
            x0 = a + i * dx  # right ใช้ความสูงขอบขวา แต่เหลี่ยมเริ่มที่ x0
        else:
            x0 = a + i * dx
        y = ys_rect[i]
        rect = Rectangle(
            (x0, 0),
            dx,
            y,
            linewidth=1,
            edgecolor=RECT_EDGE,
            facecolor=RECT,
            alpha=0.35,
        )
        ax.add_patch(rect)

    # แรเงาพื้นที่ใต้กราฟจริง (สำหรับเทียบกับ exact)
    xs_area = np.linspace(a, b, 300)
    with np.errstate(all="ignore"):
        ys_area = _as_curve(f(xs_area), xs_area)
    ax.fill_between(
        xs_area,
        ys_area,
        0,
        color=FILL,
        alpha=0.55,
        label="Exact area ∫f(x)dx",
    )

    ax.set_xlabel("x")
    ax.set_ylabel("y")
    method_label = {"left": "Left", "right": "Right", "midpoint": "Midpoint"}[method]
    title = f"Riemann Sum ({method_label}, n={n}, Δx={dx:.4f})"
    if exact is not None:
        title += f"   | exact={exact:.6f}"
    ax.set_title(title)
    ax.grid(True, color=GRID, lw=0.5)
    ax.legend(loc="upper right", fontsize=9)
    fig.tight_layout()
    return fig, ax


# ---------------------------------------------------------------------------
# Plotter stubs สำหรับบทเรียน interactive ที่นักศึกษาจะเติม
# TODO: ใส่ logic วาดกราฟจริงให้แต่ละฟังก์ชัน (อ้างอิง plot_riemann ข้างบน)
# ข้อควรจำ: label ในกราฟต้องเป็นภาษาอังกฤษเท่านั้น (matplotlib ไม่มีฟอนต์ไทย)
# ---------------------------------------------------------------------------

def _stub_figure(title: str) -> tuple:
    """สร้าง fig เปล่าที่มี title ระบุ TODO (กันหน้าเว็บพังก่อน implement)"""
    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.text(
        0.5, 0.5,
        f"{title}\n(TODO: ยังไม่ implement กราฟนี้)",
        ha="center", va="center", fontsize=12, color="#9ca3af",
        transform=ax.transAxes,
    )
    ax.axis("off")
    fig.tight_layout()
    return fig, ax


def plot_tangent(
    expr: sp.Expr,
    a: float,
    span: float = 3.0,
    slope: float | None = None,
    status: str = "finite",
) -> tuple:
    """วาดกราฟ f(x) และเส้นสัมผัสที่จุด x = a

    expr: sympy expression
    a: จุดที่ต้องการสัมผัส
    span: ความกว้างช่วงรอบจุด a
    slope: ความชันของเส้นสัมผัส (ถ้ามี)
    status: สถานะเส้นสัมผัส (finite, vertical, non_differentiable, undefined_point)
    """
    f = sp.lambdify(X, expr, modules=["numpy"])

    fa_sym = expr.subs(X, a)
    try:
        fa = float(fa_sym)
    except (TypeError, ValueError):
        fa = 0.0

    if slope is None and status == "finite":
        df = sp.diff(expr, X)
        slope_sym = df.subs(X, a)
        try:
            slope = float(slope_sym)
        except (TypeError, ValueError):
            slope = 0.0

    x_min = a - span
    x_max = a + span
    xs = np.linspace(x_min, x_max, 400)

    with np.errstate(all="ignore"):
        ys = _as_curve(f(xs), xs)
        ys = np.where(np.abs(ys) > 1e4, np.nan, ys)

    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.plot(xs, ys, color=CURVE, lw=2.5, label="y = f(x)")

    if status == "vertical":
        ax.axvline(
            a,
            color="#D96B27",
            lw=2,
            linestyle="--",
            label=f"Vertical Tangent at x={a:.2f}",
        )
        title_str = f"Vertical Tangent at x = {a:.2f}  |  Slope m = ∞"
    elif status == "non_differentiable":
        title_str = f"Non-Differentiable at x = {a:.2f} (Corner Point)"
    elif status == "finite" and slope is not None:
        ys_tangent = slope * (xs - a) + fa
        ax.plot(
            xs,
            ys_tangent,
            color="#D96B27",
            lw=2,
            linestyle="--",
            label=f"Tangent at x={a:.2f} (m={slope:.2f})",
        )
        title_str = f"Tangent Line at x = {a:.2f}  |  Slope m = {slope:.4f}"
    else:
        title_str = f"Point at x = {a:.2f}"

    point_label = f"Point ({a:.2f}, {fa:.2f})"
    if status == "non_differentiable":
        point_label += " (Corner)"
    ax.scatter(
        [a],
        [fa],
        color="#C0392B",
        s=65,
        zorder=5,
        label=point_label,
    )

    ax.axhline(0, color="#999", lw=0.8, linestyle=":")
    ax.axvline(0, color="#999", lw=0.8, linestyle=":")

    y_valid = ys[np.isfinite(ys)]
    if len(y_valid) > 0:
        y_low = min(fa - span, float(np.percentile(y_valid, 5)))
        y_high = max(fa + span, float(np.percentile(y_valid, 95)))
        pad = max(1.0, (y_high - y_low) * 0.15)
        ax.set_ylim(y_low - pad, y_high + pad)

    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_title(title_str)
    ax.grid(True, color=GRID, lw=0.5)
    ax.legend(loc="best", fontsize=9)
    fig.tight_layout()
    return fig, ax


def plot_limit_near(expr: sp.Expr, a: float, delta: float = 0.5, span: float = 3.0) -> tuple:
    """วาดเส้นโค้ง + จุดวิ่งเข้าใกล้ a ทั้งสองด้าน (delta -> 0)

    expr: sympy expression
    a: จุดที่ต้องการหาลิมิต
    delta: ระยะห่างการเข้าใกล้จากซ้ายและขวา
    span: ความกว้างช่วงรอบจุด a
    """
    f = sp.lambdify(X, expr, modules=["numpy"])
    lim_sym = sp.limit(expr, X, a)

    try:
        lim_val = float(lim_sym)
        lim_finite = np.isfinite(lim_val)
    except (TypeError, ValueError):
        lim_val = None
        lim_finite = False

    x_min = a - span
    x_max = a + span
    # หลีกเลี่ยงจุด a เล็กน้อยเพื่อป้องกัน division by zero ของ numerical evaluation
    xs_left = np.linspace(x_min, a - 1e-4, 200)
    xs_right = np.linspace(a + 1e-4, x_max, 200)
    xs = np.concatenate([xs_left, xs_right])

    with np.errstate(all="ignore"):
        ys = _as_curve(f(xs), xs)
        ys = np.where(np.abs(ys) > 1e4, np.nan, ys)

    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.plot(xs, ys, color=CURVE, lw=2.5, label="y = f(x)")

    # เส้นแนวดิ่งที่ x = a
    ax.axvline(a, color="#9ca3af", lw=1.2, linestyle="--", label=f"x = {a:.2f}")
    ax.axhline(0, color="#999", lw=0.8, linestyle=":")

    # จุดเป้าหมายลิมิตที่ x = a
    if lim_finite and lim_val is not None:
        ax.plot(
            [a],
            [lim_val],
            marker="o",
            markersize=8,
            markerfacecolor="white",
            markeredgecolor="#C0392B",
            markeredgewidth=2,
            zorder=5,
            label=f"Target L = {lim_val:.4f}",
        )
        ax.axhline(lim_val, color="#E5E7EB", lw=1, linestyle=":")

    # จุดเข้าใกล้ทางซ้าย x_L = a - delta และทางขวา x_R = a + delta
    x_l = a - delta
    x_r = a + delta

    try:
        y_l = float(expr.subs(X, x_l))
    except (TypeError, ValueError):
        y_l = None

    try:
        y_r = float(expr.subs(X, x_r))
    except (TypeError, ValueError):
        y_r = None

    if y_l is not None and np.isfinite(y_l):
        ax.scatter([x_l], [y_l], color="#2980B9", s=60, zorder=6, label=f"Left: x={x_l:.2f}")
        if lim_finite and lim_val is not None:
            ax.annotate(
                "",
                xy=(a - 0.05 * delta, lim_val),
                xytext=(x_l, y_l),
                arrowprops=dict(arrowstyle="->", color="#2980B9", lw=1.5),
            )

    if y_r is not None and np.isfinite(y_r):
        ax.scatter([x_r], [y_r], color="#E67E22", s=60, zorder=6, label=f"Right: x={x_r:.2f}")
        if lim_finite and lim_val is not None:
            ax.annotate(
                "",
                xy=(a + 0.05 * delta, lim_val),
                xytext=(x_r, y_r),
                arrowprops=dict(arrowstyle="->", color="#E67E22", lw=1.5),
            )

    ax.set_xlabel("x")
    ax.set_ylabel("y")
    l_str = f"{lim_val:.4f}" if (lim_finite and lim_val is not None) else str(lim_sym)
    ax.set_title(f"Limit as x -> {a:.2f}  |  L = {l_str} (delta = {delta:.2f})")
    ax.grid(True, color=GRID, lw=0.5)
    ax.legend(loc="best", fontsize=9)
    fig.tight_layout()
    return fig, ax


def plot_substitution(expr) -> tuple:
    """วาด f และ F (ถ้าจำเป็น) สำหรับ substitution (TODO)"""
    return _stub_figure("Integration by Substitution")


def plot_volume(
    expr,
    a: float,
    b: float,
    method: str = "disk",
    inner_expr=None,
) -> tuple:
    """วาดภาพตัดขวางและการหมุนรอบแกน x แบบ Disk/Washer Method"""
    from matplotlib.patches import Ellipse

    is_washer = (method or "disk").lower() == "washer" and inner_expr is not None

    f = sp.lambdify(X, expr, modules=["numpy"])
    f_in = None
    if is_washer:
        f_in = sp.lambdify(X, inner_expr, modules=["numpy"])

    x_start = min(a, b)
    x_end = max(a, b)
    span = max(x_end - x_start, 1.0)
    x_min = x_start - 0.2 * span
    x_max = x_end + 0.2 * span

    xs_solid = np.linspace(x_start, x_end, 300)
    xs_ext = np.linspace(x_min, x_max, 400)

    ys_inner = np.zeros_like(xs_solid)
    with np.errstate(all="ignore"):
        ys_solid = _as_curve(f(xs_solid), xs_solid)
        ys_ext = _as_curve(f(xs_ext), xs_ext)
        if is_washer and f_in is not None:
            ys_inner = _as_curve(f_in(xs_solid), xs_solid)

    fig, ax = plt.subplots(figsize=(8, 4.5))

    if is_washer:
        # เส้นขอบนอกและเส้นขอบใน
        ax.plot(xs_solid, ys_solid, color=CURVE, lw=2.2, label="Outer Radius R(x)")
        ax.plot(xs_solid, -ys_solid, color=CURVE, lw=1.8, linestyle="--", label="Reflection -R(x)")
        ax.plot(xs_solid, ys_inner, color="#2563EB", lw=2.0, label="Inner Radius r(x)")
        ax.plot(xs_solid, -ys_inner, color="#2563EB", lw=1.6, linestyle=":", label="Reflection -r(x)")

        # แรเงาเนื้อทรงตันวงแหวน
        ax.fill_between(xs_solid, ys_solid, ys_inner, where=(ys_solid >= ys_inner), color=CURVE, alpha=0.3, label="Solid Washer")
        ax.fill_between(xs_solid, -ys_inner, -ys_solid, where=(ys_solid >= ys_inner), color=CURVE, alpha=0.3)

        # วาดตัวแทนแผ่นวงแหวน (Washer cross-section slice)
        n_slices = 5
        sample_xs = np.linspace(x_start + 0.1 * span, x_end - 0.1 * span, n_slices)
        for sx in sample_xs:
            with np.errstate(all="ignore"):
                sy_out = float(f(sx))
                sy_in = float(f_in(sx)) if f_in is not None else 0.0
            if np.isfinite(sy_out) and abs(sy_out) > 1e-4:
                width = 0.08 * span
                outer_el = Ellipse((sx, 0), width, 2 * abs(sy_out), edgecolor="#D97706", facecolor="#FDE68A", alpha=0.35, lw=1.2)
                ax.add_patch(outer_el)
                if np.isfinite(sy_in) and abs(sy_in) > 1e-4:
                    inner_el = Ellipse((sx, 0), width, 2 * abs(sy_in), edgecolor="#2563EB", facecolor="white", alpha=0.9, lw=1.0)
                    ax.add_patch(inner_el)
    else:
        # เส้นขอบบนและเส้นสะท้อนขอบล่างรอบแกน x (Disk)
        ax.plot(xs_solid, ys_solid, color=CURVE, lw=2.2, label="Radius R(x)")
        ax.plot(xs_solid, -ys_solid, color=CURVE, lw=1.8, linestyle="--", label="Reflection -R(x)")

        # แรเงาเนื้อทรงตันหมุน
        ax.fill_between(xs_solid, ys_solid, -ys_solid, color=CURVE, alpha=0.25, label="Solid of Revolution")

        # วาดตัวแทนแผ่นดิสก์ (Disk cross-section slices)
        n_slices = 5
        sample_xs = np.linspace(x_start + 0.1 * span, x_end - 0.1 * span, n_slices)
        for sx in sample_xs:
            with np.errstate(all="ignore"):
                sy = float(f(sx))
            if np.isfinite(sy) and abs(sy) > 1e-4:
                ax.plot([sx, sx], [-sy, sy], color="#D97706", lw=2, alpha=0.8)
                width = 0.08 * span
                height = 2 * abs(sy)
                ellipse = Ellipse((sx, 0), width, height, edgecolor="#D97706", facecolor="#FDE68A", alpha=0.35, lw=1.2)
                ax.add_patch(ellipse)

    # แกนหมุน x-axis
    ax.axhline(0, color="#DC2626", lw=1.2, linestyle="-.", label="Axis of Revolution (y = 0)")
    ax.axvline(a, color="#9ca3af", lw=1, linestyle=":")
    ax.axvline(b, color="#9ca3af", lw=1, linestyle=":")

    ax.set_xlabel("x")
    ax.set_ylabel("y")
    method_title = "Washer Method" if is_washer else "Disk Method"
    ax.set_title(f"Volume of Solid of Revolution ({method_title} on [{a}, {b}])")
    ax.grid(True, color=GRID, lw=0.5)

    if is_washer:
        all_ys = np.concatenate([ys_solid[np.isfinite(ys_solid)], ys_inner[np.isfinite(ys_inner)]])
    else:
        all_ys = ys_solid[np.isfinite(ys_solid)]

    if len(all_ys) > 0:
        max_r = float(np.max(np.abs(all_ys))) * 1.35
        ax.set_ylim(-max_r, max_r)

    ax.legend(loc="upper right", fontsize=8.5, framealpha=0.9)
    fig.tight_layout()
    return fig, ax


def plot_area_between(f_expr, g_expr, a: float, b: float) -> tuple:
    """วาดเส้นโค้ง 2 เส้น f(x) และ g(x) พร้อมแรเงาพื้นที่ระหว่างเส้นโค้งบนช่วง [a, b]"""
    f = sp.lambdify(X, f_expr, modules=["numpy"])
    g = sp.lambdify(X, g_expr, modules=["numpy"])

    x_start = min(a, b)
    x_end = max(a, b)
    span = max(x_end - x_start, 1.0)
    x_min = x_start - 0.25 * span
    x_max = x_end + 0.25 * span

    xs_full = np.linspace(x_min, x_max, 400)
    xs_area = np.linspace(x_start, x_end, 300)

    with np.errstate(all="ignore"):
        ys_f_full = _as_curve(f(xs_full), xs_full)
        ys_g_full = _as_curve(g(xs_full), xs_full)
        ys_f_area = _as_curve(f(xs_area), xs_area)
        ys_g_area = _as_curve(g(xs_area), xs_area)

    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.plot(xs_full, ys_f_full, color=CURVE, lw=2.2, label="y = f(x)")
    ax.plot(xs_full, ys_g_full, color="#2563EB", lw=2.2, linestyle="--", label="y = g(x)")

    # แรเงาพื้นที่ระหว่าง f และ g
    ax.fill_between(
        xs_area,
        ys_f_area,
        ys_g_area,
        where=(ys_f_area >= ys_g_area),
        interpolate=True,
        color=CURVE,
        alpha=0.35,
        label="Area (f >= g)",
    )
    ax.fill_between(
        xs_area,
        ys_f_area,
        ys_g_area,
        where=(ys_f_area < ys_g_area),
        interpolate=True,
        color="#DC2626",
        alpha=0.25,
        label="Area (g > f)",
    )

    ax.axvline(a, color="#9ca3af", linestyle=":", lw=1.2, label=f"x = {a}")
    ax.axvline(b, color="#9ca3af", linestyle=":", lw=1.2, label=f"x = {b}")
    ax.axhline(0, color="#9ca3af", lw=0.8, linestyle=":")

    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_title(f"Area Between Curves on [{a}, {b}]")
    ax.grid(True, color=GRID, lw=0.5)

    all_ys = np.concatenate([ys_f_area, ys_g_area])
    finite_ys = all_ys[np.isfinite(all_ys)]
    if len(finite_ys) > 0:
        ymin = float(np.percentile(finite_ys, 2)) - 0.5
        ymax = float(np.percentile(finite_ys, 98)) + 0.5
        if ymin < ymax:
            ax.set_ylim(ymin, ymax)

    ax.legend(loc="upper right", fontsize=8.5, framealpha=0.9)
    fig.tight_layout()
    return fig, ax


def plot_improper(expr, a: float, b: float | None = None) -> tuple:
    """วาดเส้นโค้งและพื้นที่ใต้กราฟของอินทิกรัลไม่ตรงแบบ (Improper Integral)"""
    f = sp.lambdify(X, expr, modules=["numpy"])

    is_infinite_upper = (b is None)
    if is_infinite_upper:
        x_start = a
        x_end = a + 8.0
        t_bound = a + 5.0
    else:
        x_start = min(a, b)
        x_end = max(a, b) + 1.0
        t_bound = b

    xs = np.linspace(x_start, x_end, 500)
    xs = xs[np.abs(xs) > 1e-4]

    with np.errstate(all="ignore"):
        ys = _as_curve(f(xs), xs)

    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.plot(xs, ys, color=CURVE, lw=2.2, label="y = f(x)")

    xs_shade = np.linspace(x_start, t_bound, 300)
    xs_shade = xs_shade[np.abs(xs_shade) > 1e-4]
    with np.errstate(all="ignore"):
        ys_shade = _as_curve(f(xs_shade), xs_shade)

    ax.fill_between(
        xs_shade,
        ys_shade,
        0,
        color=CURVE,
        alpha=0.35,
        label=f"Area over [{a}, t] as t -> ∞" if is_infinite_upper else f"Area over [{a}, {b}]",
    )

    ax.axvline(a, color="#9ca3af", lw=1.2, linestyle="--", label=f"Lower Bound a = {a}")
    if is_infinite_upper:
        ax.axvline(t_bound, color="#D97706", lw=1.2, linestyle=":", label=f"Sample Bound t = {t_bound:.1f}")
        ax.annotate(
            "t → ∞",
            xy=(t_bound, 0.2),
            xytext=(t_bound + 1.2, 0.4),
            arrowprops=dict(facecolor="#D97706", edgecolor="#D97706", arrowstyle="->", lw=1.5),
            fontsize=10,
            color="#D97706",
            fontweight="bold",
        )
    else:
        ax.axvline(b, color="#DC2626", lw=1.2, linestyle="--", label=f"Upper Bound b = {b}")

    ax.axhline(0, color="#9ca3af", lw=0.8, linestyle=":")
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    title = f"Improper Integral on [{a}, ∞)" if is_infinite_upper else f"Improper Integral on [{a}, {b}]"
    ax.set_title(title)
    ax.grid(True, color=GRID, lw=0.5)

    finite_ys = ys_shade[np.isfinite(ys_shade)]
    if len(finite_ys) > 0:
        ymin = max(-1.0, float(np.percentile(finite_ys, 1)) - 0.5)
        ymax = min(15.0, float(np.percentile(finite_ys, 98)) + 1.0)
        if ymin < ymax:
            ax.set_ylim(ymin, ymax)

    ax.legend(loc="upper right", fontsize=8.5, framealpha=0.9)
    fig.tight_layout()
    return fig, ax
