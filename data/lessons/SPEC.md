# Lesson Data Spec — calculus-integration-app

> สถานะ: DRAFT v1 — รออาจารย์ approve ก่อนปล่อย omp (Plan A gate)
> อ้างอิง: data/lessons/ (61 ไฟล์) + /home/kitti/Downloads/Math-Silpakorn-free-books/ (PDF ต้นฉบับ)

## 1. เป้าหมาย

เปลี่ยน `data/lessons/` จาก OCR raw 61 ไฟล์ (ชื่อปนกัน 2 ระบบ, หัวข้อเลขซ้ำ,
ไฟล์ซ้ำ, บทนำว่าง) เป็นชุดบทเรียนที่มีโครงสร้างเดียวกัน ตรวจเทียบ PDF ได้
ใช้เป็นสื่อประกอบการสอน (นักเรียน + อาจารย์)

## 2. โครงสร้างโฟลเดอร์เป้าหมาย (หลัง transform — เสร็จสมบูรณ์ 2026-08-07)

```
data/lessons/
  cal2/                    # Calculus 2 (OCR จาก Silpakorn)
    00-overview.md         # Integration Overview (เขียนเอง)
    01-basic-rules.md      # Basic Integration Rules (เขียนเอง)
    ch01/ 00-intro, 01-antiderivative-indefinite, 02-exercises-12, 03-exercises-14
    ch02/ 00-intro, 01-integration-by-substitution, 02-integration-by-parts,
          03-partial-fractions, 04-integrals-with-quadratic, 05-exercises-24
    ch03/ 00-intro, 01-area-under-curve, 02-volume-of-solids, 03-arc-length
    ch04/ 00-intro, 01-improper-type1-discontinuous, 02-exercises-41,
          03-improper-type2-unbounded, 04-exercises-42
    ch05/ 00-intro, 01-rectangular-coordinates, 02-quadric-surfaces, 03-exercises-52
    ch06/ 00-intro, 01-functions-of-two-variables, 02-functions-of-many-variables,
          03-surface-integrals
    ch07/ 00-intro, 01-parametric-equations, 02-line-integrals,
          03-exercises-73, 04-exercises-75
    ch08/ 00-intro, 01-differential-equations, 02-exercises-85
    solutions/ 00-intro, 01-solutions-13, 02-solutions-32
  cal1/                    # Calculus 1 (transform เสร็จ 17 ไฟล์: ch01..ch05 + solutions)
    ch01..ch05 + solutions (17 ไฟล์)
  _archive/                # ไฟล์ซ้ำ/ชื่อผิด เก็บไว้ ไม่ลบ (4 ไฟล์)
```

## 3. Frontmatter (ทุกไฟล์ ทุกบท — implemented)

```yaml
---
title: "1.1 ปฏิยานุพันธ์และอินทิกรัลไม่จำกัดเขต"
course: cal2          # cal2 | cal1
chapter: 1
section: "1.1"
type: intro | content | exercises | solutions
source: "Calculus2-ch1-integrals.pdf"
status: transformed | verified   # transform เสร็จแล้ว, content QA = ขั้นต่อไป
---
```

## 4. กฎ Markdown (บังคับ)

1. **H1 เดียวต่อไฟล์** = ชื่อบทเรียน (ตอนนี้บางไฟล์ไม่มี H1, บางไฟล์ H1 เป็นชื่อไฟล์ภาษาอังกฤษหลุดมา)
2. **เลขหัวข้อห้ามซ้ำ**: `## 3.6 3.6 ...` → `## 3.6 ...` (เจอ 24 ไฟล์)
3. **หนึ่ง section ต่อไฟล์**: ห้ามปนหลายบท/หลายแบบฝึกหัดในไฟล์เดียว
   (ตอนนี้ `ch1-แบบฝึกหัด-12.md` มีทฤษฎี 1.3 ปน, `ch3-area-under-curve.md` มีแบบฝึกหัด 3.3 ปน)
4. Math: inline `$...$`, display `$$...$$` เท่านั้น — ห้าม `\(...\)`/`\[...\]`
5. **ตัดบรรทัดยาว**: paragraph ไม่เกิน ~500 ตัวอักษร/บรรทัด
   (ตอนนี้บางไฟล์ 1 paragraph = 1 บรรทัดยักษ์ → tool อ่านเป็น binary)
6. คำศัพท์คณิตศาสตร์: ไทยก่อน, อังกฤษวงเล็บ ณ การปรากฏครั้งแรก (ตาม convention vault)
7. **ห้ามแก้เนื้อหาคณิตศาสตร์/สมการ** ในขั้น transform — omp แตะโครงสร้างเท่านั้น

## 5. เส้นแบ่งงาน (Plan A)

| งาน | เจ้าของ | ตรวจโดย |
|---|---|---|
| transform โครงสร้าง (หัวข้อ, frontmatter, ตัดบรรทัด, แยกไฟล์) | omp | Hermes diff review |
| แก้ภาษาไทย/สมการที่เพี้ยน | Hermes + อาจารย์ | เทียบ PDF ต้นฉบับ |
| mapping ไฟล์ → PDF | Hermes (ทำแล้ว, MAPPING.md) | อาจารย์สุ่มตรวจ |
| auto-discovery lessons.py | Hermes | รันแอพจริง |
| approve ความถูกต้องรายบท | อาจารย์ | — |

## 6. Gate

- [ ] อาจารย์ approve spec นี้
- [ ] ต่อ: omp transform lot 1 (cal2 ch1–3) → Hermes diff → อาจารย์ approve
- [ ] ต่อ: Hermes content QA เทียบ PDF ch1–3 → อาจารย์ approve
- [ ] ต่อ: lot ถัดไป (ch4–8, cal1)
