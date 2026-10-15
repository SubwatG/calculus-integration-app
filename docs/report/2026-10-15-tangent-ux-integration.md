# Tangent UX integration evidence

## Scope and status

Integrated `pages/tangent.py` and new `tests/test_tangent_page_ux.py` only. No shared helper/theme/solver edits in this pilot. Other lessons audited read-only; no batch implementation authorized yet. No commit, push or service restart.

Original tangent bytes matched worker baseline immediately before integration. Backup: `/home/kitti/.hermes/profiles/teaching-orchestrated/cache/scratch/tangent-live-backup-bc6s80gz/tangent.py`. Another session's newer theme was retained, not replaced by candidate.

## Parent changes after candidate review

- Replaced an epsilon-based zero-slope classification with exact zero comparison: a small nonzero slope must not be labelled stationary.
- Replaced overly specific non-differentiability feedback with a modest statement based on reported solver status, without inferring every case is a corner or excluding vertical geometric tangents.

## Verification

Executed in the live project after final page changes:

`env -u PYTHONPATH .venv/bin/python -m pytest tests/ -q -p no:cacheprovider`

Result: **218 passed in 24.06s**. `rtk git diff --check` produced no errors.

Served page: `http://localhost:8501/tangent`. Browser DOM/interactions verified:

- Experiment heading is before results and theory.
- Worked solution, main concept and full theory are collapsed initially.
- Default polynomial displays slope `2.0000` and positive-slope feedback.
- Selecting `sin(x)` displays `1.0000` and updates feedback.
- Returning to `x^2` and opening the worked-solution expander exposes step 7 without a Streamlit exception; expander closed afterward.
- Browser checks here are interaction/DOM verification, not screenshot-level visual QA.

## Retained limitations

- No secant-distance h control exists or was added.
- Existing solver issues reported by worker (not fixed here): precision/domain behaviour at tan singularities, and an abs worked-step math rendering issue. These are not established as fixed by the passing UX suite.
- Input/control region still occupies vertical space; no claim that results fit first viewport.
- Final bounded independent Standards and Spec reviews completed: Spec found no concrete blocker; Standards identified misleading fallback error feedback and discarded severity. Parent replaced the fallback with neutral wording and respected warning severity. Existing solver/rendering limitations remain out of scope.

## Other lesson audits

Worker-authored source-review reports, copied into the project for follow-up:

- `docs/report/2026-10-15-ux-audit-riemann-area-volume.md`
- `docs/report/2026-10-15-ux-audit-substitution-improper.md`

These reports flag candidate correctness hazards and structure issues. Their source findings require parent confirmation before widening implementation scope; they are not browser visual QA or proof of numerical defects from executed counterexamples.
