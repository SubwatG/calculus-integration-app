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


def plot_tangent(expr: sp.Expr, a: float, span: float = 3.0) -> tuple:
    """วาดเส้นโค้ง f(x) + เส้นสัมผัสที่จุด a

    expr: sympy expression
    a: จุดที่ต้องการสัมผัส
    span: ความกว้างช่วงรอบจุด a
    """
    df = sp.diff(expr, X)
    f = sp.lambdify(X, expr, modules=["numpy"])

    fa_sym = expr.subs(X, a)
    slope_sym = df.subs(X, a)

    try:
        fa = float(fa_sym)
    except (TypeError, ValueError):
        fa = 0.0

    try:
        slope = float(slope_sym)
    except (TypeError, ValueError):
        slope = 0.0

    x_min = a - span
    x_max = a + span
    xs = np.linspace(x_min, x_max, 400)

    with np.errstate(all="ignore"):
        ys = f(xs)
        if isinstance(ys, (int, float)):
            ys = np.full_like(xs, ys)
        else:
            ys = np.where(np.abs(ys) > 1e4, np.nan, ys)

    ys_tangent = slope * (xs - a) + fa

    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.plot(xs, ys, color=CURVE, lw=2.5, label="y = f(x)")
    ax.plot(
        xs,
        ys_tangent,
        color="#D96B27",
        lw=2,
        linestyle="--",
        label=f"Tangent at x={a:.2f} (m={slope:.2f})",
    )
    ax.scatter(
        [a],
        [fa],
        color="#C0392B",
        s=65,
        zorder=5,
        label=f"Point ({a:.2f}, {fa:.2f})",
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
    ax.set_title(f"Tangent Line at x = {a:.2f}  |  Slope m = {slope:.4f}")
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
        ys = f(xs)
        if isinstance(ys, (int, float)):
            ys = np.full_like(xs, ys)
        else:
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


def plot_volume(expr, a: float, b: float, method: str = "disk") -> tuple:
    """วาดหน้าตัด/ทรงตันแบบ disk หรือ washer (TODO)"""
    return _stub_figure(f"Volume of Solids ({method}, [{a}, {b}])")


def plot_area_between(f_expr, g_expr, a: float, b: float) -> tuple:
    """วาดเส้นโค้ง 2 เส้น + แรเงาช่องว่างระหว่าง (TODO)"""
    return _stub_figure(f"Area Between Curves on [{a}, {b}]")


def plot_improper(expr, a: float, b: float | None) -> tuple:
    """วาดเส้นโค้ง + ขอบเขตวิ่งเข้าหาจุดไม่ต่อเนื่อง/อนันต์ (TODO)"""
    bound = "inf" if b is None else b
    return _stub_figure(f"Improper Integral on [{a}, {bound}]")
