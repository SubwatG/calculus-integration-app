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
    assert "เอกฐาน" in res["error"]


def test_substitution_arctan_not_forced_into_fake_usub():
    from utils.substitution_solver import solve_substitution
    res = solve_substitution("1/(x**2+1)")
    assert res["ok"] is True
    assert res["method"] == "standard"
    assert res["u_candidate"] is None
    assert "atan" in str(res["result"])


