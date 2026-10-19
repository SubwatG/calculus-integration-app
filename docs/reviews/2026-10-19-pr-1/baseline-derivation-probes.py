"""Classify two derivation findings against the original main snapshot."""
import json
import sys
from pathlib import Path

import sympy as sp

REPORTS = Path(__file__).resolve().parent
PIN = json.loads((REPORTS / "snapshot.json").read_text())
BASE = Path(PIN["snapshot"] + "-main")
sys.path.insert(0, str(BASE))
from utils.sympy_solver import compute_limit
from utils.tangent_solver import compute_tangent

limit = compute_limit("sin(1/x)", 0)
tangent = compute_tangent("sin(x**2)", 1)
left, right = limit["left_limit"], limit["right_limit"]
output = {
    "base_sha": PIN["base"],
    "sources": {
        name: sys.modules[name].__file__
        for name in ("utils.sympy_solver", "utils.tangent_solver")
    },
    "oscillation": {
        "status": limit["status"],
        "result": limit["result"],
        "left": str(left),
        "right": str(right),
        "false_identical_bounds_inequality": bool(
            isinstance(left, sp.AccumBounds)
            and left == right
            and r"\neq" in limit["steps"][-1]
        ),
        "steps": limit["steps"],
    },
    "composite_tangent": {
        "slope": tangent["result"],
        "expected_slope": str(2 * sp.cos(1)),
        "slope_correct": abs(tangent["result"] - float(2 * sp.cos(1))) < 1e-12,
        "chain_rule_named": "ลูกโซ่" in "\n".join(tangent["steps"]),
        "steps": tangent["steps"],
    },
}
(REPORTS / "baseline-derivation-results.json").write_text(
    json.dumps(output, ensure_ascii=False, indent=2, default=str)
)
print(json.dumps({
    "base_sha": output["base_sha"],
    "oscillation_defect_present_in_base": output["oscillation"]["false_identical_bounds_inequality"],
    "tangent_chain_omission_present_in_base": not output["composite_tangent"]["chain_rule_named"],
    "base_slope_correct": output["composite_tangent"]["slope_correct"],
}, indent=2))
