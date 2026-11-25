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


def test_interactive_plotly_functions():
    from utils.plotter import (
        plot_riemann_plotly,
        plot_tangent_plotly,
        plot_limit_plotly,
        plot_volume_plotly,
        plot_improper_plotly,
        plot_area_between_plotly,
    )
    x = sp.Symbol("x")

    fig_riemann = plot_riemann_plotly(x**2, 0.0, 2.0, n=5, method="midpoint", exact=8/3)
    assert fig_riemann is not None
    assert len(fig_riemann.data) >= 2

    fig_tangent = plot_tangent_plotly(x**2, 1.0, slope=2.0)
    assert fig_tangent is not None
    assert len(fig_tangent.data) >= 2

    fig_limit = plot_limit_plotly((x**2 - 1)/(x - 1), 1.0, delta=0.2)
    assert fig_limit is not None
    assert len(fig_limit.data) >= 2

    fig_vol = plot_volume_plotly(sp.sqrt(x), 0.0, 1.0, method="washer", inner_expr=x**2)
    assert fig_vol is not None
    assert len(fig_vol.data) >= 4

    fig_improper = plot_improper_plotly(1/x**2, 1.0, "oo")
    assert fig_improper is not None
    assert len(fig_improper.data) >= 2

    fig_area = plot_area_between_plotly(x, x**2, 0.0, 1.0, crossings=[0.0, 1.0])
    assert fig_area is not None
    assert len(fig_area.data) >= 3


def test_plot_tangent_invalid_inputs_raise_value_error():
    from utils.plotter import plot_tangent, plot_tangent_plotly
    x = sp.Symbol("x")

    # Invalid non-numeric point a
    with pytest.raises(ValueError, match="ไม่สามารถแปลงจุดสัมผัส"):
        plot_tangent(x**2, "invalid_point")
    with pytest.raises(ValueError, match="ไม่สามารถแปลงจุดสัมผัส"):
        plot_tangent_plotly(x**2, "invalid_point")

    # Point not in real domain of f(a)
    with pytest.raises(ValueError, match="ไม่สามารถคำนวณพิกัด f"):
        plot_tangent(1 / x, 0.0)
    with pytest.raises(ValueError, match="ไม่สามารถคำนวณพิกัด f"):
        plot_tangent_plotly(1 / x, 0.0)


def test_plot_limit_invalid_inputs_raise_value_error():
    from utils.plotter import plot_limit_near, plot_limit_plotly
    x = sp.Symbol("x")

    # Invalid unparseable point a
    with pytest.raises(ValueError, match="ไม่สามารถแปลงจุดเข้าใกล้"):
        plot_limit_near(x**2, "not_a_number")
    with pytest.raises(ValueError, match="ไม่สามารถแปลงจุดเข้าใกล้"):
        plot_limit_plotly(x**2, "not_a_number")



