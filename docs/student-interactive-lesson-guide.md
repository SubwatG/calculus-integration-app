# Step-by-Step Guide: สร้างบทเรียน Interactive สำหรับนักศึกษา project

คู่มือนี้สำหรับนักศึกษาที่ได้รับมอบหมายให้สร้างบทเรียน interactive ใน
`calculus-integration-app` ให้ทำตามขั้นตอนเรียงลำดับ บทเรียนที่ทำเสร็จแล้ว
คือ `pages/riemann.py` (Riemann Sum) ใช้เป็นตัวอย่างอ้างอิงได้ตลอด

## ภาพรวม: บทเรียน interactive 1 บทประกอบด้วย 5 ส่วน

```text
utils/theory.py          -> เนื้อหาทฤษฎี (dict)
utils/<topic>_solver.py  -> logic การคำนวณ (คืน dict พร้อมขั้นตอน LaTeX)
utils/plotter.py         -> ฟังก์ชันวาดกราฟ (matplotlib)
pages/<topic>.py         -> หน้า Streamlit (UI)
tests/test_<topic>.py    -> test ตรวจ logic
```

หลักการสำคัญ: แยก logic ออกจาก UI เสมอ logic อยู่ utils/ หน้าเว็บแค่เรียกใช้

---

## ขั้นที่ 1: อ่าน blueprint จากบทเรียนที่ทำเสร็จแล้ว

เปิดไฟล์เหล่านี้ก่อนเริ่ม:

- `pages/riemann.py` — โครงสร้างหน้าเว็บครบ (hero, theory panel, widget, ปุ่มคำนวณ, ผลลัพธ์, กราฟ, ขั้นตอน)
- `utils/riemann_solver.py` — รูปแบบ solver ที่คืน dict {ok, result, latex, steps, expr, error}
- `utils/theory.py` — รูปแบบ dict เนื้อหาทฤษฎี
- `utils/plotter.py` — รูปแบบฟังก์ชันวาดกราฟ (ฟังก์ชัน plot_riemann ที่ทำเสร็จแล้ว)

แผนงานทั้งหมดอยู่ใน `docs/interactive-lessons-plan.md` อ่านก่อนเริ่มงานด้วย

---

## ขั้นที่ 2: เติมเนื้อหาทฤษฎีใน utils/theory.py

เปิด `utils/theory.py` หา key ของหัวข้อที่ได้รับมอบหมาย (เช่น `"tangent"`)
เติมจุดที่เป็น TODO ให้ครบทุก field:

```python
"tangent": {
    "title": "เส้นสัมผัสและอนุพันธ์ (Tangent Line and Derivative)",
    "conditions": [...],   # เงื่อนไขการใช้งาน
    "formulas": [...],     # สูตรที่ใช้
    "properties": [...],   # สมบัติ
    "cautions": [...],     # ข้อควรระวัง
    "applications": [...], # การประยุกต์
    "decision_guide": "...", # คำแนะนำการเลือกใช้
}
```

กฎ: ใช้ `$...$` สำหรับสมการ inline และ `$$...$$` สำหรับ display
ภาษาไทยก่อน แล้ววงเล็บภาษาอังกฤษครั้งแรก

---

## ขั้นที่ 3: implement solver ใน utils/<topic>_solver.py

เปิดไฟล์ solver stub ของหัวข้อตัวเอง (เช่น `utils/tangent_solver.py`)
หา TODO แล้วเขียน logic จริง แทนที่บรรทัด `raise NotImplementedError`

รูปแบบที่ต้องคืน (เหมือน riemann_solver):

```python
{
    "ok": True,
    "result": 4.0,              # ค่าผลลัพธ์ตัวเลข
    "latex": r"f'(2) = 4",      # สูตร LaTeX สำหรับแสดงผลลัพธ์
    "steps": [                  # ขั้นตอน LaTeX ทีละขั้น
        r"\Delta x = \frac{2-0}{8} = 0.25",
        r"L_n \approx 2.187500",
    ],
    "expr": expr,               # sympy expression ที่ parse แล้ว
    "error": None,
}
```

ถ้า input ผิด ให้คืน ok=False พร้อม error (ดูตัวอย่างใน riemann_solver)

---

## ขั้นที่ 4: เขียนฟังก์ชันวาดกราฟใน utils/plotter.py

หาฟังก์ชัน stub ของหัวข้อตัวเอง (เช่น `plot_tangent`) แล้วเขียนกราฟจริง
อ้างอิงจาก `plot_riemann` ที่ทำเสร็จแล้ว

ข้อควรจำ:

- ฟังก์ชันคืน `(fig, ax)` สำหรับ `st.pyplot(fig)`
- **label ในกราฟต้องเป็นภาษาอังกฤษเท่านั้น** (matplotlib ไม่มีฟอนต์ไทย)
- ใช้สีจาก palette เดิม (เขียว KU ฯลฯ) ไม่ต้องเปลี่ยน
- ทดสอบด้วยการ savefig ก่อนเอาไปใช้ในหน้า

---

## ขั้นที่ 5: เปิดใช้งานกราฟและ widget ใน pages/<topic>.py

หน้า stub มี TODO อยู่ 2 จุด:

1. TODO ในส่วน widget: เพิ่ม slider/selectbox/number_input ที่จำเป็น
   ดูตัวอย่างจาก `pages/riemann.py` (มี slider n, number_input a/b, selectbox method)

2. TODO ในส่วนแสดงผล (บรรทัดที่เขียนว่า):
   ```python
   # TODO: เรียก plot_xxx(res["expr"], ...) แล้ว st.pyplot(fig)
   ```
   เปลี่ยนเป็น:
   ```python
   fig, _ = plot_xxx(res["expr"], ...)
   st.pyplot(fig)
   ```

---

## ขั้นที่ 6: ทำ test ให้ผ่าน

เปิดไฟล์ test ของหัวข้อตัวเองใน `tests/test_<topic>.py`
ตอนนี้ test จะ fail เพราะ solver ยังไม่ implement

รัน test เพื่อดูสถานะ:

```bash
cd /home/kitti/Documents/GitHub/calculus-integration-app
source .venv/bin/activate
pytest tests/test_<topic>.py -v
```

แก้ solver จน test ผ่าน จากนั้นรัน test ทั้งหมด:

```bash
pytest tests/ -v
```

---

## ขั้นที่ 7: รันแอปและตรวจผลจริง

```bash
streamlit run app.py
```

เปิด `http://localhost:8501` แล้ว:

1. ไปหน้าที่ตัวเองสร้างจากเมนู sidebar
2. กดปุ่มคำนวณ ดูว่าผลลัพธ์และขั้นตอนถูกต้อง
3. ตรวจกราฟว่าแสดงถูกต้อง ไม่มีตัวอักษรเพี้ยน
4. ลองเปลี่ยนค่าต่างๆ (slider, a, b) แล้วดูว่ากราฟเปลี่ยนตาม

---

## ขั้นที่ 8: ตรวจตาม definition of done แล้วส่งงาน

ตรวจสอบ checklist ใน `docs/interactive-lessons-plan.md`:

- [ ] theory.py มี key ครบทุก field
- [ ] solver คืน dict ครบ {ok, result, latex, steps, expr, error}
- [ ] กราฟวาดได้ ไม่มี label ไทย
- [ ] หน้าใน pages/ ใช้ render_hero + theory panel + widget + solver + plotter
- [ ] ลงทะเบียนหน้าใน app.py (ถ้ายังไม่ได้ทำ)
- [ ] pytest tests/ -v ผ่านทั้งหมด
- [ ] รันแอปจริง ตรวจกราฟและขั้นตอน
- [ ] commit เป็น branch ของตัวเอง แล้ว push

---

## ข้อผิดพลาดที่พบบ่อย (อ่านก่อนส่ง)

1. **ลืมคูณค่า/ขั้นตอนไม่ครบ** — ตรวจกับค่าที่คำนวณมือใน test
2. **label ไทยในกราฟ** — matplotlib จะเตือน Glyph missing ต้องเป็นภาษาอังกฤษ
3. **ใช้ตัวแปรที่ไม่ได้ประกาศ** — เช่น เรียก a_val แต่ไม่มี slider a (ดู blueprint riemann)
4. **ลืมคืน expr ใน dict** — หน้าใช้ res["expr"] วาดกราฟ
5. **ทดสอบเฉพาะหน้าไม่ทดสอบ logic** — ต้องมี test ใน tests/ ด้วย
