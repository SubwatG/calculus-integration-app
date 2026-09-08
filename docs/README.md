# สารบัญเอกสารโครงการ (Project Documentation Index)

เอกสารทั้งหมดของโครงการ **Calculus Learning Sandbox (เว็บแอปพลิเคชันช่วยเรียนรู้แคลคูลัสเชิงโต้ตอบ)** ถูกจัดระเบียบตามหมวดหมู่เพื่อความสะดวกในการเข้าถึงและอ้างอิง:

---

## 1. เอกสารการนำเสนอและสอบโครงร่าง (Proposal & Defense)
โฟลเดอร์: `docs/proposal/`

* **เล่มข้อเสนอโครงงานฉบับทางการ:**
  * [โครงร่างคณิตศาสตร์ประยุกต์.docx](proposal/โครงร่างคณิตศาสตร์ประยุกต์.docx) — เอกสาร Word ฉบับยื่นเสนอ
  * [โครงร่างคณิตศาสตร์ประยุกต์.pdf](proposal/โครงร่างคณิตศาสตร์ประยุกต์.pdf) — เอกสาร PDF ฉบับส่งตรวจ
  * [โครงร่างคณิตศาสตร์ประยุกต์-แก้ก่อนส่ง.pdf](proposal/โครงร่างคณิตศาสตร์ประยุกต์-แก้ก่อนส่ง.pdf) — ฉบับปรับปรุงจุดบกพร่องก่อนสอบ
  * [1.4-methodology-workplan.docx](proposal/1.4-methodology-workplan.docx) — รายละเอียดระเบียบวิธีวิจัยและแผนการดำเนินงาน
* **สื่อการนำเสนอและการเตรียมสอบ:**
  * [slide-deck.html](proposal/slide-deck.html) — สไลด์นำเสนอโครงร่าง 20 สไลด์ (HTML + KaTeX สไตล์วิชาการ คุมเวลา 15 นาที)
  * [proposal-defense-guide.html](proposal/proposal-defense-guide.html) — คู่มือแนวทางการตอบข้อซักค้านของคณะกรรมการ
  * [proposal-defense-critique-report.html](proposal/proposal-defense-critique-report.html) — รายงานวิเคราะห์จุดอ่อนและแนวทางปิดรอยรั่ว
  * [gemini-consultation-summary.md](proposal/gemini-consultation-summary.md) — บันทึกข้อสรุปแนวทางพัฒนาและกลยุทธ์การนำเสนอ

---

## 2. สถาปัตยกรรมระบบและพิมพ์เขียว (System Architecture)
โฟลเดอร์: `docs/architecture/`

* [system-architecture-master.html](architecture/system-architecture-master.html) — แผนผังสถาปัตยกรรมระบบแม่บท (Master Architecture)
* [project-system-blueprint.html](architecture/project-system-blueprint.html) — พิมพ์เขียวแสดงการไหลของข้อมูล (Data Flow & Component Interactions)

---

## 3. ต้นแบบจำลองและตัวสาธิต (Mockups & Interactive Prototypes)
โฟลเดอร์: `docs/mockup/`

* [master-interactive-demo.html](mockup/master-interactive-demo.html) — ระบบสาธิตต้นแบบ Standalone (HTML5 + Canvas 2D + KaTeX) ครอบคลุม 4 โมดูลหลัก
* [wireframe.html](mockup/wireframe.html) — โครงสร้างส่วนต่อประสานผู้ใช้ (UI Wireframe)
* [master-plan-review.md](mockup/master-plan-review.md) — แผนแม่บทการพัฒนาต้นแบบจำลอง

---

## 4. บันทึกการตรวจสอบความรัดกุมเชิงวิชาการ (Audits & Debates)
โฟลเดอร์: `docs/debate/`

* [hostile-audit-plan.html](debate/hostile-audit-plan.html) — แผนจำลองการซักค้านจากกรรมการสายวิชาการสุดเขี้ยว (Hostile Audit)
* [codex-audit-report.html](debate/codex-audit-report.html) — รายงานการตรวจสอบความถูกต้องทางคณิตศาสตร์โดย Codex CLI
* [debate-record.html](debate/debate-record.html) — บันทึกการอภิปรายและประเด็นโต้แย้งเชิงวิชาการ

---

## 5. คู่มือสำหรับนักศึกษาผู้พัฒนา (Student Developer Guides)
โฟลเดอร์: `docs/`

* [windows-student-setup.md](windows-student-setup.md) — คู่มือการติดตั้งและรันโปรเจกต์บนระบบปฏิบัติการ Windows (PowerShell + venv)
* [student-interactive-lesson-guide.md](student-interactive-lesson-guide.md) — ขั้นตอนการพัฒนาบทเรียน Interactive ตามโครงสร้าง 5 ชั้น
* [interactive-lessons-plan.md](interactive-lessons-plan.md) — แผนขอบเขตเนื้อหาบทเรียน 6 บทในอนาคต
* [markdown-latex-guide.qmd](markdown-latex-guide.qmd) — คู่มือการเขียนสมการคณิตศาสตร์ LaTeX และ Markdown ([ฉบับ PDF](markdown-latex-guide.pdf) / [ฉบับ HTML](markdown-latex-guide.html))
