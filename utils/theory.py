"""
modules/theory.py — เนื้อหาทฤษฎีบทเรียน interactive แคลคูลัส

ภาษาไทยทั้งหมด ใช้ LaTeX ($...$) สำหรับสัญลักษณ์ทางคณิตศาสตร์

โครงสร้างข้อมูลเหมือน stat-distribution-solver/modules/theory.py:
แต่ละบทเรียนมี dict ที่ประกอบด้วย conditions, formulas, properties,
cautions, applications และ decision_guide

บทเรียนแรก: 3.1 พื้นที่ภายใต้เส้นโค้ง (Riemann Sum)
"""

# ---------------------------------------------------------------------------
# THEORY_CONTENT — ข้อมูลทฤษฎีสำหรับแต่ละบทเรียน interactive
# ---------------------------------------------------------------------------
THEORY_CONTENT = {
    "riemann_sum": {
        "title": "พื้นที่ภายใต้เส้นโค้ง (Area under a curve)",
        "conditions": [
            "ฟังก์ชัน $f(x)$ ต่อเนื่องบนช่วงปิด $[a, b]$",
            "ในบทนิยามแรกกำหนดให้ $f(x) \\ge 0$ บน $[a,b]$ (กราฟอยู่เหนือแกน x)",
            "ถ้ากราฟอยู่ใต้แกน x บางช่วง ให้แยกช่วงและใช้ $\\int (-f(x))\\,dx$",
        ],
        "formulas": [
            "พื้นที่ภายใต้เส้นโค้ง: $A = \\int_a^b f(x)\\,dx$",
            "ผลรวมรีมันน์ซ้าย (left): $L_n = \\sum_{i=0}^{n-1} f(x_i)\\,\\Delta x$ เมื่อ $x_i = a + i\\,\\Delta x$",
            "ผลรวมรีมันน์ขวา (right): $R_n = \\sum_{i=1}^{n} f(x_i)\\,\\Delta x$",
            "ผลรวมรีมันน์จุดกึ่งกลาง (midpoint): $M_n = \\sum_{i=0}^{n-1} f(\\bar{x}_i)\\,\\Delta x$ เมื่อ $\\bar{x}_i = a + (i+\\tfrac12)\\Delta x$",
            "ความกว้าง: $\\Delta x = \\frac{b-a}{n}$",
        ],
        "properties": [
            "เมื่อ $n \\to \\infty$ ค่าประมาณ $L_n, R_n, M_n$ ลู่เข้าสู่ $\\int_a^b f(x)\\,dx$",
            "ถ้า $f$ เพิ่มขึ้น (increasing) แล้ว $L_n \\le A \\le R_n$",
            "ถ้า $f$ ลดลง (decreasing) แล้ว $R_n \\le A \\le L_n$",
            "midpoint มักให้ค่าประมาณแม่นยำกว่า left/right ที่ $n$ เท่ากัน",
        ],
        "cautions": [
            "อย่าลืมคูณ $\\Delta x$ ทุกพจน์ในผลรวม",
            "$L_n$ ใช้ $x_0$ ถึง $x_{n-1}$, ส่วน $R_n$ ใช้ $x_1$ ถึง $x_n$",
            "เมื่อกราฟอยู่ใต้แกน x ค่าอินทิกรัลเป็นลบ พื้นที่ต้องใช้ค่าสัมบูรณ์",
            "การเพิ่ม $n$ ให้ละเอียดขึ้น แต่ยังเป็นการประมาณ ถ้ายังไม่เข้าลิมิต",
        ],
        "applications": [
            "การประมาณระยะทางจากกราฟความเร็วกับเวลา",
            "การหาปริมาณสะสม เช่น น้ำ ไฟฟ้า งาน",
            "เป็นแนวคิดตั้งต้นของ definite integral",
        ],
        "decision_guide": (
            "ใช้ผลรวมรีมันน์เมื่อ: ($1$) ต้องการประมาณพื้นที่ใต้กราฟแบบตัวเลข, "
            "($2$) ต้องการเห็นแนวคิดที่มาของอินทิกรัล, "
            "($3$) ฟังก์ชันอินทิเกรตตรงๆ ยาก ใช้การประมาณแทน"
        ),
    },
    # ------------------------------------------------------------------
    # บทเรียน interactive เพิ่มเติม (skeleton สำหรับนักศึกษา)
    # TODO: เติม/ปรับปรุงรายละเอียดแต่ละหัวข้อให้สมบูรณ์
    # อ้างอิงเนื้อหาจาก data/lessons/ ตาม docs/interactive-lessons-plan.md
    # ------------------------------------------------------------------
    "tangent": {
        "title": "เส้นสัมผัสและอนุพันธ์ (Tangent Line and Derivative)",
        "conditions": [
            "ฟังก์ชัน $f$ ต่อเนื่องที่จุด $a$",
            "ลิมิต $\\lim_{h \\to 0} \\frac{f(a+h)-f(a)}{h}$ มีค่า (หาอนุพันธ์ได้)",
            "TODO: เติมเงื่อนไขเพิ่มเติมจาก cal1/ch02/01-geometric-problems.md",
        ],
        "formulas": [
            "ความชันเส้นสัมผัส: $m = f'(a) = \\lim_{h \\to 0} \\frac{f(a+h)-f(a)}{h}$",
            "สมการเส้นสัมผัส: $y - f(a) = f'(a)(x-a)$",
            "TODO: เติมสูตรเพิ่มเติม",
        ],
        "properties": [
            "เส้นสัมผัสแตะกราฟที่จุด $(a, f(a))$ พอดี",
            "TODO: เติมสมบัติเพิ่มเติม",
        ],
        "cautions": [
            "TODO: เติมข้อควรระวัง เช่น ฟังก์ชันหาอนุพันธ์ไม่ได้ที่จุดหักมุม",
        ],
        "applications": [
            "TODO: เติมการประยุกต์",
        ],
        "decision_guide": "TODO: เติมคำแนะนำการเลือกใช้",
    },
    "limit": {
        "title": "ลิมิตเข้าใกล้จุด (Limit at a Point)",
        "conditions": [
            "พิจารณา $\\lim_{x \\to a} f(x)$ เมื่อ $x$ เข้าใกล้ $a$ แต่ $x \\ne a$",
            "TODO: เติมเงื่อนไขจาก cal1/ch04/01-indeterminate-forms.md",
        ],
        "formulas": [
            "นิยาม: $\\lim_{x \\to a} f(x) = L$",
            "รูปแบบไม่กำหนด: $\\frac{0}{0}, \\frac{\\infty}{\\infty}, 0^0, 1^\\infty, \\infty^0$",
            "TODO: เติมสูตรเพิ่มเติม",
        ],
        "properties": [
            "TODO: เติมสมบัติ เช่น ลิมิตผลบวก/ผลคูณ/ผลหาร",
        ],
        "cautions": [
            "TODO: เติมข้อควรระวัง",
        ],
        "applications": [
            "TODO: เติมการประยุกต์",
        ],
        "decision_guide": "TODO: เติมคำแนะนำ",
    },
    "substitution": {
        "title": "การอินทิเกรตโดยการแทน (Integration by Substitution)",
        "conditions": [
            "อินทิกรัลมีรูปแบบ $\\int f(g(x))\\,g'(x)\\,dx$",
            "TODO: เติมเงื่อนไขจาก cal2/ch02/01-integration-by-substitution.md",
        ],
        "formulas": [
            "ตั้ง $u = g(x)$ แล้ว $du = g'(x)\\,dx$",
            "$\\int u^n\\,du = \\frac{u^{n+1}}{n+1}+C,\\quad n\\ne -1$",
            "TODO: เติมสูตรเพิ่มเติม",
        ],
        "properties": [
            "TODO: เติมสมบัติ",
        ],
        "cautions": [
            "TODO: เติมข้อควรระวัง เช่น ลืมแทนค่ากลับ",
        ],
        "applications": [
            "TODO: เติมการประยุกต์",
        ],
        "decision_guide": "TODO: เติมคำแนะนำ",
    },
    "volume": {
        "title": "ปริมาตรของทรงตัน (Volume of Solids)",
        "conditions": [
            "ทรงตันที่ตัดแบ่งเป็นแผ่นบางตามแกน",
            "TODO: เติมเงื่อนไขจาก cal2/ch03/02-volume-of-solids.md",
        ],
        "formulas": [
            "วิธีตัดแบ่ง: $V = \\int_a^b A(x)\\,dx$ เมื่อ $A(x)$ คือพื้นที่หน้าตัด",
            "วิธีจานหมุน (disk): $V = \\pi\\int_a^b [R(x)]^2\\,dx$",
            "วิธีวงแหวน (washer): $V = \\pi\\int_a^b ([R(x)]^2 - [r(x)]^2)\\,dx$",
        ],
        "properties": [
            "TODO: เติมสมบัติ",
        ],
        "cautions": [
            "TODO: เติมข้อควรระวัง เช่น สับสน R กับ r",
        ],
        "applications": [
            "TODO: เติมการประยุกต์",
        ],
        "decision_guide": "TODO: เติมคำแนะนำ",
    },
    "area_between": {
        "title": "พื้นที่ระหว่างเส้นโค้ง (Area Between Curves)",
        "conditions": [
            "เส้นโค้ง $y=f(x)$ อยู่เหนือ $y=g(x)$ บนช่วง $[a,b]$",
            "TODO: เติมเงื่อนไขจาก cal2/ch03/01-area-under-curve.md",
        ],
        "formulas": [
            "พื้นที่: $A = \\int_a^b (f(x)-g(x))\\,dx$",
            "หาจุดตัดโดยแก้ $f(x)=g(x)$",
            "TODO: เติมสูตรเพิ่มเติม",
        ],
        "properties": [
            "TODO: เติมสมบัติ",
        ],
        "cautions": [
            "TODO: เติมข้อควรระวัง เช่น ต้องรู้ว่าเส้นไหนอยู่บน",
        ],
        "applications": [
            "TODO: เติมการประยุกต์",
        ],
        "decision_guide": "TODO: เติมคำแนะนำ",
    },
    "improper": {
        "title": "อินทิกรัลไม่แท้ (Improper Integral)",
        "conditions": [
            "ขอบเขตเป็นอนันต์ หรือฟังก์ชันไม่ต่อเนื่องบนช่วง",
            "TODO: เติมเงื่อนไขจาก cal2/ch04/01-improper-type1-discontinuous.md",
        ],
        "formulas": [
            "ขอบเขตไม่จำกัด: $\\int_a^{\\infty} f(x)\\,dx = \\lim_{t \\to \\infty}\\int_a^t f(x)\\,dx$",
            "ฟังก์ชันไม่ต่อเนื่อง: $\\int_a^b f(x)\\,dx = \\lim_{t \\to b^-}\\int_a^t f(x)\\,dx$",
            "TODO: เติมสูตรเพิ่มเติม",
        ],
        "properties": [
            "TODO: เติมสมบัติ เช่น เงื่อนไขลู่เข้า",
        ],
        "cautions": [
            "TODO: เติมข้อควรระวัง เช่น ลิมิตไม่มีค่า = ลู่ออก",
        ],
        "applications": [
            "TODO: เติมการประยุกต์",
        ],
        "decision_guide": "TODO: เติมคำแนะนำ",
    },
}
