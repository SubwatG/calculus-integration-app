# Parent adjudication of PR #1 reviews

## Current acceptance boundary

Read scope-decision.md first. The user approved KEEPING the new student-designed UI/theme/effects. Older reports recommending wholesale UI/theme reversion are preserved as historical review evidence, not current implementation instructions.

No source from the original working tree has been overwritten. The candidate and pinned review snapshot remain separate.

## Standards axis

| Finding | Parent disposition |
|---|---|
| Riemann PR-body inconsistency and ownership overlap | Confirmed inconsistency; integration gate, not evidence of actual data loss. A read-only three-way preview using local/base/PR versions reports one conflict region. Do not blindly revert the PR or overwrite the local solver. See riemann-reconciliation.json. |
| Emoji/em dash/Unicode-arrow UI strings | Confirmed candidate source literals. Fix only UI strings/icons, retaining layout/CSS/fonts/effects, mathematical notation, keys and behavior. Separate UI workers own disjoint files. |
| Global redesign/creators page as scope creep | Superseded by the user's explicit latest approval. Keep the new UI; do not remove the theme or creators page merely to satisfy the old brief. |
| AppTest relative path failure | Parent reproduced on pinned PR; Flash repaired only the test path in candidate. Dispatcher independent focused check passed. Preserve assertions; full final suite still required after all edits. |
| Repeated latex wrappers/private imports/raw dict result schemas | Optional architecture observations, not current blockers. Do not widen this repair into abstraction/schema refactors; the approved task requires public API compatibility. |

## Spec axis

- Scope prohibition against redesign is superseded; text-format, math, API/status and testing requirements remain.
- Riemann untouched claim is contradicted by the diff. Local Riemann work must remain preserved, and any later integration requires explicit conflict resolution and tests.
- The review's MET claims for substitution/improper/volume are bounded source judgments, not independent mathematical certification. Main and pinned-PR pytest results are parent-executed; the remaining algebra/domain checks are tracked separately.
- The review cites source line numbers above 3000 for files that are actually 403 lines (substitution), 513 (improper), and 200 (volume). These are not valid source-file citations and appear to refer to diff positions. Do not reuse those numbers as verified source evidence.
- Limits/tangents/area were explicitly not reviewed by the Spec worker. A bounded native Sol mathematical review was dispatched for these paths. Its report and probes require parent verification before acceptance.

## Lint and source identity

Parent ran actual installed commands:

- s1 doctor docs/reviews/2026-10-19-pr-1/review-standards.md
- s1 doctor docs/reviews/2026-10-19-pr-1/review-spec.md

Both returned CLEAN with zero violations. This is Markdown syntax/structure evidence, not math correctness. The worker's mention of s1-doctor --lint is not relied upon.

Native Flash repair session: 20261019_135231_287a0f. The inspected candidate diff adds a local pathlib import and an absolute page_path from __file__, retaining rendering and By Parts assertions. Independent focused test exit code: 0. The recorded RED is a test-harness path failure, not a solver-value regression.

Current source changes remain isolated, with no commit, push, merge, PR comment or service restart authorized/applied.
