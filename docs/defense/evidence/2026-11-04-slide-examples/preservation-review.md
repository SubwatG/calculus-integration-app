# S07 Preservation & Architecture-Figure Provenance Review

Read-only audit. No source writes; only this report was created.
Snapshot taken 2026-11-04 ~12:17 (+07). **The working tree changed while auditing** (main HTML mtime 12:16:25) — hashes below pin the reviewed state.

## 0. Snapshot identities

| Artifact | Identity |
|---|---|
| Baseline commit | `0b10b63` |
| Baseline deck blob | `dd5708ec43650287cb51e7ff72d002d6b74349f1` (10,495,509 bytes) |
| Reviewed deck file | sha256 `1058e7b2…c8288`, 12,841,892 bytes, 34 slides |
| Builder (tracked, dirty) | `build_defense_deck.py`, sha256 `ddf8f8cb…9b32`, 113,802 bytes, S07 hunk only |
| Figure | `figures/architecture-workflow-full.png`, sha256 `340878ee…9964`, 2,896×957 RGB, 1,759,991 bytes, **untracked** |
| Stale evidence | `figures/screenshot-slide-07.png`, 1440×900, 232,215 bytes, **untracked** |
| Competing variants | `build_defense_deck_v2.py` + `slide-deck-defense-v2.html` (15,205,296 B), `build_defense_deck_focus.py` + `-focus.html` (10,499,243 B) — all untracked |

## 1. Preservation invariant: PASS (byte-level proof)

Method: split both files on the literal `<div class="slide">` marker (34 occurrences each) and compare raw bytes outside slide 7.

```
markers base/cur        34 / 34
prefix bytes equal      True   (everything before S07)
suffix bytes equal      True   (everything from S08 through </html>)
delta                   2,346,383 bytes, all inside S07
S07 old/new             2,918 B -> 2,349,301 B
```

Consequences, verified rather than assumed:
- S01–S06 and S08–S34 are byte-identical to `0b10b63`.
- `<head>` incl. all `<style>`, top nav, lightbox modal, progress rail, footer, `<script>`, counters are byte-identical.
- No CSS/JS/nav/zoom/zen changes leaked in (unlike the v2 build, see §6).
- `07 / 34` counter and speaker chip `เบญจกัฬยาณี` unchanged.
- `build()` is reproducible: re-running it in memory yields exactly the file on disk (same sha256 `1058e7b2…`), so no drift between builder and artifact.

## 2. What the S07 change actually is

Single hunk in `build_defense_deck.py`: `@@ -393,45 +393,36 @@` (S07 only, 31 insertions / 40 deletions). No other hunk touches CSS, JS or chrome.

New S07 structure: `.grid-2` with `grid-template-columns:0.8fr 1.6fr`
- Left: 3 compact `academic-card`s (Frontend / Backend / Data & Storage), one sentence each.
- Right: `<figure class="academic-card">` containing a `<button>` with the base64 `<img>` and a 3-line `<figcaption>`.
- Title changed to "จากเนื้อหาบทเรียน ผ่านการประมวลผล สู่การใช้งานบนเว็บ"; section label "3. วิธีดำเนินงาน · สถาปัตยกรรมระบบ 3 ชั้น" retained (still 1 occurrence, no agenda/overview drift).
- Lightbox reuses the original base function: `onclick="openLightboxModal(this.querySelector('img').src, 'ผังแนวคิดสถาปัตยกรรมจากข้อเสนอโครงงาน')"`. `openLightboxModal(src, caption)` exists in the base blob at the same place; no JS added.

## 3. CSS/JS dependency audit: no additions needed

Checked each selector/feature the new markup uses against the base stylesheet:
- `.grid-2` exists in base (`.grid-2 { display:grid; grid-template-columns:1fr 1fr; gap:1rem; … }`); inline `grid-template-columns` overrides it.
- `.academic-card`, `.card-heading`, `.slide-body`, `.slide-header` rules identical between base and v2.
- Base already ships KaTeX (7 refs, `renderMathInElement` ×4) and `openLightboxModal` (21 refs).
- `<figure>` has no global rule; inline `margin:0` prevents UA default margin.
- Tag balance inside S07 is clean (no unclosed elements); the extra `</div>` closes the slide wrapper.

Layout budget (computed, not rendered): inner width 1,156.8 px → figure column ≈ 760.5 px, inner image ≈ 736.5 px → image height ≈ 243 px at 2896:957 (under the 360 px cap). Figure card ≈ 363 px tall, left column ≈ 291 px, header ≈ 95 px, padding 64 px → ≈ 522 px of the 740 px `.slide` max-height. No overflow expected; body stays centered.

Content check: no em dash (`—`), no emoji, no Unicode arrow in S07. The "265 Tests" style claim from the v2 variant is **not** carried into this version, which is correct/safer.

## 4. Figure provenance

- Untracked working-tree file, no PNG text/EXIF chunks (`im.info` empty), no generator script anywhere in the repo (`grep -rn architecture-workflow` → only `build_defense_deck_v2.py:945` before this change; the new builder resolves it through `img_b64`).
- Only indirect origin evidence: filename, and `build_defense_deck_v2.py` calling it under caption "แผนภาพสถาปัตยกรรมระบบและกระบวนการทำงานครบวงจร"; the new figcaption calls it "ผังแนวคิดจากข้อเสนอโครงงาน" (proposal figure). No commit ever tracked it, so the claim is **unverifiable from git**.
- Embedded copy integrity proven: base64 payload in S07 decodes to exactly 1,759,991 bytes, sha256 `340878ee…9964` = the on-disk PNG. One URI occurrence only (v2 embedded it twice, ~4.7 MB).
- Dimensions claim "2896×957" (spec doc) matches the real header `2896 x 957`.
- Text extraction (tesseract, no vision) confirms the three panels `CONTENT & RESOURCES` / `APPLICATION ARCHITECTURE` / `USER EXPERIENCE & DEPLOYMENT PATH`, plus `User Progress (Future)` and `GitHub / Version Control` → `Streamlit Community Cloud`. That validates the caption's Future hedge and the deployment wording that actually appears in the figure.
- The figure also depicts capabilities phrased as complete ("Quiz Engine", "Visualization Engine"), so the existing hedge ("ไม่ใช่รายการความสามารถที่ทดสอบแล้วทั้งหมด") is necessary, not decorative.

## 5. Risks, ranked

1. **Figure is untracked → build is not reproducible from a clean clone.** `img_b64()` raises `FileNotFoundError` without `docs/defense/figures/architecture-workflow-full.png`. Commit the PNG (1.7 MB) with the builder change, or the deck cannot be regenerated.
2. **Stale evidence artifact.** `figures/screenshot-slide-07.png` (12:04) is a screenshot of the *v2* S07: 3-column layout, chip "265 Tests • CI Green", preview strip, title "…Frontend • Backend Services • Data & Storage". It is not the current 2-column S07. Do not cite it as proof of the shipped slide; regenerate or delete.
3. **Spec/deck drift.** Dirty `slide-deck-specification.md` still describes the v2 S07 ("บูรณาการ 3 ภาคส่วน", "2896x957" callout) and the title "สถาปัตยกรรมระบบและกระบวนการทำงานครบวงจร", while the built slide uses "จากเนื้อหาบทเรียน …" with a 2-column figure + caption. Align the spec text before submission.
4. **No on-disk backup of the main HTML.** Only `slide-deck-defense-v2.html.backup-*` exists. Recovery depends on the git blob (verified reachable) — acceptable, but note it.
5. **Three competing builders/artifacts** in `docs/defense/` (`build_defense_deck.py` = canonical; `_v2.py`; `_focus.py`; plus 14.5–15.2 MB HTML variants). Using v2 would silently rewrite global chrome — see §6. Recommend retaining only the canonical builder in the final tree (vault R3: version via git, not filenames).
6. **In-figure legibility.** At ~736 px width the 2896 px figure is downscaled ~3.9×, so node labels are effectively unreadable on-slide; the lightbox is the only mitigation. Acceptable for a summary slide, but do not claim the on-slide image is legible.
7. **Low:** a 2.35 MB data URI inside a `src` attribute is heavy (12.8 MB page, +22% vs base). It parses in a single copy, and print/export behavior was not verifiable without a browser.
8. **Concurrency:** the builder and HTML changed at 12:16 during this audit. Re-run the §7 check after any further edit; earlier state (04:xx–12:04) was the v2 output and does **not** satisfy the invariant.

## 6. Why the v2 builder must not be used for this deliverable

`build_defense_deck_v2.py` output (the previous dirty HTML, sha `08187096…`) differs from base far beyond S07:
- +263 CSS lines (`.top-nav-hidden`, `.btn-nav-collapse`, reveal button, `.canvas-nav-arrow`, zoom/`.is-zoomed`, footer zoom group);
- new JS functions `toggleTopNav`, `setZoom`, `zoomIn`, `zoomOut`, `resetZoom`, `updateFullscreenBtn`;
- replaced top-nav controls (prev/next/collapse/fullscreen) and footer markup;
- S07 embeds the PNG twice (~4.7 MB) and S34 segment carries chrome edits.

That violates "all other slide HTML and controls byte exact against 0b10b63". The current canonical build keeps every control identical.

## 7. Minimum implementation (already realised; recipe for re-application)

1. Edit only the `S07 = slide(...)` body in `build_defense_deck.py` (no CSS/JS/head/chrome edits). Keep `img_b64("architecture-workflow-full.png")` resolved at build time; one `src` occurrence; `onclick` via `this.querySelector('img').src`; caption states the figure is conceptual and marks `User Progress (Future)`.
2. Run `python3 docs/defense/build_defense_deck.py` (writes `slide-deck-defense.html`).
3. Gate before declaring done:

```python
import subprocess
base = subprocess.run(["git","show","0b10b63:docs/defense/slide-deck-defense.html"],
                      capture_output=True).stdout
cur  = open("docs/defense/slide-deck-defense.html","rb").read()
m = b'<div class="slide">'
bi = [i for i in range(len(base)) if base.startswith(m,i)]
ci = [i for i in range(len(cur))  if cur.startswith(m,i)]
assert len(bi) == len(ci) == 34
assert base[:bi[6]] == cur[:ci[6]]      # head + S01..S06 byte exact
assert base[bi[7]:] == cur[ci[7]:]      # S08..S34 + footer/JS byte exact
print("PASS: only S07 differs")
```

This assertion passed on the reviewed snapshot.

## 8. Remaining work owned by the parent

- `git add docs/defense/figures/architecture-workflow-full.png` (+ `build_defense_deck.py`, `slide-deck-defense.html`).
- Sync `slide-deck-specification.md` S07 lines to the shipped title/structure (2-column + figcaption), then re-run the §7 gate.
- Replace/delete stale `screenshot-slide-07.png`; do not attach it as current evidence.
- Decide whether the large uncommitted v2/focus artifacts stay.
