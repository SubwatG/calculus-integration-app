"""Run trusted repo fixtures against production helpers without modifying them."""
import argparse
from collections import Counter
import json
import math
from pathlib import Path
import sys
import time

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
import sympy as sp
from utils.sympy_solver import integrate, differentiate, compute_limit
from utils.substitution_solver import solve_substitution
from utils.limit_solver import compute_limit_near
from utils.tangent_solver import compute_tangent
from utils.riemann_solver import compute_riemann
from utils.area_solver import compute_area_between
from utils.volume_solver import compute_volume
from utils.improper_solver import compute_improper

FUNCTIONS = dict(integrate=integrate, differentiate=differentiate, limit=compute_limit,
                 substitution=solve_substitution, limit_near=compute_limit_near,
                 tangent=compute_tangent, riemann=compute_riemann,
                 area=compute_area_between, volume=compute_volume, improper=compute_improper)
x = sp.Symbol('x')
LOCAL = {'x': x, 'pi': sp.pi, 'e': sp.E, 'ln': sp.log}


def check_case(case, response):
    check = case['check']
    text = ' '.join(str(response.get(k, '')) for k in ['latex', 'steps', 'error']).lower()
    if check == 'error':
        return response.get('ok') is False and bool(response.get('error'))
    if check == 'reject_nonexistent':
        # A numeric one-sided limit or ok=True/result=None is not a two-sided diagnosis.
        return any(word in text for word in ['ไม่มีลิมิต', 'ลิมิตไม่มี', 'does not exist', 'no two-sided'])
    if check == 'divergence':
        return any(word in text for word in ['ลู่ออก', 'diverg'])
    if not response.get('ok') or response.get('result') is None:
        return False
    actual = response['result']
    reference = sp.sympify(case['expected'], locals=LOCAL)
    if check == 'antiderivative':
        return sp.simplify(sp.diff(actual-reference, x)) == 0
    if isinstance(actual, sp.Expr):
        matched = sp.simplify(actual-reference) == 0
    else:
        matched = math.isclose(float(actual), float(reference),
                               rel_tol=case['tolerance'], abs_tol=case['tolerance'])
    # Check finite-bound display too, not only the correct internal numeric result.
    if case['operation'] == 'improper' and case['args'][2] is not None:
        matched = matched and r'\infty' not in response.get('latex', '')
    return bool(matched)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, default=Path(__file__).with_name('dataset-results.json'))
    args = parser.parse_args()
    dataset = json.loads(Path(__file__).with_name('math-test-dataset.json').read_text(encoding='utf-8'))
    cases = dataset['cases']
    assert len({c['id'] for c in cases}) == len(cases)
    records = []
    for case in cases:
        started = time.perf_counter()
        try:
            response = FUNCTIONS[case['operation']](*case['args'])
            passed = check_case(case, response)
            actual = {k: str(response.get(k)) for k in ['ok', 'result', 'latex', 'error']}
        except Exception as exc:
            passed, actual = False, {'exception': repr(exc)}
        records.append(dict(id=case['id'], topic=case['topic'], contract=case['contract'],
                            status='PASS' if passed else 'FAIL', expected=case['expected'],
                            actual=actual, seconds=round(time.perf_counter()-started, 6)))
    counts = Counter(r['status'] for r in records)
    report = dict(total=len(records), passed=counts['PASS'], failed=counts['FAIL'],
                  mathematical_failures=sum(r['status']=='FAIL' and r['contract']=='mathematical' for r in records),
                  proposed_validation_failures=sum(r['status']=='FAIL' and r['contract']=='proposed-validation' for r in records),
                  results=records)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    print(json.dumps({k:v for k,v in report.items() if k!='results'}, ensure_ascii=False))
    for record in records:
        if record['status']=='FAIL':
            print(record['id'], record['topic'], record['expected'], record['actual'])
    print('Report:', args.output)
    return 1 if counts['FAIL'] else 0


if __name__ == '__main__':
    raise SystemExit(main())
