# Read-only UX/structure audit — riemann, area_between, volume_revolution

Reports: 3 pages (`pages/riemann.py`, `pages/area_between.py`, `pages/volume_revolution.py`).
Repo: `/home/kitti/Documents/GitHub/calculus-integration-app` (branch `main`, HEAD `6947a3b`).
Date: 2026-10-15.

## Method and evidence class

- Read-only source review: repo `AGENTS.md`, the 3 pages, their solvers (`utils/riemann_solver.py`, `utils/area_solver.py`, `utils/volume_solver.py`), `utils/plotter.py`, `utils/theory.py`, `utils/math_render.py`, `utils/keypad.py`, `utils/theme.py`, `app.py` nav, and the existing tests.
- NOT performed: no server start, no browser, no Streamlit AppTest, **no pytest run**. Every claim below is `[SOURCE]` (read from file, with path:line) unless explicitly marked `[UNVERIFIED VISUAL PROPOSAL]`.
- This is a **source-only audit**. It is *not* visual QA and must not be reported as such. Anything about what a learner actually sees (spacing, overflow, expander feel, render timing) is unverified.

### Audit baseline hashes (sha256, recorded at audit time — not a stability guarantee)

| file | sha256 | dirty? |
|---|---|---|
| pages/riemann.py | `4c51889f08eee317e658c8af2a3fec0e1f5531ce06989151325021e28ac692b2` | clean |
| pages/area_between.py | `c06ef6bf1b5a316cfe5f66d399788d681d0ec1b505c139aaf9c869cb9360a834` | clean |
| pages/volume_revolution.py | `31af0e675cd4aab5a8baa1019293bd27164e84ea50739dcbf5811eece2de317f` | clean |
| pages/limit_approach.py | `63652360c99d82427a384cbd7b2ec2269cfdc8382a3d1d51dea8c8787919a99c` | **MODIFIED (live session)** |
| utils/theme.py | `e2ceaf3ddc56e12a8e56001e1a12dc0146ed2d93cacf954c50f33d1ea9b8431d` | **MODIFIED (live session)** |
| utils/keypad.py | `1c07c7226971fdadada3ad44fcb655c9f99ab79f285e8f517f81bb9d7b0f32ed` | **MODIFIED (live session)** |
| utils/theory.py | `ffa3352a6a560125eae2965cbd7ad1728a010bdacfbb19c1193a1c14367b2b9d` | **MODIFIED (live session)** |
| utils/plotter.py | `94e29dcfcdb30c3577cf421e0fbe165cc8b1b95edf195387829db34a3cb4c1a0` | clean |
| utils/math_render.py | `76b84fdff2f082599128ffd731a9d13ecb0a8dc66369429188b74aba6cd2331d` | clean |
| utils/riemann_solver.py | `c87b2949a946da277aee4b699f837631a5920e29ecaf6bcb05a47f11b36b1320` | clean |
| utils/area_solver.py | `9368ac036258d0959edf3e13cfe72396004505095f6ecb38a05b56c81dd1c5e3` | clean |
| utils/volume_solver.py | `82dc7ffd0c2edd70b7b42d2590c4af515e6e9d79ccfcfa4e8f36212754d63191` | clean |

`git status --porcelain` at audit time also shows untracked `docs/plans/2026-10-15-lesson-progressive-disclosure.md`, `tests/test_limit_page_ux.py`, `docs/report/`.

Nav registration (`app.py`): 3 = riemann (L32), 5 = area_between (L34), 6 = volume_revolution (L35).

---

## 1. Cross-page findings (highest priority first)

### C1. `[SOURCE]` "Geometric quantity is always positive" is enforced by `abs()` in the solver — so the pages' own sign guidance can never be observed, and three pages contradict `utils/theory.py` in the same way

| page | on-page claim | actual solver behaviour | theory twin |
|---|---|---|---|
| area_between | `A = ∫_a^b [f-g] dx` with `f ≥ g` required (`pages/area_between.py:55`); "หากใส่สลับกัน ค่าพื้นที่ที่คำนวณได้จะติดลบ" (`pages/area_between.py:59`) | returns `∫|f-g|` (`utils/area_solver.py:156`, `:258`) and sums per-piece `abs` (`:243`); swapping f/g yields the **same positive number**, never a negative | `utils/theory.py:218` repeats the "will be negative" warning; `:234` says area is always positive |
| volume_revolution | "ระวังการกำหนดรัศมีนอกและรัศมีในสลับกัน จะทำให้ปริมาตรติดลบ" is in theory (`utils/theory.py:189`) | washer takes `abs(val_direct)` (`utils/volume_solver.py:136`) → swapped radii give the **same positive volume**; a negative `R(x)` is silently squared (`:102`), giving the volume of `|R|` | theory `:183` says volume is always positive |
| riemann | headline is "พื้นที่ใต้เส้นโค้ง" (`pages/riemann.py:21`) / "การประมาณพื้นที่…" (`:46`) | `compute_riemann` returns the **signed** sum `Σ f(x_i*)Δx` (`utils/riemann_solver.py:126`, `:163`); for `f < 0` the result is negative, while `plot_riemann` labels the shaded integral "Exact area" (`utils/plotter.py:126`) | `utils/theory.py:40` says a below-axis integral is negative and area needs absolute value — the page implements neither |

Consequences that matter for the batch:
- These are **correctness/semantics defects, not cosmetic**. Fixing them honestly requires touching `utils/area_solver.py`, `utils/volume_solver.py`, `utils/plotter.py` labels (`"Exact area"` L126, `"Area (f >= g)"`/`"Area (g > f)"` L560/L570) and `utils/theory.py` — i.e. shared files, and `utils/theory.py` is currently dirty.
- Any layout-only batch will leave the page telling learners something the code disproves. Either widen the scope (surface the sign/positivity constraint truthfully) or narrow the claim text — decide before implementation.

### C2. `[SOURCE]` All three pages violate the repo Definition of Done on emoji and em dash

`AGENTS.md:50` requires zero em dash and zero emoji in UI. Present in every one of the three pages:

- concept badge `🎯 มโนทัศน์หลัก` — riemann `:42`, area_between `:45`, volume `:47`
- observation block `👁️` — riemann `:55`, area_between `:58`, volume `:60`
- theory expander label `📖` — riemann `:60`, area_between `:63`, volume `:65`
- caution bullet `⚠️` — riemann `:73`, area_between `:76`, volume `:78`
- variable-detected info `✨ … — …` (emoji **and** em dash) — riemann `:139`, area_between `:138`, volume `:148`

Enforced on the redesigned limit page by `tests/test_limit_page_ux.py:39` (EMOJI regex) and `:205`. Reusing that assertion for these pages **fails until the emoji are removed**, and the shared expander label is also emoji-bearing across pages, so a label change is a multi-page edit (the same label string appears in the older sibling pages too).

### C3. `[SOURCE]` Identical page skeleton on all three: openness, not disclosure

All three follow the pre-pilot pattern the limit refactor abandoned:

- fully-open banner container `with st.container(border=True)` first (`riemann:28`, `area_between:31`, `volume:33`) — exactly the construct the pilot test forbids via `assert "with st.container(border=True):\n    col_badge" not in PAGE_SRC` (`tests/test_limit_page_ux.py:190`)
- long theory **before** any input/result (`riemann:60-76`, `area_between:63-79`, `volume:65-81`) → inputs and graph sit far below the fold
- worked steps printed **fully open** at the very bottom via `render_steps(...)` (`riemann:157`, `area_between:151`, `volume:161`) — the pilot moved these into a named expander (`pages/limit_approach.py:370`)
- no numeric inspection table on any of the three; the pilot page has one (`pages/limit_approach.py:316`, `:337`)
- on-page feedback is only `st.info/st.error` (`riemann:132/139/158`, `area_between:132/138/152`, `volume:142/148/162`); there is no honest short "per-case summary" akin to `_short_case_feedback` (`pages/limit_approach.py:77`)

### C4. `[SOURCE]` Shared theory dict exposes 6 fields; the pages render 4

`utils/theory.py` entries carry `conditions`, `formulas`, `properties`, `cautions`, `applications`, `decision_guide` (`utils/theory.py:17-53` riemann_sum, `:169-199` volume, `:200-230` area_between). All three pages render only `conditions`, `properties`, `cautions`, `applications` (`riemann:64-76`, `area_between:67-79`, `volume:69-81`). `formulas` and `decision_guide` are therefore **dead content** — including the left/right/midpoint definitions (`theory.py:26-28`), the Δx formula (`:29`), the increasing/decreasing inequalities (`:33-34`), and the disk-vs-washer decision rule (`:195-198`). This is available, already-written content; the pages instead re-state fragments of it by hand in the concept block.

### C5. `[SOURCE]` Keypad asymmetry and widget wiring

- `render_math_keypad(target_key, key_prefix, expanded, include_infinity, title)` (`utils/keypad.py:10-16`) writes into `st.session_state[target_key]` (`:19-31`), so the page's text input must use that exact key.
- riemann targets `riemann_expr` / `rie_kp` (`pages/riemann.py:118`); volume targets `volume_expr` / `vol_kp` (`pages/volume_revolution.py:116`); area_between targets **only f** (`area_f` / `area_f_kp`, `pages/area_between.py:123`) — a learner typing `g(x)` gets no keypad.
- riemann and volume initialize the target key at the top of the page and **also** pass `value=st.session_state.get(...)` to a widget with the same `key` (`riemann.py:103-106`, `volume_revolution.py:106-111`, `area_between.py:17-24` + `:106-108`). Passing both a default `value` and an externally-seeded `key` is the pattern that produces Streamlit's duplicate-value-for-widget warning. `[UNTESTED]` — needs a real run to confirm; flagged for the parent, not claimed.
- `pages/riemann.py:16` imports `X` from `utils/riemann_solver` and never uses it (dead import).
- area_between calls `inject_css()` explicitly (`:14`) although `render_hero` already calls `inject_css()` internally (`utils/theme.py:613`) → redundant double injection.

---

## 2. Page: riemann (`pages/riemann.py`, nav "3. ผลรวมรีมันน์")

### 2.1 Current order
1. `render_hero` (`:21`)
2. concept anchor — **open** container: badge, concept, Δx formula, convergence + increasing-function note (`:28-58`)
3. theory expander, 4 fields (`:60-76`)
4. divider, "ลองเล่นกับผลรวมรีมันน์" (`:78-83`)
5. 4 preset buttons (`:88-97`)
6. f(x) input + parsed preview + syntax guide (`:100-108`) | method selectbox with Thai labels via `format_func` (`:110-115`)
7. keypad (`:117-118`)
8. a, b, n (`:120-126`)
9. result latex (`:141-142`) → divider → graph (`:145-154`) → divider → **steps, open** (`:156-157`)

### 2.2 Required visible mathematical constraints (as actually relevant here)
- **Sign vs geometric area (missing):** the quantity computed is the signed sum `Σ f(x_i*)Δx` (`utils/riemann_solver.py:126`,`:163`); the page calls it "พื้นที่" and the plot labels the integral "Exact area" (`utils/plotter.py:126`). For `f<0` on the interval the true number is negative and neither the result block nor the graph says so. `theory.py:40` states the correct rule but is the only place it appears.
- **Orientation / monotonicity (partially stated):** underestimate-vs-overestimate depends on whether `f` is increasing or decreasing. The page states only the increasing case (`:57`); `theory.py:33-34` has both.
- **Bounds order:** `b > a` is mandatory and only surfaced as an error (`utils/riemann_solver.py:97-98`); the inputs (`:120-124`) are bare `st.number_input` with no inline guard.
- **n:** integer ≥ 1, slider range 1..50 (`:126`); solver rejects non-integer (`utils/riemann_solver.py:91-96`). Δx is shown only inside the graph title to 4 dp (`utils/plotter.py:132`).
- **Finiteness at sample points:** a pole anywhere in the sample set aborts with a Thai error (`utils/riemann_solver.py:116-124`); no pre-warning, e.g. preset `1/(x+1)` (`:97`) with `a = -1` fails.
- **Exact reference value:** computed live by `sp.integrate` (`:149-150`) and passed to the plot title only when finite and real; otherwise silently omitted (`:150`), so the learner cannot tell "no exact area" from "not computed".
- **Method notation mismatch:** midpoint uses `x̄_i = a+(i+0.5)Δx` for i=0..n-1 (`utils/riemann_solver.py:111`) while `theory.py:28` writes `a+(i-1/2)Δx` for i=1..n — equivalent, never reconciled on the page.

### 2.3 Duplicate / general text that should be collapsible
- convergence bullet (`:56`) is re-emitted verbatim as the final solver step on **every** run (`utils/riemann_solver.py:157`) → duplicate on every result.
- increasing-case note (`:57`) duplicates `theory.py:33-34`.
- Δx definition (`:49`, `:52`) duplicates `theory.py:24-29` (which are never rendered, see C4).
- the concept block itself is general orientation text, not input-specific → candidate for a named collapsed expander (C3).

### 2.4 UX proposals `[UNVERIFIED VISUAL PROPOSAL]` (source-level rationales, not observed in a browser)
- Move the experiment to the top (presets → inputs → n → method), keep a one-line truthful orientation/sign note above the fold, and collapse concept + theory into named expanders, mirroring `pages/limit_approach.py:145` / `:381` / `:420`.
- Add a short sign-aware summary next to the numeric result stating whether the value is a signed integral approximation or a geometric area — and state which, for the current `f`.
- Add a small numeric table (n, L_n/R_n/M_n, |approx − exact|) as the pilot does (`pages/limit_approach.py:337`); verification of claim is the learner-facing payoff.
- Show `Δx` and `b > a` validity in the control row instead of only in the error path.
- Collapse `render_steps` into a named expander ("วิธีทำทีละขั้นตอนฉบับเต็ม").
- Remove the emoji/em dash set (C2) and the dead `X` import (`:16`).

### 2.5 Hazards specific to this page
- Shares `utils/plotter.py` `plot_riemann` with nothing else directly, but the module also holds `plot_limit_near` used by the live page — editing the file touches the live session's page.
- Imports `METHODS`, `X`, `compute_riemann` from `utils/riemann_solver` (`:16-17`); `pages/limit_approach.py:25` and `utils/plotter.py:17` also import from that module → changes to it fan out to 3 files.
- Preset `"x^3 - 2x"` (`:93`) relies on `convert_xor` + implicit multiplication (`utils/riemann_solver.py:25-28`).

---

## 3. Page: area_between (`pages/area_between.py`, nav "5. พื้นที่ระหว่างเส้นโค้ง")

### 3.1 Current order
1. `inject_css()` (`:14`, redundant) → `render_hero` (`:15`) → session init for f/g/a/b (`:17-24`)
2. concept anchor — **open** container: badge, concept, formula with `f ≥ g` condition, top-minus-bottom + crossing notes (`:31-61`)
3. theory expander, 4 fields (`:63-79`)
4. divider, presets (`:84-100`) — 4 buttons incl. `x` vs `x²` on [0,1], `2−x²` vs `x²` on [−1,1], `cos x` vs `x` on [0,1.5], `x^{1/3}` vs `x` on [−1,1]
5. f(x) input + preview (`:104-110`) | g(x) input + preview (`:112-118`)
6. syntax guide (`:120`) → keypad **for f only** (`:122-123`)
7. a, b (`:125-129`)
8. result latex (`:140-141`) → divider → "گراف…" heading + plot (`:144-149`) → **steps, open** (`:151`)

### 3.2 Required visible mathematical constraints
- **Sign vs geometric area (contradicted on the page):** solver computes `∫|f-g|` (`utils/area_solver.py:156`, `:258`), per-piece `|∫|` (`:243`). The page's formula requires `f ≥ g` (`:55`) and warns that a swap yields a negative value (`:59`) — impossible with this solver. `theory.py:218` carries the same wrong warning.
- **Top/bottom orientation:** the page never tells the learner which curve is on top for the current interval; that information exists in the solver only indirectly via sign checks (`utils/area_solver.py:88-92`).
- **Crossings inside (a,b):** must split the integral (`theory.py:205`, `:219`). Solver does split and returns `res["crossings"]` (`utils/area_solver.py:275-278`, `:292`) — the page **never surfaces it** (it uses only `latex`, `steps`, `f_expr`, `g_expr`). The graph colors `f ≥ g` vs `g > f` regions (`utils/plotter.py:552-571`) but marks no crossing point.
- **Bounds:** `a < b` required (`utils/area_solver.py:160-161`); `a`,`b` come from `st.number_input` (`:125-129`). Bounds are re-derived as rationals via `Rational(str(val))` (`utils/area_solver.py:52-59`) and displayed with `_format_bound_latex` (`:62-70`) — note the page's own `x`/`y` axis labels and interval come from that formatting, so a float like `1.02` shows as `1.02` but is interned as `51/50`.
- **Single shared variable:** f and g must use one variable or the solver raises (`utils/area_solver.py:172-184`).
- **Real odd roots:** `x**(1/3)` needs the `real_root` conversion (`utils/area_solver.py:37-49`, mirrored in `utils/plotter.py:526`) — preset 4 depends on it.

### 3.3 Duplicate / general text that should be collapsible
- concept "เส้นบน ลบ เส้นล่าง" note (`:59`) ≈ `theory.py:218`; crossing note (`:60`) ≈ `theory.py:205`,`:219`; formula (`:55`) duplicates `theory.py:208` and is restated again by the solver's own step (`utils/area_solver.py:271`). Three copies of the same statement.
- concept container is general orientation text (`:31-61`) → collapsible candidate (C3).

### 3.4 UX proposals `[UNVERIFIED VISUAL PROPOSAL]`
- Surface `res["crossings"]` and annotate them on the graph; state explicitly "during (a,b) the curves cross N times, so the integral is split".
- Replace the swap-sign guidance with a truthful statement matching `∫|f-g|` (or change the solver, see C1) — one of the two, not both.
- Add a keypad for `g(x)` to match the f keypad.
- Collapse concept + theory + steps into named expanders; keep result + graph above them.

### 3.5 Hazards specific to this page
- Depends on `preview_math_expr(...)` twice (`:110`,`:118`) — the second call passes `label="พรีวิว g(x)"`, which `utils/math_render.py:217-219` special-cases by substring `"g(x)"`; a label rename silently changes the preview's `g(·)` naming.
- `plot_area_between` receives the **converted** expressions from the solver (`:146`), so the plotter's `MODULE_MAP` real-root shim (`utils/plotter.py:526`) is load-bearing; removing it from the plotter breaks preset 4's graph while the solver still succeeds.

---

## 4. Page: volume_revolution (`pages/volume_revolution.py`, nav "6. ปริมาตรของทรงตัน")

### 4.1 Current order
1. `render_hero` (`:15`) → session init incl. default `volume_inner = "x**2"` (`:17-26`)
2. concept anchor — **open** container: badge, concept, disk+washer formula, disk-vs-washer + `(R−r)²` trap notes (`:33-63`)
3. theory expander, 4 fields (`:65-81`)
4. divider, "ลองคำนวณ" (`:83-84`), presets (`:86-104`) — cone `x`, paraboloid `√x`, bell `4−x²`, washer `√x` / `x²`
5. R(x) input + preview (`:106-112`) + syntax guide (`:113`)
6. keypad (`:115-116`)
7. a, b (`:118-122`)
8. method selectbox — **raw English keys as visible labels** (`:124-128`)
9. inner r(x) input, only when washer (`:130-137`)
10. axis limitation caption (`:139`)
11. result latex (`:150-151`) → divider → graph heading + plot (`:154-159`) → **steps, open** (`:161`)

### 4.2 Required visible mathematical constraints
- **Axis of revolution (under-communicated):** only the x-axis (`y = 0`) is supported. It is stated once, in a small caption *after* all controls (`:139`), and in the plot legend (`utils/plotter.py:500`). A learner can pick a washer radius pair that only makes sense about another axis and get a plausible-looking number. `theory.py:172`/`:188` describe general axes and the "measure perpendicular to the axis" rule; the page has no selector and does not say "unsupported".
- **Radius is a distance (≥ 0):** a negative `R(x)` is squared silently (`utils/volume_solver.py:102`) → `V` for `|R|`; no warning anywhere.
- **Washer requires `R ≥ r`:** solver returns `abs(π∫(R²−r²))` (`utils/volume_solver.py:136`) → swapped radii give the **same positive** volume; the graph's shading uses `where=(ys_solid >= ys_inner)` (`utils/plotter.py:461-462`), so the swapped input draws *no* washer fill while still printing a number. `theory.py:189` warns about exactly this and the page cannot demonstrate it.
- **Method decision rule:** `decision_guide` (`theory.py:195-198`) is unused; the page paraphrases it in the concept note (`:61`).
- **Inner radius conditional on method:** the page only renders the r(x) box for washer (`:130-137`); when washer is selected with a blank box the solver errors clearly (`utils/volume_solver.py:83-88`) — correct behaviour, worth keeping.
- **Bounds:** `b > a` and both finite required (`utils/volume_solver.py:72-75`). The plotter **normalizes** with `min/max` (`utils/plotter.py:435-436`) — a latent graph/solver disagreement, currently unreachable because the solver rejects first.
- **Exact vs numeric result:** `result` is `float` only when the symbolic volume is a real number (`utils/volume_solver.py:115`, `:145`); the page renders `latex` unconditionally, so a non-numeric `V` still displays. Any future metric label must guard `None`.
- **Method labels:** selectbox options are literally `["disk", "washer"]` (`:124-128`) — English internals leaked as UI, unlike riemann's `format_func` (`pages/riemann.py:113`).

### 4.3 Duplicate / general text that should be collapsible
- `(R−r)²` trap note (`:62`) ≈ `theory.py:187` (theory caution) — same trap twice in one page.
- disk-vs-washer note (`:61`) duplicates the unused `decision_guide` (`theory.py:195-198`).
- formula block (`:54`,`:57`) duplicates `theory.py:177-178`.
- concept container is general text (`:33-63`) → collapsible candidate (C3).

### 4.4 UX proposals `[UNVERIFIED VISUAL PROPOSAL]`
- Promote the axis limitation out of the trailing caption into the control row (e.g. a disabled/annotated "แกนหมุน: แกน x (y = 0)" field) so it is visible before the learner commits to radii.
- Add truthful validation messages for `R(x) < 0` on the interval and for `r(x) > R(x)` instead of silently squaring / absolute-valuing.
- Thai labels for the method selectbox with a one-line decision phrase (uses content already in `theory.py:195-198`).
- Move the graph next to the method/radius controls; collapse concept, theory, steps.

### 4.5 Hazards specific to this page
- Imports `X` from `utils/riemann_solver` (`:10`) — a page→solver coupling through a module owned by the riemann batch; the same import exists in `pages/limit_approach.py:25` and `utils/plotter.py:17`.
- `render_math_keypad(... target_key="volume_expr" ...)` (`:116`) must stay aligned with the input key (`:110`) or the keypad silently writes nowhere.
- Session key `volume_inner` is initialized (`:25`) but only shown in washer mode, so stale inner expressions persist across method switches by design (`:88-94` callback also writes it).

---

## 5. Shared-file hazards (what the batch will collide with)

| shared file | used by our 3 pages for | blast radius | state |
|---|---|---|---|
| `utils/theme.py` | `render_hero(title, subtitle)` (`riemann:18`, `area:11`, `volume:11`); `render_hero` internally calls `inject_css()` (`utils/theme.py:613`) | every page (all import `render_hero`) | **dirty — live session** |
| `utils/keypad.py` | `render_math_keypad` 3 call sites (`riemann:118`, `area:123`, `volume:116`) | limit, solver, and any page using the keypad | **dirty — live session** |
| `utils/theory.py` | `THEORY_CONTENT["riemann_sum"|"volume"|"area_between"]` (`riemann:23`, `area:26`, `volume:28`); pages unpack 4 of 6 keys | 7 pages consume the same dict | **dirty — live session** |
| `utils/plotter.py` | `plot_riemann` (`riemann:151`), `plot_area_between` (`area:146`), `plot_volume` (`volume:156`) — all three plot functions live in **one file** | limit + improper pages share the module | clean, but the three page edits all need it |
| `utils/riemann_solver.py` | `compute_riemann`, `METHODS`, `X` (`riemann:16-17`) | `pages/limit_approach.py:25`, `utils/plotter.py:17`, `pages/volume_revolution.py:10` | clean |
| `utils/area_solver.py` / `utils/volume_solver.py` | page solvers | page-only | clean |
| `utils/math_render.py` | `preview_math_expr`, `render_latex`, `render_steps`, `render_syntax_guide` | every page | clean |
| `pages/limit_approach.py`, `tests/test_limit_page_ux.py`, `tests/test_limit_solver.py` | pattern reference only | live session owns them | **dirty / untracked** |

Rule that follows: `utils/plotter.py` is a **single-choke-point** file for all three pages — never let two page-batches edit it concurrently. And no batch may write while the live session holds `theme.py`/`keypad.py`/`theory.py`; re-check the hashes in §"Audit baseline hashes" before any integration, and stop/rebase on drift.

---

## 6. Existing test seams

- `tests/test_pages_apptest.py:15-18` — parametrizes every `pages/*.py`, mounts and asserts no exception. **Every edit to these three pages must keep the default run exception-free** (e.g. washers with a blank inner radius must still not raise).
- `tests/test_riemann_solver.py` (111 lines), `tests/test_area_solver.py` (89), `tests/test_volume_solver.py` (71) — solver-level behaviour including invalid bounds and unsupported method (`test_volume_solver` shows `test_compute_volume_invalid_bounds`, `test_compute_volume_unsupported_method`). These pin the current semantics: **any change to `abs()` behaviour in `area_solver`/`volume_solver` must update these tests in the same change.**
- `tests/test_plotter.py:24-60` — one smoke test per plot function plus `test_plot_volume_washer` asserting `len(ax.lines) >= 4` (`:58`) and `test_constant_curves_have_matching_shapes` asserting `ax.collections` (`:19`). Any plotter relabel/restructure must keep these green.
- `tests/test_limit_page_ux.py` — the **page-level UX pattern to clone** (AppTest rendering helpers `:50-58`, visible-text collection `:61-68`, raw-LaTeX leak scan `:78-88`, order assertions `:155-177`, named-expander assertions `:179-192`, emoji-free source assertion `:203-212`, per-case truthfulness `:251-299`). It is untracked and owned by the live session — copy the shape, do not import from it.
- Recommended new seams (one per page, so batches never share a test file): `tests/test_riemann_page_ux.py`, `tests/test_area_between_page_ux.py`, `tests/test_volume_page_ux.py`.

---

## 7. Recommended batch group / order

Grouping rationale is shared-file contention, not nav order.

1. **Batch R (riemann)** — alone. It is the oldest skeleton, has no `abs()`-masking defect, and its pilot-shaped rewrite is the cheapest to review (fewest shared-file edges: `plotter.plot_riemann` only).
2. **Batch AV (area_between + volume_revolution)** — one review unit, implemented **sequentially**, because both:
   - need the same `utils/plotter.py` label/semantics decision ("Area (f >= g)" `:560`, "Exact area" `:126`, reflection labels `:455-458`),
   - hinge on the same C1 positivity/`abs()` correctness question in their solvers,
   - share the "surface crossings / radius validation" pattern.
   Do them one file at a time so the plotter diff stays single-authored.
3. **Do not** put `pages/substitution.py` or `pages/improper_integrals.py` in this group — they belong to the separate read-only audit, and `plot_substitution` is a stub (`utils/plotter.py:411-413`).
4. **Do not** touch `pages/limit_approach.py`, `tests/test_limit_page_ux.py`, `utils/theme.py`, `utils/keypad.py`, `utils/theory.py` while the live session holds them.

Order within any batch: record hashes → snapshot the page → implement page-local layout → only then request shared-file changes (`plotter`/`solver`) as a separate reviewed step.

---

## 8. Blockers / decisions the parent must make

1. **Scope of C1.** Sign-vs-geometric-area and washer/radius positivity are solver-and-plotter correctness issues. A layout-only batch cannot fix them; it can only stop the page from asserting something false. Decide: (a) pages-only + truthful wording, or (b) widen to `area_solver`/`volume_solver`/`plotter`/`theory`. Everything else in this audit is independent of that choice.
2. **`theory.py` ownership.** The pages and `theory.py:218`/`:189` currently contradict the solvers in the same way. Whichever side changes, both must change together — and `theory.py` is dirty in another session.
3. **Emoji/em-dash removal (C2)** is a prerequisite for reusing the pilot's source-scan assertions, and it changes the shared expander label text used across pages.
4. **Unverifiable-here items** that must be checked by the parent with a real run: the `value=` + `key=` duplicate-value warning (C5), and every `[UNVERIFIED VISUAL PROPOSAL]` above. No browser was opened and no test was executed in this audit.

Page count audited: **3** (riemann, area_between, volume_revolution).
