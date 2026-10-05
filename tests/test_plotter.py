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
