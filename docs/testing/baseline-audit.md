# Baseline Test & Coverage Audit

Read-only independent audit of `calculus-integration-app` tests, solver APIs, and
coverage gaps. No application or test files were modified. The working tree was
left untouched, including pre-existing dirty state (see "Working-tree state" below).

Author: independent audit subagent
Audit date: 2026-10-05 (+07)
Repository: `/home/kitti/Documents/GitHub/calculus-integration-app`
Branch: `main`

---

## 1. Environment and baseline command

Project virtualenv was present and usable; no installs or network access were
performed.

```
$ source .venv/bin/activate
$ python -c "import sys,sympy,pytest,streamlit;print(sys.version);print('sympy',sympy.__version__);print('pytest',pytest.__version__)"
3.12.14 (main, Aug 25 2026, 14:00:49) [Clang 22.1.3 ]
sympy 1.14.0
pytest 9.1.1
```

```
$ pytest tests/ -v
platform linux -- Python 3.12.14, pytest-9.1.1, pluggy-1.6.0 -- /home/kitti/Documents/GitHub/calculus-integration-app/.venv/bin/python
cachedir: .pytest_cache
rootdir: /home/kitti/Documents/GitHub/calculus-integration-app
plugins: anyio-4.15.1
collecting ... collected 49 items
...
============================== 49 passed in 0.98s ==============================
```

```
$ pytest tests/ --collect-only -q
...
49 tests collected in 0.38s
```

**Baseline result: 49 passed, 0 failed, 0 skipped, 0 xfail. Wall time 0.98 s.**
All 49 tests exercise pure `utils/` logic only (no Streamlit runtime required for
collection; `quiz_engine`/`content_loader` import `streamlit` but are never
imported by the test suite).

Runtime warnings observed during probes only (not part of the suite):
`streamlit.runtime.caching.cache_data_api: No runtime found, using MemoryCacheStorageManager`.

---

## 2. Working-tree state (preserved, not modified)

`git status --porcelain` before audit (unchanged after):

```
 M .gitignore
 M app.py
 M docs/calculus-app-satisfaction-survey.qmd
?? docs/architecture/calculus-24h-priority-plan.md
?? docs/calculus-app-satisfaction-survey.pdf
?? docs/calculus-survey-qr.png
?? docs/survey-system-architecture-and-workflow.html
?? docs/survey-system-architecture-and-workflow.pdf
?? docs/survey-system-architecture-and-workflow.qmd
?? pages/survey.py
```

The only file this audit added is `docs/testing/baseline-audit.md` (new directory).

---

## 3. Test inventory (49 collected)

| Test file | `def test_` | Collected | Target under test |
|---|---|---|---|
| `tests/test_sympy_solver.py` | 10 | 10 | `utils.sympy_solver` |
| `tests/test_riemann_solver.py` | 10 | 10 | `utils.riemann_solver` |
| `tests/test_limit_solver.py` | 5 | 5 | `utils.limit_solver`, `plotter.plot_limit_near` |
| `tests/test_tangent_solver.py` | 5 | 5 | `utils.tangent_solver`, `plotter.plot_tangent` |
| `tests/test_area_solver.py` | 4 | 4 | `utils.area_solver`, `plotter.plot_area_between` |
| `tests/test_improper_solver.py` | 4 | 4 | `utils.improper_solver`, `plotter.plot_improper` |
| `tests/test_volume_solver.py` | 4 | 4 | `utils.volume_solver`, `plotter.plot_volume` |
| `tests/test_substitution_solver.py` | 3 | 3 | `utils.substitution_solver` |
| `tests/test_quiz_data.py` | 2 | 4 | `data/quizzes/*.json` (one method parametrized over 3 files) |
| **Total** | **47** | **49** | |

Note: `test_quiz_data.py` defines 2 methods; `test_quiz_file_valid_structure` is
parametrized over the 3 files found by glob, yielding 49 collected tests total.

### Modules with ZERO test coverage

- `utils/quiz_engine.py` (grading logic)
- `utils/content_loader.py` (lesson discovery / frontmatter parsing)
- `utils/math_render.py` (pure formatting helpers)
- `utils/theory.py` (`THEORY_CONTENT` data)
- `utils/theme.py`, `utils/plotter.py` (only plot smoke tests via solver tests)
- `pages/*` (UI; intentional, not unit-tested)

### Test quality observation

The solver tests for `area_solver`, `improper_solver`, `volume_solver`, and
`substitution_solver` are marked with `TODO: ตรวจค่า result ตามหัวข้อ` and only
assert `res["result"] is not None` + `len(res["steps"]) >= 3`. They do **not**
assert numeric correctness, method behavior, or divergence handling. These tests
pass even when the underlying behavior is wrong (see section 6).

---

## 4. Public API surface (from `inspect.signature`)

```
utils/sympy_solver.py
    _parse_input(expr_str: str) -> Expr
    integrate(expr_str: str) -> dict[str, Any]
    differentiate(expr_str: str) -> dict[str, Any]
    compute_limit(expr_str: str, point: float | int = 0) -> dict[str, Any]

utils/riemann_solver.py
    _parse_input(expr_str: str) -> Expr
    _fmt_num(x: float) -> str
    _point_latex(expr: Expr, x_val: float) -> str
    compute_riemann(expr_str: str, a: float, b: float, n: int, method: str = "left") -> dict[str, Any]
    METHODS: {"left": (th_name, r"L_n"), "right": (..., r"R_n"), "midpoint": (..., r"M_n")}

utils/area_solver.py
    compute_area_between(f_str: str, g_str: str, a: float, b: float) -> dict

utils/improper_solver.py
    compute_improper(expr_str: str, a: float, b: float | None = None) -> dict

utils/limit_solver.py
    compute_limit_near(expr_str: str, a: float) -> dict

utils/volume_solver.py
    compute_volume(expr_str: str, a: float, b: float, method: str = "disk") -> dict

utils/substitution_solver.py
    solve_substitution(expr_str: str) -> dict

utils/tangent_solver.py
    compute_tangent(expr_str: str, a: float) -> dict

utils/quiz_engine.py
    grade_quiz(questions: list[dict[str, Any]], answers: dict[int, str | None]) -> dict[str, int]
    load_quiz(topic: str) -> list[dict[str, Any]]   # @st.cache_data

utils/content_loader.py
    _frontmatter_title(text: str) -> str | None
    _heading_title(text: str) -> str | None
    _display_name(filename: str, text: str) -> str
    list_lessons() -> list[dict]
    load_lesson(filename: str) -> str   # @st.cache_data

utils/math_render.py
    has_thai(text: str) -> bool
    strip_math_delimiters(expr: str) -> str
    is_pure_latex(expr: str) -> bool
    render_latex(expr: str, *, label: Optional[str] = None) -> None
    render_steps(steps) -> None
    preview_math_expr(expr_str: str, label: str = "สมการที่ระบบเข้าใจ") -> bool
    render_syntax_guide() -> None

utils/plotter.py
    plot_riemann(expr, a, b, n, method="left", exact=None) -> tuple
    plot_tangent(expr, a, span=3.0) -> tuple
    plot_limit_near(expr, a, delta=0.5, span=3.0) -> tuple
    plot_substitution(expr) -> tuple
    plot_volume(expr, a, b, method="disk") -> tuple
    plot_area_between(f_expr, g_expr, a, b) -> tuple
    plot_improper(expr, a, b=None) -> tuple
    _stub_figure(title) -> tuple
```

All 8 solvers share an identical result contract documented in their module
docstrings:

```python
{
    "ok": bool,
    "result": float | sympy.Expr | None,  # sympy.Expr for indefinite integrals
    "latex": str,
    "steps": list[str],   # LaTeX strings
    "expr": sympy.Expr | None,
    "error": str | None,  # Thai error message
}
```

---

## 5. What the existing tests DO cover

- `sympy_solver`: `integrate` power/constant/sum/reciprocal; `differentiate`
  power rule; `compute_limit` finite limit and `1/x → 0`; invalid/empty input
  returns `ok=False`.

- `riemann_solver`: left/right/midpoint numeric values for `x**2` on `[0,2]`,
  midpoint accuracy vs `8/3`, `METHODS` catalog, and error paths (bad expr,
  bad method, `b<=a`, `n=0`).

- `limit_solver`, `tangent_solver`: one numeric case each + invalid input +
  a plot-figure smoke test.

- `area_solver`, `improper_solver`, `volume_solver`, `substitution_solver`:
  a "runs and returns non-None" smoke test, an invalid-input test, a non-empty
  latex test, and for three of them a plot-figure smoke test.

- `data/quizzes/*.json`: file existence and per-question structural schema
  (`topic, question, choices, answer, hint, explanation`; answer ∈ choices).

- Plot smoke tests only assert `fig is not None and ax is not None` (matplotlib).

---

## 6. Prioritized untested / unverified behaviors

Each finding below was reproduced by running the real code in the project venv
(read-only probes; no source edited).

### P0 — Correctness / domain handling hidden by weak tests

1. **`volume_solver.compute_volume` ignores `method` entirely.**
   `method` is accepted but never read; washer is identical to disk and any
   unknown method is accepted.
   ```
   compute_volume("x", 0, 2, "disk")   -> 8.377580409572783
   compute_volume("x", 0, 2, "washer") -> 8.377580409572783   # same
   compute_volume("x", 0, 2, "bogus")  -> ok=True             # not rejected
   ```
   The existing test only calls `method="disk"` and asserts `result is not None`.

2. **`improper_solver.compute_improper` does not distinguish convergence from
   divergence, and its LaTeX bound is wrong for finite `b`.**
   ```
   compute_improper("1/x", 1, None) -> ok=True, result=None, latex="\int_{1}^{\infty} \frac{1}{x} \, dx = \infty"
   compute_improper("x", 0, 2)      -> latex="\int_{0}^{\infty} x \, dx = 2"   # bound shown as \infty though b=2
   ```
   Divergent integral returns `ok=True` with `result=None` (because
   `oo.is_real is False`), so callers see success with no numeric value.
   The `latex` field hardcodes `\infty` regardless of `b`.

3. **`area_solver.compute_area_between` returns the signed net integral, not the
   geometric area, and does not find intersections as its docstring claims.**
   ```
   compute_area_between("x", "x**2", 0, 1) -> 0.16666666666666666
   compute_area_between("x**2", "x", 0, 1) -> -0.16666666666666666  # negative area
   compute_area_between("x", "x", 0, 1)    -> 0.0
   ```
   Docstring: `"""หาจุดตัด f(x)=g(x) แล้วคำนวณ A = ∫(f-g)dx"""` — no intersection
   solving or absolute value / interval splitting is implemented.

4. **`limit_solver.compute_limit_near` reports non-existent two-sided limits as
   success with `result=None`.**
   ```
   compute_limit_near("1/x", 0) -> ok=True, result=None, latex="\lim_{x \to 0} \frac{1}{x} = \infty"
   ```
   Left limit is `-oo` and right limit is `+oo`, yet the step text asserts
   `lim_{x->a^-} f = lim_{x->a^+} f = oo`, which is mathematically false.

5. **`sympy_solver` real-domain edge cases.**
   ```
   integrate("1/x")            -> result = log(x)        # no abs(); valid only x>0
   compute_limit("1/x", 0)     -> result = oo            # sympy 1.14 gives oo, not zoo
   integrate("x**-1")          -> steps use the 1/x branch (correct)
   integrate("") / "   "       -> ok=False
   integrate("x**")            -> ok=False
   ```
   `log(x)` (not `log(abs(x))`) is documented as an assumption only in a test
   comment; the `+" + C"` appended to `latex` is not asserted anywhere.

### P1 — Logically significant, weakly or untested

6. **`riemann_solver` n>8 branch and helpers.**
   - The `n_i > 8` branch computes `index_note` but never uses it (dead local),
     while `terms_latex` becomes `f(x_0)+\cdots+f(x_{n-1})`.
     ```
     compute_riemann("x**2",0,2,9,"left")["steps"][2]
       -> "คำนวณ $f(x_i)$ แต่ละจุด แล้วรวมกัน: $f(x_0)+\\cdots+f(x_{8})$"
     ```
   - `int(n)` silently truncates a float `n` (`4.7` → `ok=True`, n=4).
   - Non-real integrand values (e.g. `sqrt(x)` over `[-1,1]`) return `ok=False`
     with the generic Thai message; behavior is untested.
   - `_fmt_num` and `_point_latex` have no direct tests.
     ```
     _fmt_num(-0.0)            -> "0"
     _fmt_num(1.0000000001)    -> "1"
     _fmt_num(1.5)             -> "1.5"
     ```

7. **`sympy_solver.differentiate` / `compute_limit` steps and `latex` are not
   asserted** — only `ok`/`result`. Branch selection for `x` vs `Pow` vs other
   (`sin(x)`) is unverified for `differentiate`.

8. **`quiz_engine.grade_quiz` has zero tests.** Verified behaviors (unasserted):
   ```
   grade_quiz(3 q, all correct)     -> {"score": 3, "total": 3}
   grade_quiz(3 q, partial)         -> {"score": 1, "total": 3}
   grade_quiz(3 q, {})              -> {"score": 0, "total": 3}
   grade_quiz(3 q, {0: None,...})   -> {"score": 2, "total": 3}
   grade_quiz(3 q, extra keys)      -> {"score": 3, "total": 3}
   grade_quiz([], {})               -> {"score": 0, "total": 0}
   ```
   `load_quiz` (JSON path + `@st.cache_data`) is also untested.

9. **`content_loader` helpers have zero tests** — `_frontmatter_title`,
   `_heading_title` (duplicate-number cleanup `"3.6 3.6 X" -> "3.6 X"`),
   `_display_name` fallbacks, and `list_lessons` ordering/sort_key across the
   four filename layouts (`cal2/chNN/`, `cal2/NN-`, `cal2/solutions/`,
   legacy `silpakorn-*`). `NON_LESSONS` filtering and `_archive` exclusion
   are unverified.

10. **`math_render` pure helpers have zero tests** — `has_thai`,
    `strip_math_delimiters` (only strips when the whole string is wrapped;
    `$` count check for inline), `is_pure_latex` edge cases (`""`, Thai text,
    bare numbers). `render_*` functions touch Streamlit and need a runtime.

11. **`plotter.plot_riemann` and `plot_substitution` are not directly tested**
    (only `plot_tangent`, `plot_limit_near`, `plot_volume`,
    `plot_area_between`, `plot_improper` have smoke tests). `_stub_figure`
    (fallback path) untested.

### P2 — Structural / data

12. `utils/theory.py` `THEORY_CONTENT` dict schema (required keys per topic) is
    not validated by any test.

13. `utils/theme.py` and all `pages/*` are untested (UI-only; acceptable, but
    raises the question of an integration/smoke test via `streamlit.testing`).

14. `riemann_solver` and `sympy_solver` parse-input error messages are asserted
    only as truthy, not for content.

---

## 7. Recommended test-plan focus (for the runner/dataset to be built)

Ordered by risk, mapping directly onto the gaps above:

1. `volume_solver`: `method` dispatch ("disk" vs "washer" vs unknown), numeric
   correctness for each, invalid method rejection. → P0.1

2. `improper_solver`: convergence value, divergence signalling (`1/x` on
   `[1,∞)`), finite-`b` LaTeX bound correctness, `b=None` vs numeric. → P0.2

3. `area_solver`: signed vs geometric area, negative-result case, equal
   functions, intersection semantics. → P0.3

4. `limit_solver`: two-sided existence (`1/x` at 0), one-sided values,
   `result=None` semantics. → P0.4

5. `sympy_solver`: `log(x)` vs `log(abs(x))` assumption, `+C` in latex, `oo`/`zoo`
   limit outcomes, steps branch coverage. → P0.5

6. `quiz_engine.grade_quiz`: correct/partial/empty/None/extra-key/empty-list.
   → P1.8

7. `content_loader`: frontmatter/heading/display-name parsing and lesson
   ordering. → P1.9

8. `math_render`: `has_thai`, `strip_math_delimiters`, `is_pure_latex`. → P1.10
9. `riemann_solver`: n>8 step rendering, float `n`, non-real integrand,
   `_fmt_num`/`_point_latex`. → P1.6

---

## 8. Blockers and notes

- **No blockers to running the baseline.** Project venv is intact and the suite
  is fully green (49/49).

- The existing `TODO`-style smoke tests (area/improper/volume/substitution) will
  need to be strengthened, not just extended, to catch P0 items 1–3.

- `quiz_engine` and `content_loader` import `streamlit`; testing them outside a
  Streamlit runtime emits cache warnings but works (verified). Prefer testing
  pure helpers directly and, if desired, `load_quiz` with a temp quiz dir.

- Working tree was left dirty exactly as found; only `docs/testing/baseline-audit.md`
  was added.

- No test count was taken from memory: all counts come from the `pytest`
  collection/run output above.
