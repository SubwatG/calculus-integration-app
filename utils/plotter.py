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
    """วาดเส้นโค้ง f(x) + เส้นสัมผัสที่จุด a (TODO)"""
    return _stub_figure(f"Tangent line at a = {a}")


def plot_limit_near(expr, a: float) -> tuple:
    """วาดเส้นโค้ง + จุดวิ่งเข้าใกล้ a (TODO)"""
    return _stub_figure(f"Limit as x -> {a}")


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
