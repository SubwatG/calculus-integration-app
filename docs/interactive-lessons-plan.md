# Interactive Lessons Plan — calculus-integration-app

แผนโครงบทเรียน interactive สำหรับนักศึกษา project
อ้างอิงเนื้อหาจาก `data/lessons/` (ไฟล์ Markdown ที่ transform แล้ว)

## หลักการ

- บทเรียน interactive 1 บท = theory dict + solver module + plotter function + page + test
- โครงสร้างอ้างอิงบทเรียนที่ทำเสร็จแล้ว: `pages/riemann.py` (Riemann Sum)
- นักศึกษาเติมเนื้อหาใน stub ให้ test ผ่าน และตรวจตาม AGENTS.md

## ตารางหัวข้อ

| # | key | ชื่อบทเรียน | แหล่งเนื้อหา | ทฤษฎีหลัก | solver ต้องทำอะไร | กราฟต้องแสดงอะไร | ความยาก |
|---|---|---|---|---|---|---|---|
| 1 | `tangent` | เส้นสัมผัสและอนุพันธ์ | cal1/ch02/01-geometric-problems.md | $f'(a)=\lim_{h\to 0}\frac{f(a+h)-f(a)}{h}$ | คำนวณความชันเส้นสัมผัสที่จุด a + สมการเส้นสัมผัส | เส้นโค้ง + เส้นสัมผัสหมุนตามจุด a (slider) | ปานกลาง |
| 2 | `limit` | ลิมิตเข้าใกล้จุด | cal1/ch04/01-indeterminate-forms.md | $\lim_{x\to a} f(x)$ ฟังก์ชันรูปแบบไม่กำหนด | คำนวณลิมิต + แสดงการแทนค่าใกล้จุดทีละขั้น | เส้นโค้ง + จุดวิ่งเข้าใกล้ a (slider) | ง่าย-ปานกลาง |
| 3 | `substitution` | การอินทิเกรตโดยการแทน | cal2/ch02/01-integration-by-substitution.md | $\int u^n\frac{du}{dx}dx = \frac{u^{n+1}}{n+1}+C$ | ตั้ง u, หา du, อินทิเกรต, แทนกลับ ทีละขั้น | ไม่มีกราฟจำเป็น หรือวาด f และ F | ปานกลาง-ยาก |
| 4 | `volume` | ปริมาตรของทรงตัน | cal2/ch03/02-volume-of-solids.md | $V = \int_a^b A(x)\,dx$ (slicing/disk/washer) | คำนวณปริมาตรแบบ disk/washer | ภาพตัดขวาง + รูปทรง (matplotlib) | ยาก |
| 5 | `area_between` | พื้นที่ระหว่างเส้นโค้ง 2 เส้น | cal2/ch03/01-area-under-curve.md | $A = \int_a^b (f(x)-g(x))\,dx$ | หาจุดตัด + คำนวณพื้นที่ระหว่างเส้นโค้ง | เส้นโค้ง 2 เส้น + แรเงาช่องว่าง (slider) | ปานกลาง |
| 6 | `improper` | อินทิกรัลไม่แท้ | cal2/ch04/01-improper-type1-discontinuous.md | $\int_a^b f(x)dx = \lim_{t\to b^-}\int_a^t f(x)dx$ | ตรวจลู่เข้า/ลู่ออก + คำนวณลิมิต | เส้นโค้ง + ขอบเขตวิ่งเข้าหาจุดไม่ต่อเนื่อง | ยาก |

## ลำดับแนะนำสำหรับนักศึกษา

1. `limit` — ง่ายสุด เห็นกราฟชัด ใช้ pattern ของ riemann ได้เลย
2. `tangent` — เพิ่มแนวคิดเส้นสัมผัส เหมาะเป็นบทที่ 2
3. `area_between` — ต่อยอดจาก riemann โดยตรง (แรเงาระหว่างเส้นโค้ง)
4. `substitution` — เน้น solver ทีละขั้น (ไม่ต้องกราฟ)
5. `volume` — กราฟซับซ้อนขึ้น (ตัดขวาง/ทรงตัน)
6. `improper` — ต้องเข้าใจลิมิต + อินทิกรัลไม่แท้พร้อมกัน

## Definition of done (ต่อบท)

- [ ] `utils/theory.py` มี key ครบ (conditions, formulas, properties, cautions, applications, decision_guide)
- [ ] solver module คืน dict {ok, result, latex, steps, expr, error}
- [ ] ฟังก์ชัน plotter วาดกราฟได้ ไม่มี label ไทย (matplotlib)
- [ ] หน้าใน `pages/` ใช้ render_hero + theory panel + widget + solver + plotter
- [ ] ลงทะเบียนหน้าใน `app.py`
- [ ] test ใน `tests/` ผ่าน (pytest tests/ -v)
- [ ] รันแอปจริง ตรวจกราฟและขั้นตอน
