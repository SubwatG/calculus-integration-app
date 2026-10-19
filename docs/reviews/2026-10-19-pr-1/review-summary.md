# Calculus webapp: PR review checkpoint

สถานะ: กำลังตรวจและแก้ candidate ตามขอบเขตที่อนุมัติ ยังไม่พร้อม merge

## แหล่งจริงและขอบเขต

- Repository: https://github.com/SubwatG/calculus-integration-app
- PR #1: https://github.com/SubwatG/calculus-integration-app/pull/1
- Base: `d36dd7e19dc834a3e572431c9f551a80157c9e9e`
- Head: `fa6761c9e7ee53e55690b8bea5d56e30b04d835e`
- เปรียบเทียบ `git diff BASE...HEAD`; PR เปลี่ยน 31 ไฟล์ มี 11 commits ที่ยังไม่อยู่ใน main
- อาจารย์อนุมัติให้เก็บ UI ใหม่และปรับตามมาตรฐานแล้ว ดู scope-decision.md; ข้อห้าม redesign ในโจทย์เดิมไม่เป็น blocker ปัจจุบัน

## Branch inventory ที่ตรวจจาก remote

มี remote branches จริง 9 branches ไม่นับ symbolic origin/HEAD:

- main ตรงกับ local HEAD
- feat/worked-solutions-detail: ahead 11, behind 0 มี PR #1
- quiz-conceptual-bank: ahead 5, behind 46 ไม่มี PR เปิดในรายการที่ตรวจ ทั้ง 5 commits ไม่ถูก git cherry ระบุเป็น patch-equivalent กับ main แต่ยังไม่ได้ตรวจ semantic equivalence จึงไม่ควรนำ branch เก่ามารวมทั้งชุด
- อีก 6 branches ไม่มี commits ที่ main ยังเข้าไม่ถึง ไม่ได้ลบ branch ใด

หลักฐาน: branch-status.json, quiz-branch-cherry.txt และ pr-metadata.json

## การทดสอบที่ parent รันเอง

ใช้ project .venv เดิม ล้าง PYTHONPATH และไม่สร้าง pytest cache ใน snapshot:

- Python 3.12.14 / Streamlit 1.63.0 / SymPy 1.14.0 / pytest 9.1.1
- Base main: 218 passed, exit 0
- Pinned PR: 235 passed, 1 failed, exit 1
- Failure: tests/test_substitution_solver.py:126 ใช้ AppTest.from_file("pages/substitution.py") ซึ่ง resolve เป็น tests/pages/substitution.py บน runtime ปัจจุบัน ปัญหานี้เป็น test harness/path failure ไม่ใช่หลักฐานว่าคณิตศาสตร์ผิด
- ตัว runner ที่เก็บ log อาจจบด้วย exit 0 เพื่อเขียนรายงาน แต่ผล pytest จริงเป็น exit 1 ตาม pr-pytest.log/test-result.json จึงยังไม่ถือว่า PR ผ่าน

## การแยกงานและผลกระทบ

- พื้นที่ source review แบบ pinned: ดู snapshot.json
- Candidate สำหรับซ่อม: ดู candidate.json
- ไม่แก้ไฟล์ใน pinned snapshot เพื่อให้ผลรีวิวอ้าง head เดิมได้
- Native bot-worker-flash กำลังซ่อมเฉพาะ AppTest path ใน candidate พร้อม RED/GREEN logs และ independent check
- Standards/Spec review สั่งแยกกันบน Flash ผลที่อิงข้อห้าม redesign เดิมต้องอ่านร่วมกับ scope-decision.md
- รอผลรีวิวก่อนเลือก minimal correctness/UI compliance repairs ต่อไป ไม่มีการอนุมัติให้ย้อน UI ใหม่ทั้งชุด

## งานในเครื่องที่ต้องรักษา

มี 3 tracked modified files และ 1 untracked test ของ Riemann ก่อนเริ่มตรวจ: pages/riemann.py, utils/riemann_solver.py, tests/test_riemann_solver.py, tests/test_riemann_page_ux.py

parent ตรวจ SHA-256 หลังรัน baseline tests แล้วตรงกับก่อนเริ่มทั้งหมด ไม่ stash/reset/overwrite งานนั้น PR เองแก้ utils/riemann_solver.py ด้วยแม้ PR body บอกว่าไม่ได้แตะ จึงต้องตัดสินการรวมจาก diff จริง ไม่อิงคำอธิบายอย่างเดียว

## เกตที่ยังไม่ผ่าน/ยังไม่ตรวจ

- Candidate focused test และ full regression suite หลังซ่อม
- ยืนยันข้อค้นพบทางคณิตศาสตร์/สัญญา API ด้วย parent probes
- UI standards ตามขอบเขตใหม่ และ actual browser interaction ของ candidate
- ตรวจ conflict/compatibility กับงาน Riemann ในเครื่องโดยไม่ทับงานเดิม
- Parent synthesis หลัง Standards/Spec review
- คำอนุมัติ commit/push/merge และการรับรอง deployed version

ยังไม่มีการแก้ remote PR, comment/review บน GitHub, commit, push, merge หรือ restart บริการเดิม
