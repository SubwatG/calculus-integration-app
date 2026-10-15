# Lesson progressive disclosure

## Current priority

ผู้ใช้ยุติการขยายการปรับ layout ไปบทอื่นแล้ว งานต่อไปคือปรับความละเอียดของเฉลย ส่งต่อชิชาตาม `docs/tasks/2026-10-15-task-chicha.md` โดยคงหน้าตาที่มีอยู่และส่ง PR เข้า main ไม่ merge เอง งานรีมันน์ที่อีกเซสชันทำค้างต้องประสานสิทธิ์ไฟล์ก่อนแก้

## Approved scope

ผู้ใช้อนุมัติให้สำรวจบทที่เหลือพร้อมกัน และปรับบทเส้นสัมผัสและอนุพันธ์เป็นบทนำร่องถัดจากหน้าลิมิต โดยยังไม่ปรับบทอื่นจนกว่าจะตรวจต้นแบบผ่าน ไม่ได้อนุมัติ commit, push หรือเปลี่ยนธีมส่วนกลาง

## Outcome

ผู้เรียนเริ่มทดลองได้เร็ว เห็นผลลัพธ์พร้อมคำอธิบายสั้นที่ถูกต้อง และเปิดอ่านเนื้อหาฉบับเต็มได้ รูปแบบร่วมเป็นหลักการจัดข้อมูล ไม่ใช่บังคับทุกบทให้มีกล่องเหมือนกัน

## Work allocation

- Tangent pilot: isolated candidate; own `pages/tangent.py` and new `tests/test_tangent_page_ux.py` only.
- Read-only audit: `pages/riemann.py`, `pages/area_between.py`, `pages/volume_revolution.py`.
- Read-only audit: `pages/substitution.py` (including u-sub/by-parts modes), `pages/improper_integrals.py`.
- Parent: inspect actual source, verify artifacts and integration hashes, run tests and browser checks, assemble audit recommendations.

## Tangent acceptance

- Preserve hero, theme, navigation, presets, parsed expression preview and existing state keys.
- Place experiment before long general theory; retain graph, exact slope/result and concise truthful feedback outside collapsed details.
- Preserve instructional content in clearly named collapsed sections for concept/theory/full worked steps.
- Keep differentiation/domain errors and nondifferentiability visible; zero derivative must not imply a turning point.
- Existing tangent page has no secant-distance control. Adding secant/h visualization is outside this layout pilot; do not invent or claim it.
- Tests cover supported polynomial/transcendental presets, input changes, invalid/domain inputs and nondifferentiability. Run full relevant suite on latest integrated files, then exercise browser.

## Concurrent-session safety

- Another Hermes session is editing shared files. Workers must not write live source or shared helpers.
- Record baseline source/dependency hashes and return a patch from isolated copy.
- Before live integration inspect diff and compare current target hashes; stop/rebase on target drift, never replace another session's newer version.
- Preserve latest shared theme/keypad/solver/theory. New shared changes require separate review, not implicit approval.
- Keep original source backup in active-profile scratch; no git staging, commits, pushes, or server restart.

## Completion evidence

Implementation approval is not proof of completion. Record exact tests, browser observations, retained limitations and any concurrency blockers before declaring the pilot usable. Audit reports distinguish source observations from visual findings. Later batch implementation remains unapproved until this pilot is reviewed.
