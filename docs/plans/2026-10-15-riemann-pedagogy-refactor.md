# แผนการยกระดับมโนทัศน์และการเฉลยผลรวมรีมันน์ (Riemann Sum Pedagogy Refactor)

**วันที่:** 15 ตุลาคม 2026  
**สถานะ:** อนุมัติแล้ว (Approved) พร้อมดำเนินการตาม Matt Pocock Flow  
**เป้าหมาย:** ยกระดับหน้า `pages/riemann.py` และ `utils/riemann_solver.py` จากเครื่องคำนวณตัวเลขพื้นฐาน สู่บทเรียนมโนทัศน์เชิงโต้ตอบ (Conceptual & Visual Sandbox) ที่ลึกซึ้ง ครบถ้วน และสอดคล้องกับมาตรฐานมหาวิทยาลัย

---

## 1. ปัญหาและจุดบกพร่องเดิม (Current Deficiencies)

1. **การเฉลยกระโดดข้ามขั้น (Black-Box Arithmetic):** แสดงแค่สัญลักษณ์ $f(x_0) + \dots + f(x_{n-1})$ แล้วกระโดดไปที่คำตอบทันที ไม่แจกแจงความสูงแต่ละแท่งและผลรวมความสูง $\sum f(x_i^*)$
2. **ขาดการวิเคราะห์ความคลาดเคลื่อน (Missing Error & Convergence Analysis):** ไม่มีการเปรียบเทียบระหว่างค่าประมาณกับค่าจริง $\int_a^b f(x)\,dx$ ทำให้ผู้เรียนไม่เห็นความเร็วในการลู่เข้า
3. **ขาดมโนทัศน์เปรียบเทียบ 3 วิธีพร้อมกัน (L_n vs M_n vs R_n):** ผู้เรียนต้องสลับตัวเลือก 3 รอบ ทำให้ไม่เห็นภาพว่าทำไม Midpoint ถึงมีความคลาดเคลื่อนต่ำกว่า Left/Right อย่างมหาศาล
4. **ความคลุมเครือระหว่าง Net Signed Area กับ Geometric Area:** เมื่องานมีช่วงที่ $f(x) < 0$ (เช่น $x^3 - 2x$) ผลรวมติดลบ แต่หน้าเว็บไม่มีคำอธิบายแยกแยะว่าคือพื้นที่คิดเครื่องหมาย
5. **ขาดการเชื่อมโยงสู่ลิมิต $n \to \infty$:** ขาดการแสดงสูตรซิกม่าในรูปปิดและการเทคลิมิตสู่ปริพันธ์จำกัดเขตสำหรับโจทย์พหุนาม

---

## 2. พิมพ์เขียวทางเทคนิค (Technical Specification)

### 2.1 ส่วน `utils/riemann_solver.py`
เพิ่มฟังก์ชันและโครงสร้างข้อมูลผลลัพธ์:
- `compute_riemann(...)` ขยาย return dict:
  - `exact_integral`: float | None (ค่าจริงจาก `sp.integrate`)
  - `exact_latex`: str (LaTeX แสดงการอินทิเกรตและค่าจริง)
  - `error_abs`: float | None
  - `error_signed`: float | None ($R - \text{exact}$)
  - `error_pct`: float | None
  - `direction`: `"underestimate" | "overestimate" | "exact" | "unknown"` (วิเคราะห์จากความชัน/ทิศทางฟังก์ชัน)
  - `methods_comparison`: dict สรุปค่าของทั้ง 3 วิธี (`left`, `right`, `midpoint`) พร้อม error
  - `has_negative_region`: bool (ตรวจว่ามีค่า $f(x) < 0$ บนช่วงหรือไม่)
  - `negative_warning`: str | None (คำเตือนอธิบาย Net Signed Area)
  - `table_data`: รายการแจกแจงค่า $i, x_i^*, f(x_i^*), f(x_i^*)\Delta x$ สำหรับแสดงในตารางหรือขั้นตอนละเอียด
  - `sum_heights`: float ($\sum f(x_i^*)$)
  - `analytical_limit`: dict | None (สูตรปิดในรูป $n$ และการเทคลิมิต $n \to \infty$ สำหรับพหุนาม)

### 2.2 ส่วน `pages/riemann.py`
ปรับปรุง UI และโครงสร้างการนำเสนอตามหลัก Progressive Disclosure:
1. **Multi-Method Comparison Dashboard:** การ์ด 3 คอลัมน์ ($L_n, M_n, R_n$) เทียบกับค่าจริง $\int_a^b f(x)\,dx$ พร้อมแสดง \% Error ทันที
2. **Net Signed Area Alert:** แสดงกล่องอธิบายชัดเจนเมื่อฟังก์ชันมีค่าติดลบในบางช่วง
3. **Step-by-Step Breakdown:** แจกแจงความสูงแต่ละแท่ง ผลรวมความสูง และการคูณด้วย $\Delta x$
4. **Data Table Expander:** ตารางค่าพิกัดความสูงและพื้นที่ของแต่ละแท่ง ($n \le 50$)
5. **Analytical Limit Expander:** แสดงการพิสูจน์ $\lim_{n \to \infty} R_n$ สำหรับโจทย์พหุนาม

### 2.3 การทดสอบ (TDD via `tests/test_riemann_solver.py`)
- เขียนเทสต์ครอบคลุม:
  - `exact_integral` และ `error_signed` / `error_pct`
  - `methods_comparison` (ครบทั้ง 3 วิธีในครั้งเดียว)
  - `has_negative_region` สำหรับฟังก์ชัน $x^3 - 2x$ บน $[0, 2]$
  - `direction` สำหรับฟังก์ชันเพิ่มและลด
  - `analytical_limit` สำหรับ $x^2$ และ $x^3$
  - Backward compatibility ของ fields เดิม (`ok, result, latex, steps, expr, error, variable`)

---

## 3. ขั้นตอนการดำเนินการ (Action Plan)

- [x] Phase 1: ออกแบบ Spec และ Plan
- [ ] Phase 2: เขียน Unit Tests ใหม่ใน `tests/test_riemann_solver.py` (TDD Red)
- [ ] Phase 3: อัปเดต Logic ใน `utils/riemann_solver.py` (TDD Green)
- [ ] Phase 4: อัปเดตหน้า UI ใน `pages/riemann.py` และคุมความเรียบร้อยตาม `AGENTS.md`
- [ ] Phase 5: รัน Full Pytest Suite และทดสอบ Visual UX ผ่าน `browser-box`
