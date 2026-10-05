"""Build trusted local test fixtures; never parse untrusted user files here."""
import csv
import json
from pathlib import Path
import sympy as sp

OUT = Path(__file__).resolve().parent
x = sp.Symbol('x')
LOCAL = {'x': x, 'e': sp.E, 'pi': sp.pi, 'ln': sp.log}
cases = []


def add(topic, operation, args, expected, *, check='value', domain='R', kind='normal', contract='mathematical'):
    index = len(cases) + 1
    cases.append(dict(id=f'MATH-{index:03d}', topic=topic, operation=operation,
                      args=args, expected=str(expected), check=check, domain=domain,
                      kind=kind, contract=contract, priority='P0' if kind != 'normal' else 'P1',
                      tolerance=1e-9))


# Reference antiderivatives are verified by differentiation below.
for expr, answer, domain in [
    ('0', '0', 'R'), ('7', '7*x', 'R'), ('x', 'x**2/2', 'R'),
    ('x^4', 'x**5/5', 'R'), ('3x^2 - 2x + 1', 'x**3-x**2+x', 'R'),
    ('1/x', 'log(x)', 'x>0; use ln|x| on each real component'),
    ('x^(-2)', '-1/x', 'x!=0'), ('sqrt(x)', '2*x**(3/2)/3', 'x>0'),
    ('e^x', 'exp(x)', 'R'), ('sin(x)', '-cos(x)', 'R'),
    ('cos(x)', 'sin(x)', 'R'), ('1/(1+x^2)', 'atan(x)', 'R'),
    ('1/sqrt(1-x^2)', 'asin(x)', '-1<x<1'),
    ('x*e^x', '(x-1)*exp(x)', 'R'),
    ('ln(x)', 'x*log(x)-x', 'x>0'),
    ('1/(x^2-1)', 'log(x-1)/2-log(x+1)/2', 'x>1; real branches separately'),
]:
    add('basic-and-techniques', 'integrate', [expr], answer, check='antiderivative', domain=domain)
for expr, answer, domain in [
    ('2x*cos(x^2)', 'sin(x**2)', 'R'),
    ('2*x/(1+x^2)', 'log(1+x**2)', 'R'),
    ('3*x^2*e^(x^3)', 'exp(x**3)', 'R'),
    ('cos(x)/sin(x)', 'log(sin(x))', '0<x<pi'),
    ('x/sqrt(1+x^2)', 'sqrt(1+x**2)', 'R'),
    ('x*ln(x)', 'x**2*log(x)/2-x**2/4', 'x>0'),
]:
    add('substitution-and-parts', 'substitution', [expr], answer, check='antiderivative', domain=domain)
for expr, answer, domain in [
    ('5', '0', 'R'), ('x^5', '5*x**4', 'R'),
    ('(x^2+1)*sin(x)', '2*x*sin(x)+(x**2+1)*cos(x)', 'R'),
    ('sin(x^2)', '2*x*cos(x**2)', 'R'),
    ('ln(x)', '1/x', 'x>0'), ('e^(2x)', '2*exp(2*x)', 'R'),
    ('1/x', '-1/x**2', 'x!=0'),
]:
    add('derivative', 'differentiate', [expr], answer, domain=domain)
for expr, point, answer in [
    ('x^2', 2, '4'), ('(x^2-4)/(x-2)', 2, '4'),
    ('sin(x)/x', 0, '1'), ('(e^x-1)/x', 0, '1'),
    ('(sqrt(1+x)-1)/x', 0, '1/2'), ('abs(x)', 0, '0'),
]:
    add('limit', 'limit', [expr, point], answer)
    add('limit', 'limit_near', [expr, point], answer)
for expr, point, answer in [('x^2', 2, '4'), ('sin(x)', 0, '1'),
                             ('e^x', 0, '1'), ('x^3', 0, '0')]:
    add('tangent', 'tangent', [expr, point], answer)
# These are exact finite sums, not definite integrals.
for method in ['left', 'right', 'midpoint']:
    for expr, a, b, n in [('x', 0, 1, 4), ('x^2', 0, 1, 4),
                          ('-2', -1, 2, 3), ('x^2', 0, 1, 10)]:
        offset = {'left': sp.S.Zero, 'right': sp.S.One, 'midpoint': sp.Rational(1, 2)}[method]
        dx = sp.Rational(b-a, n)
        ref_expr = sp.sympify(expr.replace('^', '**'), locals=LOCAL)
        answer = sp.simplify(dx * sum(ref_expr.subs(x, a+(i+offset)*dx) for i in range(n)))
        add('riemann', 'riemann', [expr, a, b, n, method], answer)
for f, g, a, b, answer in [('x', 'x^2', 0, 1, '1/6'),
                          ('2', '0', -1, 1, '4'), ('x^2', '0', 0, 2, '8/3')]:
    add('area', 'area', [f, g, a, b], answer)
for expr, a, b, answer in [('x', 0, 1, 'pi/3'), ('sqrt(x)', 0, 4, '8*pi'),
                           ('2', 0, 3, '12*pi')]:
    add('volume-disk', 'volume', [expr, a, b, 'disk'], answer)
for expr, a, b, answer in [('1/x^2', 1, None, '1'), ('e^(-x)', 0, None, '1'),
                           ('1/sqrt(x)', 0, 1, '2'), ('1/x^2', 1, 2, '1/2')]:
    add('improper', 'improper', [expr, a, b], answer)
# Boundary expectations come from mathematical meaning, not current bugs.
add('limit', 'limit_near', ['1/x', 0], 'no_two_sided_limit', check='reject_nonexistent', kind='boundary')
add('limit', 'limit', ['1/x', 0], 'no_two_sided_limit', check='reject_nonexistent', kind='boundary')
add('area', 'area', ['x', '0', -1, 1], '1', kind='boundary')
add('area', 'area', ['x^2', 'x', 0, 1], '1/6', kind='boundary')
add('improper', 'improper', ['1/x', 1, None], 'diverges', check='divergence', kind='boundary')
add('improper', 'improper', ['1/x^2', 0, 1], 'diverges', check='divergence', kind='boundary')
for operation, args in [('integrate', ['']), ('differentiate', ['  ']),
                         ('limit', ['sin(', 0]), ('substitution', ['x+']),
                         ('tangent', ['', 0]), ('area', ['', 'x', 0, 1]),
                         ('volume', ['', 0, 1, 'disk']), ('improper', ['', 1, None]),
                         ('riemann', ['x', 0, 1, 0, 'left']),
                         ('riemann', ['x', 1, 0, 4, 'left']),
                         ('riemann', ['x', 0, 1, 4, 'invalid'])]:
    add('validation', operation, args, 'error', check='error', kind='invalid')
# Product validation decisions, not established application contracts.
add('validation', 'riemann', ['x', 0, 1, 2.5, 'left'], 'error', check='error', kind='invalid', contract='proposed-validation')
add('validation', 'volume', ['x', 0, 1, 'washer'], 'error', check='error', kind='invalid', contract='proposed-validation')

# Validate the hand-entered antiderivative fixtures independently of app outputs.
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application, convert_xor
transformations = standard_transformations + (implicit_multiplication_application, convert_xor)
for case in cases:
    if case['check'] == 'antiderivative':
        integrand = parse_expr(case['args'][0], local_dict=LOCAL, transformations=transformations)
        ref = sp.sympify(case['expected'], locals=LOCAL)
        assert sp.simplify(sp.diff(ref, x) - integrand) == 0, case['id']
assert len({c['id'] for c in cases}) == len(cases)
OUT.mkdir(parents=True, exist_ok=True)
(OUT/'math-test-dataset.json').write_text(json.dumps({'schema_version': 1, 'cases': cases}, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
with (OUT/'math-test-dataset.csv').open('w', encoding='utf-8-sig', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=list(cases[0]))
    writer.writeheader()
    for case in cases:
        writer.writerow({**case, 'args': json.dumps(case['args'], ensure_ascii=False)})
print(json.dumps({'cases': len(cases), 'antiderivatives_verified': sum(c['check']=='antiderivative' for c in cases)}, ensure_ascii=False))
