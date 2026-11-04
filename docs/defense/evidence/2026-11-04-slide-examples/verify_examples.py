#!/usr/bin/env python3
"""Recompute slide examples; a successful audit can report manuscript mismatches."""
import ast
from decimal import Decimal, ROUND_HALF_UP
import hashlib
import json
from pathlib import Path
import re

import sympy as sp

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
SOURCE = ROOT / "docs/defense/build_defense_deck.py"
PDF = Path("/home/kitti/Downloads/02-Active/Student-Projects/เล่มโครงงานแคลคูลัส-ฉบับส่งกรรมการ-20261102.pdf")
PDF_HASH = "18b3412fafc841d1ce7b35ca7193dc3a4c3e0165b3f22ea6902ab2c0a51c6a84"
x, h = sp.symbols("x h", real=True)
t = sp.symbols("t", positive=True)
source = SOURCE.read_text()
assert hashlib.sha256(PDF.read_bytes()).hexdigest() == PDF_HASH
nodes = ast.parse(source)
slides = {n.targets[0].id: ast.get_source_segment(source, n) or "" for n in nodes.body
          if isinstance(n, ast.Assign) and isinstance(n.targets[0], ast.Name)
          and re.fullmatch(r"S\d\d", n.targets[0].id)}
checks = []


def equal(name, actual, expected):
    assert actual == expected or sp.simplify(actual - expected) == 0, (name, actual, expected)
    checks.append({"id": name, "actual": str(actual), "expected": str(expected), "pass": True})
    return str(actual)


# Reference transcriptions are from the submitted PDF, not inferred from the slides.
named = []

def case(number, slide, printed, pdf_page, expression, actual, expected, status, note=""):
    value = equal("example-" + number, actual, expected)
    assert "2." + number.split(".")[1] in slides[f"S{slide:02d}"]
    named.append({"example": number, "slide": slide, "printed_page": printed,
                  "pdf_page": pdf_page, "reference_expression": expression,
                  "reference_value": value, "status": status, "note": note})


case("2.2", 12, "8", "21", "limit((x**2-9)/(x-3),x,3)",
     sp.limit((x**2-9)/(x-3), x, 3), 6, "different_problem",
     "Slide uses x->2, (x**2-4)/(x-2), result 4, and cites printed page 10.")
equal("slide12-alternative-limit", sp.limit((x**2-4)/(x-2), x, 2), 4)
for value in [sp.Rational(s) for s in ("1.9", "1.99", "1.999", "2.1", "2.01", "2.001")]:
    equal("slide12-table-" + str(value), ((x*x-4)/(x-2)).subs(x, value), value+2)
case("2.3", 14, "9-10", "22-23", "derivative(x**2,x=1); tangent y=2*x-1",
     sp.limit(((1+h)**2-1)/h, h, 0), 2, "same_problem_wrong_page",
     "Slide cites printed page 12; solution continues on printed page 10.")
equal("slide14-contact-value", (x*x).subs(x, 1), 1)
equal("slide14-tangent", sp.diff(x*x, x).subs(x, 1)*(x-1)+1, 2*x-1)


def riemann(n):
    dx = sp.Rational(2, n)
    return tuple(sp.simplify(sum(((sp.Rational(i)+offset)*dx)**2*dx for i in range(n)))
                 for offset in (0, 1, sp.Rational(1, 2)))


case("2.7", 16, "14", "27", "midpoint(x**2,[0,2],n=8)", riemann(8)[2],
     sp.Rational(85, 32), "extended_not_literal",
     "PDF specifies n=8; slide table instead lists n=4,10,20,50,100.")
equal("reference-midpoint-error", sp.Rational(8,3)-riemann(8)[2], sp.Rational(1,96))
equal("riemann-exact-integral", sp.integrate(x*x, (x, 0, 2)), sp.Rational(8,3))

rows = re.findall(r"<tr><td>(\d+)</td>" + r"<td>([^<]+)</td>"*6 + r"</tr>", slides["S16"])
assert [int(r[0]) for r in rows] == [4, 10, 20, 50, 100]
rounding_issues, table_results = [], []
for row in rows:
    n = int(row[0])
    values = riemann(n)
    for j, (method, value) in enumerate(zip(("left", "right", "midpoint"), values)):
        shown = row[1+2*j]
        rounded = (Decimal(int(sp.numer(value)))/Decimal(int(sp.denom(value)))).quantize(Decimal("0.0001"), rounding=ROUND_HALF_UP)
        assert Decimal(shown) == rounded, (n, method, shown, str(rounded))
        error = sp.simplify(100*(value-sp.Rational(8,3))/sp.Rational(8,3))
        dec_error = Decimal(int(sp.numer(error)))/Decimal(int(sp.denom(error)))
        expected_error = dec_error.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        shown_error = row[2+2*j]
        if "0.01%" in shown_error and ("lt;" in shown_error or "<" in shown_error):
            ok = abs(error) < sp.Rational(1,100)
        else:
            ok = Decimal(shown_error.rstrip("%")) == expected_error
        item = {"n": n, "method": method, "exact": str(value), "display": shown,
                "error_percent_exact": str(error), "error_percent_rounded": str(expected_error),
                "error_display": shown_error, "rounding_ok": bool(ok)}
        table_results.append(item)
        if not ok:
            rounding_issues.append(item)

case("2.8", 18, "17", "30", "antiderivative(2*x*cos(x**2))=sin(x**2)+C",
     sp.diff(sp.sin(x*x), x), 2*x*sp.cos(x*x), "same_problem_wrong_page",
     "Slide cites printed page 15 instead of 17.")
case("2.9", 18, "17", "30", "antiderivative(x*exp(x))=x*exp(x)-exp(x)+C",
     sp.diff(x*sp.exp(x)-sp.exp(x), x), x*sp.exp(x), "same_problem")
case("2.10", 20, "18", "31", "integral(2*x-x**2,0,2)",
     sp.integrate(2*x-x*x, (x,0,2)), sp.Rational(4,3), "same_problem_wrong_page",
     "Slide cites printed page 17 instead of 18.")
case("2.11", 20, "18-19", "31-32", "area(2*x,x**2,[0,2])",
     sp.integrate(2*x-x*x, (x,0,2)), sp.Rational(4,3), "same_problem")
equal("area-intersections", sp.FiniteSet(*sp.solve(2*x-x*x,x)), sp.FiniteSet(0,2))
case("2.12", 22, "19-20", "32-33", "pi*integral(x,0,4)",
     sp.pi*sp.integrate(x,(x,0,4)), 8*sp.pi, "same_problem")
case("2.13", 22, "20-21", "33-34", "pi*integral(x**2-x**4,0,1)",
     sp.pi*sp.integrate(x*x-x**4,(x,0,1)), 2*sp.pi/15, "same_problem")
equal("washer-intersections", sp.FiniteSet(*sp.solve(x-x*x,x)), sp.FiniteSet(0,1))
case("2.14", 24, "22", "35", "integral(1/x**2,1,infinity)",
     sp.limit(sp.integrate(x**-2,(x,1,t)),t,sp.oo), 1, "same_problem")
case("2.15", 24, "23", "36", "integral(1/sqrt(x),0,1)",
     sp.limit(2-2*sp.sqrt(t),t,0,dir="+"), 2, "same_problem")

# Supplementary examples and repeated appearances outside the numbered cards.
supplementary = []
left = sp.limit(sp.Abs(h)/h, h, 0, dir="-")
right = sp.limit(sp.Abs(h)/h, h, 0, dir="+")
equal("corner-left",left,-1); equal("corner-right",right,1)
assert left != right
supplementary.append({"slides":[14,25], "case":"abs(x) at 0", "result":"left=-1,right=1; not differentiable",
                      "provenance":"PDF printed 9 / physical 22 discusses this corner; not example 2.3 itself."})
equal("parts-swapped-identity", sp.diff(x*x*sp.exp(x)/2,x)-x*x*sp.exp(x)/2, x*sp.exp(x))
supplementary.append({"slides":[18], "case":"u=exp(x),dv=x dx", "result":"valid identity, less useful choice",
                      "provenance":"Supplement to example 2.9; algebra alone does not prove software loops."})
f = sp.sin(x)-sp.cos(x)
area = -sp.integrate(f,(x,0,sp.pi/4))+sp.integrate(f,(x,sp.pi/4,5*sp.pi/4))-sp.integrate(f,(x,5*sp.pi/4,2*sp.pi))
equal("trig-area",sp.simplify(area),4*sp.sqrt(2))
for root in (sp.pi/4,5*sp.pi/4): equal("trig-intersection-"+str(root),f.subs(x,root),0)
supplementary.append({"slides":[20],"case":"sin(x) vs cos(x), [0,2*pi]", "result":str(sp.simplify(area)),
                      "provenance":"Supplement, not numbered example 2.10 or 2.11."})
equal("singular-left",sp.limit(sp.log(t),t,0,dir="+"),-sp.oo)
equal("singular-right",sp.limit(-sp.log(t),t,0,dir="+"),sp.oo)
supplementary.append({"slides":[24],"case":"integral(1/x,-1,1)","result":"diverges; principal value is not ordinary integral",
                      "provenance":"Supplement to convergent examples 2.14 and 2.15."})
z=sp.symbols("z",positive=True)
equal("log-positive-component",sp.diff(sp.log(z),z),1/z)
equal("log-negative-component",sp.diff(sp.log(-x),x),1/x)
supplementary.append({"slides":[26],"case":"antiderivative(1/x)=log(abs(x))+C", "result":"valid on each interval avoiding zero",
                      "provenance":"Supplementary misconception example; not assigned a manuscript example number."})
equal("slide25-repeated-area",sp.integrate(2*x-x*x,(x,0,2)),sp.Rational(4,3))
equal("screenshot-area",sp.integrate(x-x*x,(x,0,1)),sp.Rational(1,6))
equal("screenshot-volume",sp.pi*sp.integrate(x*x,(x,0,2)),8*sp.pi/3)
equal("screenshot-riemann-left",riemann(8)[0],sp.Rational(35,16))
equal("screenshot-riemann-right",riemann(8)[1],sp.Rational(51,16))
assert len(named) == 11 and len(supplementary) == 5
result = {"audit_completed":True,"all_examples_match_manuscript":False,
          "scope":"Exact recomputation of stated examples, not application solver or screenshot provenance verification",
          "pdf_path":str(PDF),"pdf_sha256":PDF_HASH,
          "builder_sha256":hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
          "sympy_version":sp.__version__,"named_example_count":len(named),
          "supplementary_case_count":len(supplementary),"exact_check_count":len(checks),
          "named_examples":named,"supplementary":supplementary,"checks":checks,
          "riemann_table":table_results,"rounding_issues":rounding_issues,
          "rounding_policy":"Decimal ROUND_HALF_UP at two decimal places; error=(approx-exact)/exact*100"}
(HERE/"examples-results.json").write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n")
print(json.dumps({k:result[k] for k in ["audit_completed","all_examples_match_manuscript","named_example_count","supplementary_case_count","exact_check_count","rounding_issues"]},ensure_ascii=False,indent=2))
