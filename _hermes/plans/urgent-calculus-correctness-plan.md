---
topic: urgent-calculus-correctness-plan
date: 2026-10-05
model: gpt-6.1-sol-900k
provider: openai-codex
status: ready-for-user-review-planning-only
---

# Urgent Calculus Correctness Implementation Plan

> **For agentic workers:** โหลด `subagent-driven-development` และ `tdd` ด้วย `skill_view(name=...)` แล้วทำทีละงานพร้อมตรวจ Standards และ Spec ก่อนรับงาน ห้ามใช้ร่าง subagent แทนแผนฉบับนี้

**Goal:** แก้ข้อสรุปลิมิต พื้นที่ ขอบเขตปริพันธ์ และกราฟค่าคงที่ โดยไม่รายงานคำตอบที่ระบบยังพิสูจน์ไม่ได้

**Architecture:** ใช้ public helper เดิมเป็น test seams ปรับ dict ด้วยคีย์สถานะเพิ่มเฉพาะที่จำเป็น และให้ UI อ่านสถานะก่อนแสดงคำตอบ แก้ scalar broadcasting ภายใน plotter เดิม ไม่รื้อ parser หรือเพิ่มระบบใหม่

**Tech Stack:** Python, SymPy, NumPy, Matplotlib, Streamlit, pytest ที่อยู่ใน `.venv` ของโครงการ

**Spec:** [urgent-calculus-correctness-spec.md](urgent-calculus-correctness-spec.md)

## Global Constraints

- รอบนี้เป็นการวางแผนเท่านั้น ไม่มีการแก้ production code หรือ tests
- ไม่เพิ่ม dependencies ไม่เปลี่ยนธีม ไม่แตะ survey และไม่ commit/push หากยังไม่ได้รับอนุญาต
- อ่าน `AGENTS.md`, `CONTEXT.md` และ working-tree diff ก่อนลงมือ รักษางานที่ค้างอยู่ใน `.gitignore`, `app.py`, เอกสาร survey และไฟล์ untracked
- คง signatures และชื่อคีย์เดิม แก้ค่าที่ผิดได้ การรักษารูปร่าง API ไม่ใช่การรักษาคำตอบผิด
- Code/comments/filenames เป็น English; ข้อความ UI เป็นไทย ไม่มี emoji; LaTeX ใช้ `$...$` และ `$$...$$`
- ข้อความไทยอยู่ใน Markdown หรือ widget label ไม่ใส่ใน `\text{}` ของสมการ
- `ok=True` ใช้กับสถานะ `finite`, `infinite`, `dne`, `divergent` ตามประเภท helper; `unsupported`/`error` คืน `ok=False`, `result=None`, ข้อความไทยใน `error`
- ชุดข้อมูลมีข้อเสนอ validation สองกรณีที่อยู่นอกงานเร่งด่วน ต้องรายงานแยก ไม่บังคับทั้งชุดเป็นสีเขียวด้วยการแก้เฉลย
- เวลา symbolic evaluation ไม่ถูกจำกัดเพียงเพราะช่วงอินทิเกรตจำกัด ห้ามเรียก `solve` หรือ `solveset` ว่ามี timeout หากไม่มีตัวควบคุมเวลาจริง

## จุดที่แก้จากร่างของ subagent

1. `sp.limit` ที่ไม่ระบุทิศทางใช้ทิศทางเริ่มต้น ไม่ใช่ตัวตรวจว่าลิมิตสองด้านมีอยู่ ต้องคำนวณซ้ายและขวาจริง
2. เมื่อ `status='dne'` ให้ `result=None` และไม่แสดงสมการเท่ากับอนันต์ แม้ test เก่าเคยยอมรับผลนั้น
3. การสุ่มกริดและตรวจ sign change ไม่ยืนยันว่าพบจุดตัดครบ ห้ามใช้ midpoint ของช่องกริดเป็น exact root หรือใช้ `sp.N` เปลี่ยน Integral ค้างเป็นคำตอบ exact
4. `nan`, `zoo` หรือ complex result ไม่ใช่หลักฐานว่าปริพันธ์จริงลู่ออกเสมอ ต้องตรวจ domain ก่อนและแยก `unsupported`
5. Scalar broadcast ไม่ได้ mask nonfinite โดยอัตโนมัติ ต้องเขียนการจัดการ NaN/inf อย่างชัดเจนและไม่แปลงเป็นศูนย์

## ลำดับและ blocking edges

| งาน | ลำดับ | สิ่งที่ต้องเสร็จก่อน |
|---|---|---|
| T1 ลิมิตสองด้าน | 1 | baseline |
| T2 พื้นที่เรขาคณิต | 2 | baseline; แยกแก้จาก T1 ได้แต่ยังส่งตรวจทีละงาน |
| T3 ขอบเขตและสถานะปริพันธ์ | 3 | baseline |
| T4 กราฟค่าคงที่ | 4 | baseline; ส่ง patch แยกจาก T2 เพราะแตะ plotter |
| T5 ตรวจระบบก่อนปิดงาน | สุดท้าย | T1–T4 |

## เตรียม baseline

- [ ] รันจาก `/home/kitti/Documents/GitHub/calculus-integration-app` และบันทึกผลใหม่ ไม่ใช้ผลเก่าเป็นหลักฐานหลังแก้

```bash
.venv/bin/python -m pytest tests/ -q
.venv/bin/python docs/testing/run-test-dataset.py --output /home/kitti/.hermes/profiles/teaching-orchestrated/cache/scratch/calculus-before.json
```

baseline ที่เคยรัน: pytest 49 ผ่าน; dataset 76 ผ่านจาก 86 กรณี คำสั่ง dataset คืน exit code 1 เป็นผลคาดหมายก่อนแก้ ไม่ใช่เหตุให้แก้ expected ตามผลผิด

## T1: ลิมิตสองด้านและผลในเครื่องคิดเลข

**Files:** Modify `utils/limit_solver.py`, `utils/sympy_solver.py`, `pages/limit_approach.py`, `pages/solver.py`; Test `tests/test_limit_solver.py`, `tests/test_sympy_solver.py`

**Interfaces:** คง `compute_limit_near(expr_str: str, a: float) -> dict` และ `compute_limit(expr_str: str, point: float | int = 0) -> dict[str, Any]`; เพิ่ม `status` พร้อม `left_limit`/`right_limit` เป็น SymPy objects เมื่อคำนวณได้ สถานะ `finite/infinite/dne/unsupported/error`

- [ ] เพิ่ม failing tests ต่อไปนี้ พร้อม imports ในแต่ละไฟล์ที่นำไปใช้

```python
import pytest
import sympy as sp
from utils.limit_solver import compute_limit_near
from utils.sympy_solver import compute_limit

@pytest.mark.parametrize('solver', [compute_limit_near, compute_limit])
def test_two_sided_limit_dne(solver):
    res = solver('1/x', 0)
    assert res['status'] == 'dne'
    assert res['result'] is None
    assert res['left_limit'] == -sp.oo
    assert res['right_limit'] == sp.oo
    assert 'ไม่มีลิมิต' in ' '.join(res['steps'])

@pytest.mark.parametrize('solver', [compute_limit_near, compute_limit])
def test_equal_infinite_sides(solver):
    res = solver('1/x**2', 0)
    assert res['status'] == 'infinite'
    assert res['left_limit'] == res['right_limit'] == sp.oo

def test_finite_limit_near_kept():
    assert compute_limit_near('sin(x)/x', 0)['result'] == pytest.approx(1)
    assert compute_limit('sin(x)/x', 0)['result'] == sp.Integer(1)
```

- [ ] รัน `.venv/bin/python -m pytest tests/test_limit_solver.py tests/test_sympy_solver.py -v` ยืนยัน regression tests แดงเพราะพฤติกรรมปัจจุบัน ไม่ใช่ import ผิด
- [ ] ใช้การจำแนกด้านเดียวต่อไปนี้เป็น core logic ภายในโมดูลเดิม และใช้ซ้ำด้วย import ทิศทางเดียวที่ไม่เกิดวงจร

```python
from sympy.calculus.accumulationbounds import AccumulationBounds

def _limit_status(left, right):
    if isinstance(left, AccumulationBounds) or isinstance(right, AccumulationBounds):
        return 'dne'
    if left.is_extended_real is not True or right.is_extended_real is not True:
        return 'unsupported'
    if left == right:
        return 'infinite' if left in (sp.oo, -sp.oo) else 'finite'
    if left.is_number is True and right.is_number is True:
        return 'dne'
    return 'unsupported'
```

- [ ] สรุปค่าจากด้านซ้าย/ขวาที่ตรวจแล้ว ไม่ใช้ค่า default directional limit เป็นคำตอบสองด้าน `finite` คืนชนิดเดิม; `infinite` คืน SymPy infinity ในเครื่องคิดเลขและ `None` ใน helper บทเรียน; `dne` คืน `None` ทั้งคู่
- [ ] สถานะ `unsupported` ห้ามผ่านเข้า branch ที่เขียนสมการซ้ายเท่าขวา ไม่มี numeric sample fallback และไม่สรุป nonreal limit เป็น real answer
- [ ] แก้ test เก่าที่ตรวจ 1/x ที่ 0 แล้วอนุญาต oo/zoo ให้ตรวจ `dne`; นี่คือการแก้เกณฑ์ผิด ไม่ใช่การปิด test
- [ ] หน้า UI แสดง metric/คำอธิบายตาม status และแสดงซ้ายกับขวาโดยไม่อ้างว่าต่างกันเท่ากัน
- [ ] เพิ่มกรณี `-1/x**2`, `sin(1/x)`, empty input และกรณี domain จริงที่ไม่ครบสองข้างเป็น `unsupported` โดยไม่เดา
- [ ] รัน targeted tests จนผ่าน ตรวจ diff ตาม Spec ก่อนรับ T1

## T2: พื้นที่เรขาคณิตบนช่วงจริงจำกัด

**Files:** Modify `utils/area_solver.py`, `pages/area_between.py`; Test `tests/test_area_solver.py`

**Interfaces:** คง `compute_area_between(f_str: str, g_str: str, a: float, b: float) -> dict` และคีย์ `ok/result/latex/steps/expr/f_expr/g_expr/error`; ไม่จำเป็นต้องเพิ่ม intersections หรือ warnings API ในรุ่นเร่งด่วน

- [ ] เพิ่ม regression tests

```python
import pytest
from utils.area_solver import compute_area_between

@pytest.mark.parametrize('f,g,a,b,expected', [
    ('x', '0', -1, 1, 1),
    ('x**2', 'x', 0, 1, 1/6),
    ('x', 'x**2', 0, 1, 1/6),
    ('3', '1', 0, 2, 4),
    ('x', 'x', -1, 1, 0),
])
def test_geometric_area(f, g, a, b, expected):
    res = compute_area_between(f, g, a, b)
    assert res['ok'] is True
    assert res['result'] == pytest.approx(expected)

@pytest.mark.parametrize('f,g,a,b', [
    ('1/x', '0', -1, 1),
    ('sqrt(x)', '0', -1, 1),
    ('x', '0', 1, 0),
    ('x', '0', 0, float('inf')),
])
def test_area_rejects_invalid_domain(f, g, a, b):
    res = compute_area_between(f, g, a, b)
    assert res['ok'] is False
    assert res['result'] is None
    assert res['error']
```

- [ ] รัน `.venv/bin/python -m pytest tests/test_area_solver.py -v` ให้เห็นค่าพื้นที่ที่ผิดก่อนแก้
- [ ] ตรวจ bounds เป็น finite real และ `a<b`; ตรวจทั้ง f และ g ไม่มีสัญลักษณ์อื่นและ continuous domain ครอบช่วงจริงทั้งหมด ถ้ายืนยันไม่ได้ให้ reject ไม่ใช่อาศัยเพียง diff ที่ตัด singularity ทิ้ง
- [ ] หา exact area ด้วย integration ของ Abs(diff) ถ้าประเมินไม่ได้ ให้ใช้ exact polynomial path สำหรับผลต่างพหุนามที่มีสัมประสิทธิ์ตรรกยะเท่านั้น ตัวอย่าง core logic:

```python
def _polynomial_area(diff, x, lower, upper):
    poly = sp.Poly(diff, x)
    if any(c.is_Rational is not True for c in poly.all_coeffs()):
        raise ValueError('Unsupported exact polynomial domain')
    poly = poly.set_domain(sp.QQ)
    if poly.is_zero:
        return sp.S.Zero
    roots = sorted(set(poly.real_roots()))
    cuts = [lower] + [r for r in roots if lower < r < upper] + [upper]
    primitive = sp.integrate(diff, x)
    total = sp.S.Zero
    for left, right in zip(cuts, cuts[1:]):
        sign = sp.sign(diff.subs(x, (left + right)/2))
        if sign not in (sp.S.One, sp.S.NegativeOne):
            raise ValueError('Cannot certify sign on subinterval')
        total += sign * (primitive.subs(x, right)-primitive.subs(x, left))
    return sp.simplify(total)
```

- [ ] bounds ใช้ค่าจริงที่ป้อน ไม่ใช้ `nsimplify` เดาค่าคงที่พิเศษ; หากแปลง decimal finite เป็น Rational ให้ใช้ `sp.Rational(str(value))` และระบุ semantics นี้ใน test
- [ ] ผลต้องไม่มี Integral ค้าง เป็น real finite nonnegative ก่อนแปลงเป็น float; ถ้า direct path และ exact polynomial path ไม่สำเร็จ ให้ error ไทย ไม่ใช้ sign scan หรือ quadrature เป็น exact certification
- [ ] รักษา symbol ที่ parser/plotter ใช้ อย่าเปลี่ยน assumptions ของ symbol ใน expr ที่ส่งออกโดยไม่แทนกลับให้ตรงกับ caller
- [ ] LaTeX ใช้ $A=\int_a^b|f-g|\,dx$ และ steps อธิบายพื้นที่จริง ไม่เรียกผลแบบ signed ว่าพื้นที่; หน้าเปลี่ยน label จากบน/ล่างเป็นฟังก์ชันที่ 1/2 เพื่อไม่ตั้งสมมติฐานผิดเมื่อกราฟตัดกัน
- [ ] เพิ่ม test reject unresolved Integral โดย monkeypatch `sp.integrate` ให้คืน Integral ตรวจ public helper ว่าไม่รายงานคำตอบ
- [ ] รัน targeted tests จนผ่าน พร้อมยืนยันไม่มี numerical root fallback ก่อนรับ T2

## T3: ขอบเขตและสถานะปริพันธ์ไม่ตรงแบบ

**Files:** Modify `utils/improper_solver.py`, `pages/improper_integrals.py`; Test `tests/test_improper_solver.py`

**Interfaces:** คง `compute_improper(expr_str: str, a: float, b: float | None = None) -> dict`; เพิ่ม `status` เป็น `finite/divergent/unsupported/error`; `result` เป็น float เฉพาะ `finite`

- [ ] เพิ่ม regression tests

```python
import pytest
from utils.improper_solver import compute_improper

def test_finite_bound_latex_matches_input():
    res = compute_improper('1/x**2', 1, 2)
    assert res['status'] == 'finite'
    assert res['result'] == pytest.approx(0.5)
    assert r'\int_{1}^{2}' in res['latex']
    assert r'\infty' not in res['latex']

@pytest.mark.parametrize('expr,a,b,expected', [
    ('1/x**2', 1, None, 1),
    ('1/sqrt(x)', 0, 1, 2),
])
def test_convergent_improper(expr, a, b, expected):
    res = compute_improper(expr, a, b)
    assert res['status'] == 'finite'
    assert res['result'] == pytest.approx(expected)

@pytest.mark.parametrize('expr,a,b', [('1/x',1,None), ('1/x**2',0,1)])
def test_divergent_improper(expr, a, b):
    res = compute_improper(expr, a, b)
    assert res['status'] == 'divergent'
    assert res['result'] is None

def test_interior_singularity_is_not_a_finite_principal_value():
    res = compute_improper('1/x', -1, 1)
    assert res['status'] in ('divergent', 'unsupported')
    assert res['result'] is None
```

- [ ] รัน `.venv/bin/python -m pytest tests/test_improper_solver.py -v` ยืนยันแดง
- [ ] ตรวจ bounds และ real domain ภายใน open interval ก่อน classify ผล CAS ไม่ยืนยัน nan/zoo/complex ว่า divergent อัตโนมัติ
- [ ] หากมี singularity ภายในที่ยังไม่แยก one-sided integrals ให้ unsupported แทนค่าจำกัด; endpoints singular ที่พิสูจน์การลู่เข้า/ออกได้ยังรองรับ เช่นสองกรณีข้างต้น
- [ ] หลังยืนยัน real domain: finite real result เป็น finite, signed infinity หรือ oscillatory accumulation ที่เป็นหลักฐานไม่มี finite limit เป็น divergent, Integral/conditional/nonreal/unknown เป็น unsupported
- [ ] ใช้ `upper = sp.oo if b is None else b` ทั้งการคำนวณและสร้าง LaTeX; formatting number ใช้ค่าเดียวกัน ไม่ทำ bound ต่างจากที่คำนวณ
- [ ] สร้าง steps ตามชนิด singularity ที่พิสูจน์ได้ กรณี singular endpoint ล่างต้องกล่าวถึงลิมิตที่ขอบล่าง ไม่ใช้เพียงการเข้าใกล้ขอบบน
- [ ] หน้า UI แสดงคำเตือนลู่ออกชัดเจน ไม่สร้างสมการปริพันธ์จริงเท่ากับข้อความที่ดูเหมือนค่าจำกัด; unsupported แสดงข้อจำกัด ไม่กล่าวว่าปริพันธ์ไม่มีรูปปิดโดยไม่มีหลักฐาน
- [ ] เพิ่ม empty input, invalid order, unknown real domain และ unresolved Integral tests; รัน targeted tests จนผ่าน ตรวจ diff ก่อนรับ T3

## T4: กราฟค่าคงที่และ nonfinite samples

**Files:** Modify `utils/plotter.py`; Create `tests/test_plotter.py`

**Interfaces:** คง signatures และ `(fig, ax)` ของ plot helpers เดิม เพิ่ม private helper ในไฟล์เดิมเท่านั้น

- [ ] เพิ่ม regression tests ที่ตรวจข้อมูลกราฟจริงและปิด figure

```python
import matplotlib.pyplot as plt
import numpy as np
import pytest
import sympy as sp
from utils.plotter import plot_area_between

@pytest.mark.parametrize('f,g', [('x','0'), ('5','0'), ('3','1')])
def test_constant_curves_have_matching_shapes(f, g):
    fig, ax = plot_area_between(sp.sympify(f), sp.sympify(g), -1, 1)
    try:
        for line in ax.lines[:2]:
            assert len(line.get_xdata()) == len(line.get_ydata())
            assert len(line.get_xdata()) > 1
        assert ax.collections
    finally:
        plt.close(fig)
```

- [ ] รัน `.venv/bin/python -m pytest tests/test_plotter.py -v` ยืนยัน shape mismatch ก่อนแก้
- [ ] ใช้ core helper ดังนี้ ไม่แปลง nonfinite เป็นศูนย์และไม่ยอมรับ shape ที่ไม่เข้ากับ grid

```python
def _as_curve(values, xs):
    arr = np.asarray(values)
    if np.iscomplexobj(arr):
        arr = np.where(np.imag(arr) == 0, np.real(arr), np.nan)
    arr = np.asarray(arr, dtype=float)
    if arr.ndim == 0:
        arr = np.full(xs.shape, float(arr))
    if arr.shape != xs.shape:
        raise ValueError('Curve samples do not match x grid')
    return np.where(np.isfinite(arr), arr, np.nan)
```

- [ ] เรียก helper หลัง lambdify ที่ส่งไป plot/fill ใน area, Riemann, volume, improper; ตรวจ tangent/limit ที่มี guard เดิมและเปลี่ยนเฉพาะจุดที่จำเป็น ไม่แก้ theme
- [ ] รักษา finite masks ก่อน fill/percentile/axis limits; all-NaN ต้องมีข้อจำกัดชัดเจน ไม่ได้ถือว่ากราฟว่างเป็นความสำเร็จ
- [ ] เปลี่ยน labels กราฟ area ที่เรียกเส้นว่า top/bottom และส่วนหนึ่งว่า Inverted Area ให้ตรงกับพื้นที่ระหว่างฟังก์ชันทั้งสองใน T2 โดยไม่เปลี่ยนสี/ธีม
- [ ] เพิ่ม public plot tests ของฟังก์ชันคงที่บน Riemann/improper และ nonfinite samples; ทุก test ปิด figure ตรวจ baseline plots ไม่เสีย
- [ ] รัน targeted และ full tests ตรวจ diff ก่อนรับ T4

## T5: Gate ก่อนประกาศว่าแก้แล้ว

- [ ] รัน `.venv/bin/python -m pytest tests/ -v`; บันทึกจำนวนจริงใหม่ ไม่อ้างว่าจะยังเป็น 49 รายการหลังเพิ่ม tests
- [ ] รัน dataset ไป report ใหม่ ไม่เขียนทับหลักฐานก่อนแก้; `mathematical_failures` ต้องเป็น 0 ส่วน proposed-validation สองรายการแยกรายงาน
- [ ] ทดสอบผ่าน browser-box ตามตารางนี้ โดยยืนยันค่าที่ commit แล้วและ KaTeX annotation ไม่ใช่ตรวจ DOM input อย่างเดียว

| หน้า | Input | Acceptance |
|---|---|---|
| ลิมิต + เครื่องคิดเลข | `1/x`, point 0 | ไม่มีลิมิตสองด้าน ไม่มีสมการสรุปซ้ายเท่าขวา |
| ลิมิต | `1/x**2`, point 0 | อนันต์เครื่องหมายเดียวกัน ไม่สับสนกับ DNE |
| พื้นที่ | `x`, `0`, -1, 1 | พื้นที่ 1 พร้อมกราฟโหลด |
| พื้นที่ | `x**2`, `x`, 0, 1 | พื้นที่บวก 1/6 |
| พื้นที่ | `5`, `0`, 0, 2 | เส้นแนวนอนและพื้นที่แรเงา |
| ปริพันธ์ไม่ตรงแบบ | `1/x**2`, 1, 2 | สมการขอบบน 2 ค่า 1/2 |
| ปริพันธ์ไม่ตรงแบบ | `1/x`, 1, infinity | มีคำวินิจฉัยลู่ออก |
| ปริพันธ์ไม่ตรงแบบ | `1/sqrt(x)`, 0, 1 | ค่า 2 พร้อม steps กล่าวถึง singular endpoint |
| ปริพันธ์ไม่ตรงแบบ | `1/x`, -1, 1 | ไม่แสดงค่าจำกัดจาก principal value |
| Quiz | ผิดครั้งแรก แล้วแก้ถูก ไป history แล้วกลับ | คำใบ้และคะแนนไม่ regress |

- [ ] เก็บ JSON/รายงาน before-after ใหม่พร้อม commit และ working-tree fingerprint; ไม่ส่ง survey ภายนอก
- [ ] ตรวจ Markdown ด้วย s1-doctor และรายงานข้อจำกัดจริง รวมการยังไม่มี hard timeout symbolic evaluation
- [ ] Parent ตรวจ Standards + Spec และ test/browser evidence ก่อนประกาศเสร็จ ไม่รับเพียงคำรายงานของ worker
- [ ] Commit/push เป็นขั้นตอนแยก ต้องได้รับอนุญาต ไม่ใช้ `git add -A` ใน dirty tree นี้

## การส่งมอบเพื่อเริ่มลงมือ

แนะนำทำทีละ task ด้วย worker หนึ่งตัวแล้ว parent ตรวจ ก่อนเริ่ม task ถัดไป ไม่แก้ plotter พร้อมกันสอง worker ไม่ต้องเปิด server ใหม่หาก `http://127.0.0.1:8502/_stcore/health` ยังตอบ ok

test seams ที่เสนอคือ public helper เดิมและหน้าจอ browser-box หากผู้ใช้อนุมัติให้เริ่มลงมือ ให้เริ่ม T1 ก่อน แผนนี้ยังไม่ถือเป็นการอนุมัติ commit/push
