import matplotlib.pyplot as plt
import pytest
import sympy as sp
from utils.plotter import (
    plot_area_between,
    plot_riemann,
    plot_improper,
    plot_volume,
)


@pytest.mark.parametrize("f,g", [("x", "0"), ("5", "0"), ("3", "1")])
def test_constant_curves_have_matching_shapes(f, g):
    fig, ax = plot_area_between(sp.sympify(f), sp.sympify(g), -1.0, 1.0)
    try:
        for line in ax.lines[:2]:
            assert len(line.get_xdata()) == len(line.get_ydata())
            assert len(line.get_xdata()) > 1
        assert ax.collections
    finally:
        plt.close(fig)


def test_plot_riemann_constant():
    fig, ax = plot_riemann(sp.sympify("3"), 0.0, 2.0, n=4, method="left")
    try:
        assert fig is not None and ax is not None
    finally:
        plt.close(fig)


def test_plot_improper_constant():
    fig, ax = plot_improper(sp.sympify("1"), 1.0, 2.0)
    try:
        assert fig is not None and ax is not None
    finally:
        plt.close(fig)


def test_plot_volume_constant():
    fig, ax = plot_volume(sp.sympify("2"), 0.0, 3.0, method="disk")
    try:
        assert fig is not None and ax is not None
    finally:
        plt.close(fig)


def test_plot_volume_washer():
    fig, ax = plot_volume(
        sp.sympify("sqrt(x)"),
        0.0,
        1.0,
        method="washer",
        inner_expr=sp.sympify("x**2"),
    )
    try:
        assert fig is not None and ax is not None
        assert len(ax.lines) >= 4
    finally:
        plt.close(fig)


def test_plotter_supports_arbitrary_variables():
    from utils.plotter import plot_tangent, plot_limit_near
    t = sp.Symbol("t")
    y = sp.Symbol("y")
    u = sp.Symbol("u")

    fig1, ax1 = plot_riemann(t**2, 0.0, 2.0, n=4)
    assert ax1.get_xlabel() == "t"
    plt.close(fig1)

    fig2, ax2 = plot_area_between(t, t**2, 0.0, 1.0)
    assert ax2.get_xlabel() == "t"
    plt.close(fig2)

    fig3, ax3 = plot_tangent(y**3, 1.0)
    assert ax3.get_xlabel() == "y"
    plt.close(fig3)

    fig4, ax4 = plot_limit_near(sp.sin(u) / u, 0.0)
    assert ax4.get_xlabel() == "u"
    plt.close(fig4)

    fig5, ax5 = plot_volume(y, 0.0, 2.0, method="disk")
    assert ax5.get_xlabel() == "y"
    plt.close(fig5)

