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

# KU-inspired palette (เหมือน stat-distribution-solver)
CURVE = "#105D38"      # เขียวเข้ม
FILL = "#B9D4C4"       # เขียวอ่อน
RECT = "#3D7A56"       # เขียวกลางสำหรับสี่เหลี่ยม
RECT_EDGE = "#105D38"
GRID = "#D8DEE8"
TEXT = "#232a4d"


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
        ys_smooth = f(xs_smooth)

    # sample points ตามวิธี
    if method == "left":
        xs_rect = np.array([a + i * dx for i in range(n)])
    elif method == "right":
        xs_rect = np.array([a + (i + 1) * dx for i in range(n)])
    else:  # midpoint
        xs_rect = np.array([a + (i + 0.5) * dx for i in range(n)])

    with np.errstate(all="ignore"):
        ys_rect = f(xs_rect)

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
        ys_area = f(xs_area)
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


def plot_tangent(expr, a: float) -> tuple:
    """วาดเส้นโค้ง f(x) + เส้นสัมผัสที่จุด a"""
    f = sp.lambdify(X, expr, modules=["numpy"])
    df_expr = sp.diff(expr, X)

    fa_val = None
    slope_val = None
    try:
        sub_fa = expr.subs(X, a)
        if sub_fa.is_real and sub_fa.is_number:
            fa_val = float(sub_fa)
        sub_slope = df_expr.subs(X, a)
        if sub_slope.is_real and sub_slope.is_number:
            slope_val = float(sub_slope)
    except Exception:
        pass

    x_span = 3.0
    xs = np.linspace(a - x_span, a + x_span, 400)
    with np.errstate(all="ignore"):
        ys = f(xs)

    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.plot(xs, ys, color=CURVE, lw=2.2, label="y = f(x)")

    if fa_val is not None and slope_val is not None and np.isfinite(fa_val) and np.isfinite(slope_val):
        y_tangent = slope_val * (xs - a) + fa_val
        ax.plot(
            xs,
            y_tangent,
            color="#D97706",
            lw=1.8,
            linestyle="--",
            label=f"Tangent at a={a:.2f} (m={slope_val:.2f})",
        )
        ax.plot(
            [a],
            [fa_val],
            marker="o",
            markersize=8,
            color="#DC2626",
            zorder=5,
            label=f"Point ({a:.2f}, {fa_val:.2f})",
        )
        ax.set_title(f"Tangent Line to Curve at x = {a:.2f} (Slope m = {slope_val:.4f})")
    else:
        ax.set_title(f"Curve at x = {a:.2f} (Tangent Undefined)")

    ax.axhline(0, color="#9ca3af", lw=0.8, linestyle=":")
    ax.axvline(0, color="#9ca3af", lw=0.8, linestyle=":")
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.grid(True, color=GRID, lw=0.5)

    finite_ys = ys[np.isfinite(ys)]
    if len(finite_ys) > 0 and fa_val is not None and np.isfinite(fa_val):
        y_min = max(fa_val - 10.0, float(np.percentile(finite_ys, 5)) - 1.0)
        y_max = min(fa_val + 10.0, float(np.percentile(finite_ys, 95)) + 1.0)
        if y_min < y_max:
            ax.set_ylim(y_min, y_max)

    ax.legend(loc="upper left", fontsize=9, framealpha=0.9)
    fig.tight_layout()
    return fig, ax


def plot_limit_near(expr, a: float, delta: float = 0.35) -> tuple:
    """วาดเส้นโค้ง + จุดวิ่งเข้าใกล้ a จากซ้ายและขวา"""
    f = sp.lambdify(X, expr, modules=["numpy"])
    span = 2.5
    xs = np.linspace(a - span, a + span, 500)
    xs = xs[np.abs(xs - a) > 1e-4]

    with np.errstate(all="ignore"):
        ys = f(xs)

    try:
        lim_val = float(sp.limit(expr, X, a))
    except Exception:
        lim_val = None

    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.plot(xs, ys, color=CURVE, lw=2.2, label="y = f(x)")

    x_left = a - delta
    x_right = a + delta
    try:
        y_left = float(f(x_left))
        y_right = float(f(x_right))
        ax.plot([x_left], [y_left], marker=">", markersize=9, color="#2563EB", label=f"Left: x={x_left:.2f}")
        ax.plot([x_right], [y_right], marker="<", markersize=9, color="#D97706", label=f"Right: x={x_right:.2f}")
    except Exception:
        pass

    if lim_val is not None and np.isfinite(lim_val):
        ax.plot([a], [lim_val], marker="o", markersize=8, color="#DC2626", mfc="white", mew=2, label=f"Limit L = {lim_val:.4f}")
        ax.axhline(lim_val, color="#DC2626", linestyle=":", lw=1, alpha=0.7)

    ax.axvline(a, color="#9ca3af", linestyle="--", lw=1.2, label=f"x = {a:.2f}")
    ax.axhline(0, color="#9ca3af", lw=0.8, linestyle=":")

    ax.set_xlabel("x")
    ax.set_ylabel("y")
    title = f"Limit Behavior as x -> {a:.2f}"
    if lim_val is not None and np.isfinite(lim_val):
        title += f" (L = {lim_val:.4f})"
    ax.set_title(title)
    ax.grid(True, color=GRID, lw=0.5)
    ax.legend(loc="best", fontsize=8.5, framealpha=0.9)
    fig.tight_layout()
    return fig, ax


def plot_substitution(expr) -> tuple:
    """วาด f และ F (ถ้าจำเป็น) สำหรับ substitution (TODO)"""
    return _stub_figure("Integration by Substitution")


def plot_volume(expr, a: float, b: float, method: str = "disk") -> tuple:
    """วาดภาพตัดขวางและการหมุนรอบแกน x แบบ Disk/Washer Method"""
    from matplotlib.patches import Ellipse

    f = sp.lambdify(X, expr, modules=["numpy"])
    x_start = min(a, b)
    x_end = max(a, b)
    span = max(x_end - x_start, 1.0)
    x_min = x_start - 0.2 * span
    x_max = x_end + 0.2 * span

    xs_solid = np.linspace(x_start, x_end, 300)
    xs_ext = np.linspace(x_min, x_max, 400)

    with np.errstate(all="ignore"):
        ys_solid = f(xs_solid)
        ys_ext = f(xs_ext)

    fig, ax = plt.subplots(figsize=(8, 4.5))

    # เส้นขอบบนและเส้นสะท้อนขอบล่างรอบแกน x
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
    method_title = "Disk Method" if method.lower() == "disk" else "Washer Method"
    ax.set_title(f"Volume of Solid of Revolution ({method_title} on [{a}, {b}])")
    ax.grid(True, color=GRID, lw=0.5)

    finite_ys = ys_solid[np.isfinite(ys_solid)]
    if len(finite_ys) > 0:
        max_r = float(np.max(np.abs(finite_ys))) * 1.35
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
        ys_f_full = f(xs_full)
        ys_g_full = g(xs_full)
        ys_f_area = f(xs_area)
        ys_g_area = g(xs_area)

    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.plot(xs_full, ys_f_full, color=CURVE, lw=2.2, label="y = f(x) (top)")
    ax.plot(xs_full, ys_g_full, color="#2563EB", lw=2.2, linestyle="--", label="y = g(x) (bottom)")

    # แรเงาพื้นที่ระหว่าง f และ g
    ax.fill_between(
        xs_area,
        ys_f_area,
        ys_g_area,
        where=(ys_f_area >= ys_g_area),
        interpolate=True,
        color=CURVE,
        alpha=0.35,
        label="Enclosed Area (f >= g)",
    )
    ax.fill_between(
        xs_area,
        ys_f_area,
        ys_g_area,
        where=(ys_f_area < ys_g_area),
        interpolate=True,
        color="#DC2626",
        alpha=0.25,
        label="Inverted Area (g > f)",
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
        ys = f(xs)

    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.plot(xs, ys, color=CURVE, lw=2.2, label="y = f(x)")

    xs_shade = np.linspace(x_start, t_bound, 300)
    xs_shade = xs_shade[np.abs(xs_shade) > 1e-4]
    with np.errstate(all="ignore"):
        ys_shade = f(xs_shade)

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
