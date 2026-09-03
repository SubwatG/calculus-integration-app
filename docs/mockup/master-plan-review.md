# แผนแม่บทการพัฒนาต้นแบบจำลอง (Mockup Plan) สำหรับระบบแคลคูลัสแบบมีปฏิสัมพันธ์
**โครงการ:** Calculus Integration Interactive Learning Sandbox (Bespoke Pedagogical Engine)  
**เป้าหมาย:** สร้าง Mockup ฉบับสมบูรณ์ (Standalone HTML + KaTeX + Canvas 2D + Live Interactive Logic) เพื่อใช้เป็น "เฉลยต้นแบบสำหรับอาจารย์" ในการตรวจสอบมาตรฐานของนิสิต และใช้เป็น Deck สาธิตในการสอบ Proposal Defense ปิดช่องโหว่ทางคณิตศาสตร์และระเบียบวิธีวิจัย 100%

---

## 1. โครงสร้างและสถาปัตยกรรมของ Mockup (`docs/mockup/master-interactive-demo.html`)

ออกแบบในรูปแบบ Interactive Academic Application รองรับ KaTeX เรนเดอร์สมการคณิตศาสตร์ คุมโทนสี Dark Slate / Academic Cyan / Emerald / Crimson ให้ความรู้สึกจริงจังทางวิชาการและเป็นระบบ พร้อม Tab สลับ 4 โมดูลหลัก:

### โมดูลที่ 1: Riemann Convergence & Partitioning Sandbox (แก้โจทย์ช่องโหว่ 1.1)
- **Interactive UI:**
  - ตัวเลือกฟังก์ชัน $f(x)$ แบบ Parameterized ($x^2$, $x^3 - 2x$, $\sin(x) + 1.5$, $\frac{1}{x+1}$)
  - ช่องกรอกช่วง $[a, b]$ และแถบสไลเดอร์ $n$ (ตั้งแต่ 2 ถึง 100)
  - Interactive Canvas 2D แสดงเส้นโค้ง $f(x)$ และแท่งสี่เหลี่ยมแนบกราฟ (Left, Right, Midpoint)
- **Rigorous Mathematical Features:**
  - ตารางเปรียบเทียบสด: $I_{\text{exact}}$ vs $L_n, R_n, M_n$
  - ตารางและกราฟคู่ขนาน Log-Log Error Plot ($\log(n)$ vs $\log(\text{Error})$) แสดงความชันเชิงประจักษ์ ยืนยัน $O(1/n)$ เทียบกับ $O(1/n^2)$
  - ข้อความแสดงสมมติฐานความเรียบของฟังก์ชัน (Smoothness & Bounded Second Derivative condition)

### โมดูลที่ 2: 3-State $u$-Substitution Scaffolding Engine (แก้โจทย์ช่องโหว่ 1.2)
- **Pedagogical 3-Tier Classification:**
  - ตัวอย่างโจทย์: $\int 2x\sqrt{x^2+1}\,dx$
  - ตัวเลือกการแทนค่าตัวแปร:
    1. $u = x \implies$ จำแนกเป็น `[Valid but Inefficient]` $\to$ แปลงรูปเป็น $\int 2u\sqrt{u^2+1}\,du$ (อธิบายว่าแทนค่าถูกต้องตามกฎคณิตศาสตร์ แต่ไม่ได้ช่วยให้อินทิเกรตง่ายขึ้น)
    2. $u = 2x \implies$ จำแนกเป็น `[Valid but Inefficient]` $\to$ แปลงรูปเป็น $\int \frac{u}{2}\sqrt{\frac{u^2}{4}+1}\,du$
    3. $u = x^2+1 \implies$ จำแนกเป็น `[Preferred Substitution]` $\to$ คำนวณ $du = 2x\,dx$ ยุบเหลือ $\int \sqrt{u}\,du = \frac{2}{3}u^{3/2} + C$
    4. $u = \sin(x) \implies$ จำแนกเป็น `[Invalid Substitution]` $\to$ ชี้แจงว่าไม่มีความเชื่อมโยงกับ integrand
  - **Scaffolding Fading Mode:** มีปุ่มจำลองการถอดตัวช่วย (Level 1: Choice Selection $\to$ Level 2: Fill $u$ & Auto-check $du$ $\to$ Level 3: Transfer Problem)

### โมดูลที่ 3: Improper Integral Singularity & Domain Guard (แก้โจทย์ช่องโหว่ 1.3)
- **Domain Discontinuity Detection:**
  - โจทย์ตัวอย่าง: $\int_{-1}^{1} \frac{1}{x^2}\,dx$ และ $\int_{1}^{\infty} \frac{1}{x^p}\,dx$
  - ระบบตรวจสอบและแจ้งเตือน: ตรวจพบจุด Singularities ที่ $x = 0 \in [-1, 1]$ $\to$ สั่งแยกเป็น 2 ช่วง $\lim_{t \to 0^-} \int_{-1}^t + \lim_{t \to 0^+} \int_t^1$
  - แสดงบทพิสูจน์การลู่ออก ($+\infty$) เพื่อป้องกัน Misconception ของการแทนค่าตรง ๆ ที่ได้ $-2$

### โมดูลที่ 4: Methodology & Feasibility Defense Blueprint (แก้โจทย์ช่องโหว่ 2 & 4)
- สรุปกรอบระเบียบวิธีวิจัยฉบับแก้ไข:
  - วางตำแหน่งงานเป็น **"Usability & Feasibility Pilot Study"** กับนิสิต 15–20 คน
  - ผังการวัดผล: ความเข้าใจมโนทัศน์ (Parallel Pre/Post Conceptual Diagnostics) + System Usability Scale (SUS 10 ข้อ) + Qualitative Think-aloud Observations
  - การแยกชั้นหลักฐาน 3 ระดับ: Math Rigor $\to$ Software Verification (Pytest Metamorphic & Invariant Tests) $\to$ Usability Evidence

---

## 2. ขั้นตอนการส่งตรวจความรัดกุมกับ Codex CLI ก่อนดำเนินการ
1. ส่งแผน Master Plan นี้ให้ `codex exec` ตรวจสอบความถูกต้องของสัญลักษณ์ทางคณิตศาสตร์ นิยาม $u$-sub และกรอบการวัดผล
2. นำข้อคิดเห็นของ Codex มาปรับแต่งโค้ด HTML/JS ให้สมบูรณ์แบบ
3. สร้างไฟล์ Mockup HTML ที่สมบูรณ์พร้อมทดสอบการทำงาน 100%
