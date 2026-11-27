import sympy as sp

from utils.sympy_solver import compute_limit
from utils.tangent_solver import compute_tangent


def test_oscillatory_limit_explains_nonexistent_one_sided_limits():
    result = compute_limit("sin(1/x)", 0)
    assert result["ok"] is True
    assert result["status"] == "dne"
    assert result["result"] is None
    assert result["left_limit"] == result["right_limit"]
    steps = " ".join(result["steps"])
    assert "oscillat" in steps.lower() or "แกว่ง" in steps
    assert "\\neq \\lim" not in steps
    assert "limsup" in steps.lower() or "liminf" in steps.lower() or "ลิมิตทางซ้ายไม่มี" in steps


def test_jump_limit_still_explains_unequal_one_sided_limits():
    result = compute_limit("1/x", 0)
    assert result["ok"] is True
    assert result["status"] == "dne"
    assert result["result"] is None
    assert result["left_limit"] == -sp.oo
    assert result["right_limit"] == sp.oo
    assert "\\neq" in " ".join(result["steps"])


def test_direct_and_composite_tangent_derivations():
    direct = compute_tangent("sin(x)", 0)
    assert direct["ok"] is True
    assert direct["result"] == 1.0
    direct_steps = " ".join(direct["steps"])
    assert "\\cos(x)" in direct_steps

    composite = compute_tangent("sin(x**2)", 1)
    assert composite["ok"] is True
    assert abs(composite["result"] - float(2 * sp.cos(1))) < 1e-12
    composite_steps = " ".join(composite["steps"])
    assert "x^{2}" in composite_steps or "x**2" in composite_steps
    assert "2 x" in composite_steps or "2*x" in composite_steps
    assert "\\cos" in composite_steps
    assert "ลูกโซ่" in composite_steps


def test_mixed_one_sided_oscillation_preserves_finite_side():
    result = compute_limit("(1+sign(x))*sin(1/x)", 0)
    assert result["status"] == "dne"
    assert result["result"] is None
    assert result["left_limit"] == 0
    assert result["right_limit"] == sp.AccumBounds(-2, 2)
    steps = "\n".join(result["steps"])
    compact = "".join(steps.split())
    assert r"\lim_{x\to0^-}f(x)=0" in compact
    assert "ลิมิตทางขวาไม่มี" in steps
    assert "ลิมิตทางซ้ายไม่มี" not in steps
    assert "ค่าในแต่ละด้านไม่เข้าใกล้จำนวนเดียว" not in steps


def test_chain_rule_groups_additive_inner_derivative():
    result = compute_tangent("sin(x**2+x)", 1)
    assert result["ok"] is True
    assert abs(result["result"] - float(3 * sp.cos(2))) < 1e-12
    step = result["steps"][2]
    assert r"\cdot 2 x + 1" not in step
    assert r"\cdot \left(2 x + 1\right)" in step


def test_improper_trig_interior_singularity():
    from utils.improper_solver import compute_improper
    res = compute_improper("tan(x)", 0, float(sp.pi))
    assert res["ok"] is True
    assert res["status"] == "divergent"
    assert len(res["interior_singularities"]) >= 1


def test_area_between_interior_singularity_rejected():
    from utils.area_solver import compute_area_between
    res = compute_area_between("1/(x-2)", "0", 0, 3)
    assert res["ok"] is False
    assert res["result"] is None
    assert "ไม่ต่อเนื่อง" in res["error"]


def test_substitution_arctan_not_forced_into_fake_usub():
    from utils.substitution_solver import solve_substitution
    res = solve_substitution("1/(x**2+1)")
    assert res["ok"] is True
    assert res["method"] == "standard"
    assert res["u_candidate"] is None
    assert "atan" in str(res["result"])


def test_math_06_no_duplicate_piecewise_simplifier():
    import inspect
    import utils.area_solver as area_module

    source = inspect.getsource(area_module)
    assert source.count("def _simplify_piecewise_on_interval") == 1


def test_math_04_area_between_no_absolute_values_in_crossing_formula():
    from utils.area_solver import compute_area_between

    res = compute_area_between("x", "x**2", 0, 2)
    assert res["ok"] is True
    assert len(res["crossings"]) >= 1
    # Check that formula step (index 1) does not use |f - g|
    formula_step = res["steps"][1]
    assert "|" not in formula_step
    assert "\\text{บน}" in formula_step or "\\text{ล่าง}" in formula_step
    assert "|" not in res["latex"]


def test_math_12_improper_no_volume_symbol_in_summary():
    from utils.improper_solver import compute_improper

    res = compute_improper("1/sqrt(1-x**2)", -1, 1)
    assert res["ok"] is True
    assert res["status"] == "finite"
    # Ensure no V = volume symbol appears in steps
    steps_text = " ".join(res["steps"])
    assert "$V =" not in steps_text
    assert "V =" not in steps_text


def test_expl_01_tangent_sqrt_zero_not_corner_point():
    from utils.tangent_solver import compute_tangent

    res = compute_tangent("sqrt(x)", 0)
    assert res["ok"] is True
    assert res["status"] == "non_differentiable"
    steps_text = " ".join(res["steps"])
    assert "Corner Point" not in steps_text
    assert "จุดมุมหัก" not in steps_text
    assert "\\infty i" not in steps_text
    assert "ไม่อยู่ในโดเมน" in steps_text or "ไม่นิยาม" in steps_text


def test_expl_03_substitution_ln_x_no_compound_fraction():
    from utils.substitution_solver import solve_substitution

    res = solve_substitution("1/(x*log(x))")
    assert res["ok"] is True
    steps_text = " ".join(res["steps"])
    assert "\\frac{du}{1/x}" not in steps_text
    assert "\\frac{du}{\\frac{1}{x}}" not in steps_text
    assert "dx = x \\, du" in steps_text or "dx = x du" in steps_text or "x du" in steps_text


def test_math_05_improper_plot_scales_beyond_15():
    from utils.plotter import plot_improper, plot_improper_plotly

    expr = sp.sympify("1/(x-1)**2")
    fig, ax = plot_improper(expr, 0.0, 2.0)
    assert fig is not None
    ymin, ymax = ax.get_ylim()
    assert ymax > 15.0

    fig_p = plot_improper_plotly(expr, 0.0, 2.0)
    assert fig_p is not None
    assert fig_p.layout.yaxis.range[1] > 15.0


def test_ped_04_no_informal_diff_word_in_pages_and_utils():
    import glob
    files = glob.glob("pages/*.py") + glob.glob("utils/*.py")
    for f in files:
        with open(f, "r", encoding="utf-8") as fp:
            content = fp.read()
            assert "ดิฟ" not in content, f"Informal word 'ดิฟ' found in {f}"


def test_ped_03_substitution_case_4_option_c_feedback():
    from pathlib import Path
    from streamlit.testing.v1 import AppTest
    sub_page = str(Path(__file__).resolve().parent.parent / "pages" / "substitution.py")
    at = AppTest.from_file(sub_page)
    at.run(timeout=5)
    assert not at.exception
    # Select Case 4
    if at.selectbox:
        sb = at.selectbox[0]
        opt_case4 = [o for o in sb.options if "กรณีที่ 4" in o][0]
        sb.select(opt_case4).run(timeout=5)
        r = at.radio(key="radio_u_case4")
        if r:
            # Select Option C (index 2: Option C indicating incompatible)
            r.set_value(r.options[2]).run(timeout=5)
            assert not at.exception
            assert len(at.warning) >= 1
            assert "ยังไม่ถูกต้อง" in at.warning[0].value
            assert "x = u - 1" in at.warning[0].value


def test_ped_05_no_informal_phrases_in_pages_and_utils():
    import glob
    files = glob.glob("pages/*.py") + glob.glob("utils/*.py")
    informal_phrases = ["ไส้ใน", "เมื่อ x ไม่หมด"]
    for f in files:
        with open(f, "r", encoding="utf-8") as fp:
            content = fp.read()
            for phrase in informal_phrases:
                assert phrase not in content, f"Informal phrase '{phrase}' found in {f}"





