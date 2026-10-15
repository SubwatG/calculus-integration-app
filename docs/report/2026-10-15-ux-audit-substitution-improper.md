# UX/Structure Audit — `pages/substitution.py` + `pages/improper_integrals.py`

- Repo: `/home/kitti/Documents/GitHub/calculus-integration-app`
- Date: 2026-10-15 (+07)
- Scope: READ-ONLY source audit. No edits, no browser, no services, no git.
- Evidence class: **source review only**. Line numbers are from the on-disk files as read now.
  Every "visual"/render claim below is *inferred from source*, NOT visually verified in a running app.
  No tests were executed (read-only constraint); test status is described from source, not from a run.
- Binding context: repo `AGENTS.md` (logic in `utils/`, Thai UI, no emoji/no em-dash/no `→` in UI, `$...$`/`$$...$$` only).
- Approved principle carried in from the limit pilot (`tests/test_limit_page_ux.py`): **experiment first; visible result + one short truthful summary; details collapsed into named expanders; instructional content preserved, not deleted.**

---

## 1. Baseline facts

| File | Lines | Bytes | Tabs | Expanders | Graph |
|---|---|---|---|---|---|
| `pages/substitution.py` | 572 | 47,676 | 3 | 1 (`expanded=True`) | none (stub) |
| `pages/improper_integrals.py` | 149 | 8,401 | 0 | 1 (collapsed) | yes (`st.pyplot`, source-review) |

Both pages are **page-level only**: heavy literals live in `pages/`, not `utils/` (contrary to AGENTS.md §3, but consistent with every other page — see §7 hazard H5).

---

## 2. Current flow — `pages/substitution.py` (per mode)

### 2.0 Global shell (before tabs) — `substitution.py:15-59`
1. `render_hero("เทคนิคการอินทิเกรต", ...)` — L15-18
2. `st.expander("เข็มทิศการตัดสินใจ: ...", expanded=True)` — L23-51 — **two columns of theory** (u-sub chain-rule rules vs by-parts LIATE rules) shown **open, above any interaction**. ← first pilot-principle violation.
3. divider L53 → `st.tabs([u-Sub, By Parts, SymPy CAS])` L55-59

### 2.1 Tab 1 — u-Substitution (L64-289)
- `1.1` 4-pattern summary: 2 columns, 4× (`st.markdown` label + `st.latex` + `st.caption`) — L65-91
- `1.2` `selectbox` (4 cases, key `select_u_case`) L104-109
- Per case: `st.latex(problem)` → `st.radio(index=None, key=radio_u_caseN)` → branch:
  - `None` → `st.info` prompt
  - **correct** → `st.success` + 5 named steps (`ขั้นที่ 1..5`) each `st.markdown` + `st.latex`, ending in derivative verification
  - **wrong** → `st.warning` / `st.error` / (occasionally `st.info` for a valid-but-inferior route)
- Case map: case1 `∫2x√(x²+1)dx` L114-157; case2 `∫(ln x)/x dx` L162-202; case3 `∫cos(x)e^{sin x}dx` L207-244; case4 `∫x√(x+1)dx` L249-289

### 2.2 Tab 2 — Integration by Parts (L295-505)
- `2.1` LIATE principles + a 5-row markdown table (L / I / A / T / E) — L296-318
- `2.2` `selectbox` (4 cases, key `select_p_case`) L332-337
- Per case same radio→branch shape; case4 (cyclic) success branch only, "0=0 trap" as `st.error` — L469-505

### 2.3 Tab 3 — SymPy CAS solver (L511-572)
- 7 preset buttons (2 rows) L518-535 → `st.text_input(key="substitution_expr")` L537-542 → `preview_math_expr` L543 → `render_syntax_guide` L544 → `render_math_keypad(expanded=False)` L546
- `st.button("คำนวณผลลัพธ์")` L548 → `solve_substitution()` L552 →
  - `res["ok"]` → optional variable-detect `st.info` L556 → `render_latex(res["latex"])` L559 →
    - `status=="non_elementary"` → `st.warning` L562
    - else if `u_candidate` → `st.info` u/du hint L566
  - divider L568 → `render_steps(res["steps"])` L570
  - `not ok` → `st.error(res["error"])` L572

**Result vs steps gap (tab3):** result LaTeX and the u-hint are separate blocks (L558-566) with a divider THEN steps (L568-570). The solver emits an *unordered* step list (`substitution_solver.py:134-159`) — it does not guarantee the u/du line precedes the result line in reading order. Source-review note only.

---

## 3. Current flow — `pages/improper_integrals.py` (single page, mode = interval type)

### 3.0 Shell
1. `inject_css()` L15 → `render_hero(...)` L16
2. **OPEN** `st.container(border=True)` "Concept Anchor + What to observe" L23-53 — includes:
   - badge `🎯 มโนทัศน์หลัก` L26-39
   - the defining limit `∫_a^∞ = lim_{t→∞}∫_a^t` L47
   - `st.info` "👁️ จุดที่ควรสังเกต…" with a convergence-vs-divergence note **and the p-test rule** (`1/x^p` converges iff `p>1`) L49-53
   → **long concept block above the experiment**; second pilot-principle violation.
3. collapsed `st.expander("📖 รายละเอียดทฤษฎี …", expanded=False)` L55-71 reading `THEORY_CONTENT["improper"]` (conditions/properties/cautions/applications)
4. `### ลองคำนวณ` L74 → 4 preset buttons L81-90 → `text_input(key="improper_expr")` L92-97 → `preview_math_expr` L98 → `render_syntax_guide` L99 → keypad L101-102
5. `a`/`b` text inputs L104-116 → caption listing supported interval shapes L118
6. **Result:** L120-149
   - empty → `st.info` L121
   - `compute_improper(expr,a,b)` L123 → `### ผลลัพธ์` + `render_latex(res["latex"])` L129-130
   - status `divergent` → `st.warning`; `unsupported` → `st.info` L132-136
   - **Graph** L140-145 (`plot_improper(res["expr"], a_input, b_input)` inside try/except)
   - **Steps last**: `render_steps(res["steps"])` L147
   - `not ok` → `st.error` L149

### 3.1 Solver modes (`utils/improper_solver.py`) — what each branch decides
| Mode | Branch | Status logic | Evidence |
|---|---|---|---|
| (-∞,∞) split at c | L150-201 | left/right classified; any `divergent` ⇒ whole `divergent` (explicitly "ไม่สามารถนำ ±∞ มาหักล้างกันได้" L304 in the interior twin) | L161-190 |
| (-∞, b] | L206-235 | single `sp.integrate` + classify | L210-224 |
| [a, ∞) | L240-269 | single `sp.integrate` + classify | L244-258 |
| [a,b] plain | L319-338 | `sp.integrate` + classify | L323-336 |
| [a,b] with interior singularity | L279-318 | split at **first** singularity `interior_sings[0]` L282; left/right classified; any divergent ⇒ whole divergent (no PV) | L292-306 |

`_classify_improper` (L53-65): `Integral`→unsupported; `nan/zoo`→divergent; `AccumulationBounds`→divergent; `±oo`→divergent; finite+real→finite; else unsupported.
`_find_interior_singularities` (L107-121): **denominator roots only** — misses singularities from other causes (see H2).

---

## 4. What must remain visible (do not collapse / do not hide)

**Both pages**
- The **result** and its **status** as one visible unit: substitution `render_latex` + non-elementary warning (`substitution.py:559-562`); improper `render_latex` + divergent/unsupported message (`improper_integrals.py:130-136`).
- **Method assumption of the current case** — for substitution, which u / which u,dv pairing the branch is validating (the `st.success`/`st.warning` verdict line). Collapsing the *worked steps* is fine; hiding *which assumption was checked* is not.
- **Domain / interval** — for improper, the exact `a`,`b` (incl. `±inf`) as the integral is defined; the caption at L118 is the only place supported-shape semantics are stated.

**Per mode, must stay visible**
| Mode | Must remain visible | Evidence |
|---|---|---|
| u-Sub case (all 4) | the verdict (valid / valid-but-inferior / invalid) and *why*, in the Thai one-liner | L131,150,153,156 ; L179,198,200,202 ; L224,240,242,244 ; L267,287,289 |
| By-Parts case (all 4) | the LIATE verdict + the "complexity increased" / "cyclic 0=0 trap" warning | L358,376,381 ; L402,420,422 ; L444,462,464 ; L486-489 |
| Cyclic case | the algebraic step `2I = …` (the whole point) | L505 |
| Solver (tab3) | non-elementary verdict (special function name) and the u/du recommendation | L562,566 |
| Proper-divergent | **divergent is a result**, not an error: keep `st.warning` + the definitional sentence ("ถ้ามีส่วนย่อยอย่างน้อย 1 ฝั่งลู่ออก …") | `improper_solver.py:174,304-305` |
| Interior-singularity | the split-at-c definition and the no-PV note | `improper_solver.py:286-289,305` |
| All improper modes | **the graph cutoff disclosure** (see §5, CUT) | `plotter.py:607-630` |

---

## 5. What can collapse (safe to move into named, collapsed expanders)

- `substitution.py:23-51` decision compass → collapse (`expanded=False`) and/or move below the tabs is unsafe (it is cross-tab); **collapse in place** is the low-risk move.
- `substitution.py:65-91` (4-pattern summary) and `:296-318` (LIATE table) → collapsible "ทฤษฎี/เกณฑ์ตัดสินใจ" expanders; the table is reference, not first-read.
- `substitution.py:134-148 / 182-196 / 227-238 / 270-285 / 361-374 / 405-418 / 447-460 / 493-505` (per-case worked steps) → collapsible "วิธีทำทีละขั้นตอนฉบับเต็ม" per case (mirrors the limit page's `"วิธีทำทีละขั้นตอนฉบับเต็ม (Full Worked Solution)"` expander).
- `substitution.py:518-546` presets + syntax guide + keypad → keypad and syntax guide are already collapsed; presets could fold into one expander, but they are cheap and useful — low priority.
- `improper_integrals.py:23-53` **open** concept container → collapse into a named expander and/or move the "what to observe" bullets below the experiment. The defining limit (L47) is the anchor and should stay visible.
- `improper_integrals.py:55-71` theory → already collapsed; keep.

**Preserved teaching content (must survive any collapse, verbatim or equivalent):**
- Convergence vs divergence definition (`improper_integrals.py:44,47,51`)
- p-test rule (`1/x^p` converges iff `p>1`) — `improper_integrals.py:52`
- chain-rule / product-rule justification for u-sub vs by-parts — `substitution.py:29,43`
- LIATE ordering table — `substitution.py:310-317`
- The 4 u-patterns and 4 by-parts archetypes (`substitution.py:75-90`, presets L521-535)
- Verification-by-differentiation step in every correct branch

---

## 6. Proposals (aligned to approved principle; NO batch implementation now)

**P1 — improper page: invert theory/experiment order.** Move the open concept container (`improper_integrals.py:23-53`) below the inputs/result, or convert to a collapsed named expander; keep the defining limit line visible. Rationale: matches limit-pilot D3; smallest page; highest teaching payoff.

**P2 — improper page: label graph cutoffs (high priority, truthfulness).** `plot_improper` shades a **finite truncation** but the legend says "Area over [a, ∞)" / "Area over (-∞, ∞)" (`plotter.py:611,617,623`). The pedagogical claim "this shaded region is the improper integral" is false; it is `∫_a^{a+5}` etc. Proposal: change the shade label to state the cutoff (e.g. "แสดงช่วง [a, a+5] เพื่อดูแนวโน้ม; ค่าจริงได้จากลิมิต") **and** render `res["result"]` (the exact value or "diverges") adjacent to the graph as the authoritative number. Keep the graph even for `divergent` (instructive) but pair it with the explicit divergence note. — *Source-review claim; not visually verified.*

**P3 — substitution page: collapse the top compass + per-case worked steps.** `substitution.py:23-51` → `expanded=False`; each case's 5-step block → one collapsed "วิธีทำละเอียด" expander; keep the verdict + one-line reason visible above it. Matches limit-pilot D6.

**P4 — fix the dead branch (correctness defect, source-confirmed).** In case 4, `substitution.py:266` already catches `"แนวทาง D"`, so the `elif "แนวทาง D" in u_choice:` at **`substitution.py:286-287`** is **unreachable**. Its text is the *correct guidance for option C* (`u=√(x+1)`, "ได้คำตอบเดียวกัน"). Net effect: choosing **option C** falls through to the final `else` at L288-289 which says "**[ไม่สามารถแก้ได้]**" — mathematically wrong (C is a valid, if messier, route). Fix the condition to `"แนวทาง C"`. Evidence: `substitution.py:257` (option C label) vs `:266`, `:286`, `:288-289`.

**P5 — emoji hygiene (contract conflict, flag not fix).** Repo `AGENTS.md:50` bans emoji in UI. Present: `substitution.py:556 (✨), :566 (💡)`; `improper_integrals.py:37 (🎯), :50 (👁️), :55 (📖), :68 (⚠️), :127 (✨)`. The limit pilot's test asserts emoji-free labels for the limit page only. Any new page test copied from `test_limit_page_ux.py` will **fail** these two pages until cleaned. Decide deliberately (clean the touched pages, or scope the assertion).

**P6 — dead import / cross-page coupling.** `improper_integrals.py:11 from utils.riemann_solver import X` is unused on that page (only `plot_improper` uses `X`, via its own import `plotter.py:17`). Low risk; remove when the page is next touched.

**P7 — (defer) `inject_css()` inconsistency.** Only `quiz.py:43`, `area_between.py:14`, `improper_integrals.py:15` call `inject_css()`; `substitution.py` does not. Normalizing changes styling globally — **defer**, out of scope for a page UX batch.

---

## 7. Shared hazards (cross-cutting)

- **H1 — Shared modules under concurrent edit.** `theme.py` (`inject_css`, `render_hero`), `keypad.py` (`render_math_keypad`), `theory.py` (`THEORY_CONTENT`), `limit_solver.py` are being edited by other Hermes sessions right now. Both audited pages import from these (`substitution.py:10,13`; `improper_integrals.py:8,9,11,12,13,101`). **Do not touch them**; if a page refactor needs a shared change, stop and hand off.
- **H2 — Interior-singularity detection is denominator-only.** `_find_interior_singularities` (`improper_solver.py:107-121`) only roots `sp.denom`. Singularities from non-denominator causes (e.g. `log(x)` at `x=0`, `tan` poles, endpoint singularities inside `(a,b)` that aren't denominator roots) are **missed** ⇒ a `[a,b]` integral could be reported `finite` without the required split. Page-level UX cannot fix this; flag as a solver gap (out of READ-ONLY scope).
- **H3 — Cutoff truthfulness (see P2).** The graph's finite truncation is presented with an infinite-interval label. This is the single highest-severity *teaching* hazard on the improper page.
- **H4 — Emoji / label assertions.** Copying the limit-UX test template introduces an emoji-free assertion that both pages currently violate (P5).
- **H5 — Logic-in-pages.** Both pages embed long Thai teaching logic as literals in `pages/` (all 572 + 149 lines). AGENTS.md §3 wants logic in `utils/`. Refactors should **not** try to fix this now (would be a "new global abstraction / batch" — explicitly out of scope).
- **H6 — Order of result vs steps.** Both pages call `render_steps` after the result; improper puts the graph *between* result and steps (`improper_integrals.py:140-147`). Any reordering must keep the "visible result" criterion (limit-pilot D3/`test_result_metric_appears_before_theory`).

---

## 8. Existing test seams (identified from source; NOT run)

| Seam | File | What it pins | Relevance |
|---|---|---|---|
| Page smoke (all pages) | `tests/test_pages_apptest.py` | every `pages/*.py` mounts default run without exception (AppTest, timeout 5) | **Must stay green** for any layout change |
| substitution solver | `tests/test_substitution_solver.py` (7 tests) | basic u-detection, `u=x**2+x`, non-elementary `erf`/`Si`, empty⇒error, latex, variable `t` | regression net for tab3 |
| improper solver | `tests/test_improper_solver.py` (13 tests) | finite semi-infinite, finite-bounds latex, harmonic divergence, endpoint singularities, interior singularity ≠ PV, `(-∞,∞)` convergent to π, lower-infinite `exp` | regression net for the page's modes |
| **limit page UX template** | `tests/test_limit_page_ux.py` (23 tests) | named expanders, experiment-before-theory ordering, result-before-theory, graph-next-to-control, emoji-free labels, no raw-LaTeX leaks, no invented method, "สรุปสั้น" single summary | **the pattern to copy** for new substitution/improper UX tests |
| No page-UX test exists | — | `substitution.py` and `improper_integrals.py` have **no** page-level UX test today | new assertions are net-new |

Reusable conventions to lift from `test_limit_page_ux.py`: `_visible_texts(at)`, `_raw_latex_leaks(at)` (bare `\cmd` outside `$...$` — note the limit page's D1/D2 defect class), `NAMED_EXPANDERS` set assertion, `PAGE_SRC` source-order checks (`test_graph_is_rendered_next_to_delta_control`), single "สรุปสั้น" feedback contract.

---

## 9. Suggested batch order (when approved)

1. **Batch A — `improper_integrals.py` + new `tests/test_improper_page_ux.py`.** Smallest, self-contained; carries H3/P2 (cutoff labeling + show exact `res["result"]`) and P1 (experiment-first). Copy the limit UX test template. Gate on `test_pages_apptest.py` + `test_improper_solver.py` staying green.
2. **Batch B — `pages/substitution.py`.** Larger and branch-dense: P4 (dead branch — do this **first**, it is a correctness fix), then P3 (collapse compass + worked steps), then P5 emoji in tab3. Add `tests/test_substitution_page_ux.py`. Gate on smoke + `test_substitution_solver.py`.
3. **Batch C — hygiene (optional).** P6 dead import; decide P5 scope for both pages. Defer P7 (`inject_css`).
4. **Not in any batch now:** H2 solver gap, H5 logic-in-pages refactor, any change to shared modules (H1).

---

## 10. Untested-claim register

- All layout/ordering/visibility statements are **source-review**; none were visually confirmed in a running Streamlit app.
- `st.pyplot` graph rendering, cutoff extent `[a,a+5]`/`[-5,5]`/`[a-1,a+8]` in the rendered figure are read from `plotter.py`, not observed.
- Test files were read, **not executed**; "must stay green" is a requirement, not a verified current state.
- `substitution_solver` u-candidate heuristic quality (`_detect_u_candidate`, `substitution_solver.py:54-76`) was reasoned from source only.
