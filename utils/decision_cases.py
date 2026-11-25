"""utils/decision_cases.py

Active Scaffolding decision cases data and renderer for calculus learning.
Extracts repetitive case study blocks from page files into clean, reusable structures.
"""

from typing import Any
import streamlit as st


# =============================================================================
# 1. Integration by Substitution Cases (6 Cases)
# =============================================================================
SUBSTITUTION_CASES: list[dict[str, Any]] = [
    {
        "id": 1,
        "total": 6,
        "title": "ฟังก์ชันใต้กรณฑ์ยกกำลัง",
        "selector_title": "กรณีที่ 1: ฟังก์ชันใต้กรณฑ์ยกกำลัง (2x √(x² + 1))",
        "latex": r"\int 2x\sqrt{x^2+1} \, dx",
        "description": None,
        "question": "**ท่านจะเลือกกำหนดตัวแปร $u$ เป็นฟังก์ชันใด?**",
        "radio_label": "ท่านจะเลือกกำหนด u เป็นฟังก์ชันใด?",
        "radio_key": "radio_u_case1",
        "options": [
            "แนวทาง A: ให้ u = x² + 1 (ฟังก์ชันใต้กรณฑ์)",
            "แนวทาง B: ให้ u = 2x (ฟังก์ชันสัมประสิทธิ์ด้านนอก)",
            "แนวทาง C: ให้ u = x (ตัวแปรเดิม)",
        ],
        "feedbacks": {
            "แนวทาง A": {
                "type": "success",
                "message": r"**ถูกต้องตามหลักการ:** เมื่อเลือก $u = x^2 + 1$ จะได้ $du = 2x\,dx$ ซึ่งพจน์ $2x$ จะตัดทอนกับตัวคูณด้านหน้าหมดพอดี",
                "latex_ans": r"\int 2x\sqrt{x^2+1} \, dx = \frac{2}{3}(x^2+1)^{3/2} + C",
                "worked_steps": r"""
1. **กำหนดตัวแปรและหาอนุพันธ์:**
   $$u = x^2 + 1 \implies \frac{du}{dx} = 2x \implies dx = \frac{du}{2x}$$
2. **แทนค่าในโจทย์:**
   $$\int 2x\sqrt{x^2+1} \, dx = \int 2x \cdot \sqrt{u} \cdot \frac{du}{2x}$$
3. **ตัดทอนตัวแปรเดิม:**
   $$\int \sqrt{u} \, du = \int u^{1/2} \, du = \frac{2}{3}u^{3/2} + C$$
4. **แทนค่า $u$ กลับคืน:**
   $$= \frac{2}{3}(x^2+1)^{3/2} + C$$
""",
            },
            "แนวทาง B": {
                "type": "error",
                "message": r"**ยังไม่เหมาะสม:** หากเลือก $u = 2x$ จะได้ $du = 2dx$ ใต้กรณฑ์จะกลายเป็น $\sqrt{(u/2)^2+1}$ ซึ่งยังคงติดตัวแปร $u$ ซับซ้อนและตัดทอนไม่ได้",
            },
        },
        "default_feedback": {
            "type": "warning",
            "message": "**ไม่มีการเปลี่ยนแปลง:** การให้ $u = x$ เป็นเพียงการเปลี่ยนชื่อตัวแปร ไม่ได้ช่วยลดความซับซ้อนของโจทย์",
        },
    },
    {
        "id": 2,
        "total": 6,
        "title": "ฟังก์ชันตัวส่วนและลอการิทึม",
        "selector_title": "กรณีที่ 2: ฟังก์ชันตัวส่วนและลอการิทึม ((ln x) / x)",
        "latex": r"\int \frac{\ln x}{x} \, dx",
        "description": None,
        "question": "**ท่านจะเลือกกำหนดตัวแปร $u$ เป็นฟังก์ชันใด?**",
        "radio_label": "ท่านจะเลือกกำหนด u เป็นฟังก์ชันใด?",
        "radio_key": "radio_u_case2",
        "options": [
            "แนวทาง A: ให้ u = x (ตัวส่วน)",
            "แนวทาง B: ให้ u = ln(x) (ตัวเศษ)",
            "แนวทาง C: ให้ u = 1/x",
        ],
        "feedbacks": {
            "แนวทาง B": {
                "type": "success",
                "message": r"**ถูกต้องตามหลักการ:** อนุพันธ์ของ $\ln(x)$ คือ $\frac{1}{x}$ ซึ่งจะตัดกับตัวส่วน $x$ หายไปหมดพอดี",
                "latex_ans": r"\int \frac{\ln x}{x} \, dx = \frac{(\ln x)^2}{2} + C",
                "worked_steps": r"""
1. **กำหนดตัวแปรและหาอนุพันธ์:**
   $$u = \ln x \implies \frac{du}{dx} = \frac{1}{x} \implies dx = x\,du$$
2. **แทนค่าในโจทย์:**
   $$\int \frac{\ln x}{x} \, dx = \int \frac{u}{x} \cdot (x\,du)$$
3. **ตัดทอนตัวแปรเดิม:**
   $$\int u \, du = \frac{u^2}{2} + C$$
4. **แทนค่า $u$ กลับคืน:**
   $$= \frac{(\ln x)^2}{2} + C \quad (x > 0)$$
""",
            },
            "แนวทาง A": {
                "type": "warning",
                "message": r"**ไม่มีการเปลี่ยนแปลง:** ได้เพียง $\int \frac{\ln u}{u}\,du$ ซึ่งเหมือนโจทย์เดิม",
            },
        },
        "default_feedback": {
            "type": "error",
            "message": r"**รูปจะซับซ้อนขึ้น:** หากเลือก $u = 1/x$ จะได้ $du = -\frac{1}{x^2}\,dx$ ซึ่งทำให้ดีกรีตัวส่วนเพิ่มขึ้นเป็น $x^2$",
        },
    },
    {
        "id": 3,
        "total": 6,
        "title": "ฟังก์ชันตรีโกณมิติและเลขชี้กำลัง",
        "selector_title": "กรณีที่ 3: ฟังก์ชันตรีโกณมิติและเลขชี้กำลัง (cos(x) e^(sin x))",
        "latex": r"\int \cos(x) e^{\sin(x)} \, dx",
        "description": None,
        "question": "**ท่านจะเลือกกำหนดตัวแปร $u$ เป็นฟังก์ชันใด?**",
        "radio_label": "ท่านจะเลือกกำหนด u เป็นฟังก์ชันใด?",
        "radio_key": "radio_u_case3",
        "options": [
            "แนวทาง A: ให้ u = sin(x) (ฟังก์ชันภายในเลขชี้กำลัง)",
            "แนวทาง B: ให้ u = cos(x) (สัมประสิทธิ์ด้านหน้า)",
            "แนวทาง C: ให้ u = e^(sin x)",
        ],
        "feedbacks": {
            "แนวทาง A": {
                "type": "success",
                "message": r"**ถูกต้องตามหลักการ:** หาอนุพันธ์ของ $u = \sin(x)$ ได้ $du = \cos(x)\,dx$ ซึ่งตัดกับ $\cos(x)$ ด้านหน้าหมดพอดี",
                "latex_ans": r"\int \cos(x) e^{\sin(x)} \, dx = e^{\sin(x)} + C",
                "worked_steps": r"""
1. **กำหนดตัวแปรและหาอนุพันธ์:**
   $$u = \sin(x) \implies du = \cos(x)\,dx \implies dx = \frac{du}{\cos(x)}$$
2. **แทนค่าและตัดทอน:**
   $$\int \cos(x) e^u \cdot \frac{du}{\cos(x)} = \int e^u \, du = e^u + C$$
3. **แทนค่า $u$ กลับคืน:**
   $$= e^{\sin(x)} + C$$
""",
            },
            "แนวทาง C": {
                "type": "info",
                "message": r"**ทำได้เช่นกัน:** หากให้ $u = e^{\sin x} \implies du = e^{\sin x}\cos(x)dx$ จะได้ $\int 1\,du = u + C = e^{\sin x} + C$",
            },
        },
        "default_feedback": {
            "type": "error",
            "message": r"**ยังไม่เหมาะสม:** หาอนุพันธ์ของ $\cos(x)$ ได้ $-\sin(x)$ ซึ่งไม่สามารถตัดกับ $\sin(x)$ ที่ติดอยู่บนเลขชี้กำลังได้",
        },
    },
    {
        "id": 4,
        "total": 6,
        "title": "การจัดรูปพีชคณิตเสริมเมื่อยังเหลือตัวแปร x",
        "selector_title": "กรณีที่ 4: การจัดรูปพีชคณิตเสริมเมื่อยังเหลือตัวแปร x (x √(x + 1))",
        "latex": r"\int x\sqrt{x+1} \, dx",
        "description": None,
        "question": "**ท่านจะแก้ปัญหาตัวแปร $x$ ด้านหน้าที่เหลืออยู่อย่างไร?**",
        "radio_label": "ท่านจะแก้ปัญหาตัวแปร x ด้านหน้าที่เหลืออยู่อย่างไร?",
        "radio_key": "radio_u_case4",
        "options": [
            "แนวทาง A: แทน x = u - 1 แล้วคูณกระจายเข้าไปในวงเล็บ",
            "แนวทาง B: ดึง x ออกนอกอินทิกรัลเลยเพราะเป็นตัวคูณ",
            "แนวทาง C: ถือว่าทำไม่ได้ด้วย u-Substitution ต้องเปลี่ยนไปใช้วิธีอื่นทันที",
            "แนวทาง D: ให้ u = √(x+1)",
        ],
        "feedbacks": {
            "แนวทาง B": {
                "type": "error",
                "message": r"**ข้อควรระวัง:** ห้ามดึงตัวแปรที่กำลังอินทิเกรต ($x$) ออกนอกเครื่องหมาย $\int$ ดึงได้เฉพาะค่าคงที่เท่านั้น",
            },
            "แนวทาง A": {
                "type": "success",
                "message": "**ถูกต้องตามหลักการ:** จัดรูป $x = u - 1$ แล้วคูณกระจาย $(u - 1)u^{1/2} = u^{3/2} - u^{1/2}$ ทำให้หาอินทิกรัลทีละพจน์ได้",
                "latex_ans": r"\int x\sqrt{x+1} \, dx = \frac{2}{5}(x+1)^{5/2} - \frac{2}{3}(x+1)^{3/2} + C",
                "worked_steps": r"""
1. **สลับรูปตัวแปร:**
   $$u = x + 1 \implies x = u - 1 \quad \text{และ} \quad dx = du$$
2. **แทนค่าลงในอินทิกรัล:**
   $$\int x\sqrt{x+1}\,dx = \int (u - 1)\sqrt{u}\,du = \int (u - 1)u^{1/2}\,du$$
3. **คูณกระจายและอินทิเกรตทีละพจน์:**
   $$= \int (u^{3/2} - u^{1/2})\,du = \frac{2}{5}u^{5/2} - \frac{2}{3}u^{3/2} + C$$
4. **แทนค่า $u$ กลับคืน:**
   $$= \frac{2}{5}(x+1)^{5/2} - \frac{2}{3}(x+1)^{3/2} + C$$
""",
            },
            "แนวทาง D": {
                "type": "info",
                "message": r"**ทำได้เช่นกัน:** หากให้ $u = \sqrt{x+1} \implies u^2 = x+1$ จัดรูปเป็น $\int 2(u^4 - u^2)\,du$ ซึ่งได้ผลลัพธ์เดียวกัน",
            },
        },
        "default_feedback": {
            "type": "warning",
            "message": r"**ยังไม่ถูกต้อง:** โจทย์ข้อนี้ยังสามารถแก้ได้ด้วยการจัดรูปพีชคณิต $x = u - 1$",
        },
    },
    {
        "id": 5,
        "total": 6,
        "title": "ฟังก์ชันเศษส่วนและอนุพันธ์ของตัวส่วน",
        "selector_title": "กรณีที่ 5: ฟังก์ชันเศษส่วนและอนุพันธ์ของตัวส่วน (2x / (x² + 1))",
        "latex": r"\int \frac{2x}{x^2+1} \, dx",
        "description": None,
        "question": "**ท่านจะเลือกกำหนดตัวแปร $u$ เป็นฟังก์ชันใด?**",
        "radio_label": "ท่านจะเลือกกำหนด u เป็นฟังก์ชันใด?",
        "radio_key": "radio_u_case5",
        "options": [
            "แนวทาง A: ให้ u = x² + 1 (ตัวส่วนทั้งก้อน)",
            "แนวทาง B: ให้ u = 2x (ตัวเศษ)",
            "แนวทาง C: ให้ u = x",
        ],
        "feedbacks": {
            "แนวทาง A": {
                "type": "success",
                "message": r"**ถูกต้องตามหลักการ:** ตัวเศษ $2x$ คืออนุพันธ์ของตัวส่วนพอดี ได้รูปพื้นฐาน $\int \frac{1}{u}\,du = \ln|u| + C$",
                "latex_ans": r"\int \frac{2x}{x^2+1} \, dx = \ln(x^2+1) + C",
                "worked_steps": r"""
1. **กำหนดตัวแปรและหาอนุพันธ์:**
   $$u = x^2 + 1 \implies du = 2x\,dx \implies dx = \frac{du}{2x}$$
2. **แทนค่าลงในอินทิกรัลและตัดทอน:**
   $$\int \frac{2x}{x^2+1}\,dx = \int \frac{2x}{u} \cdot \frac{du}{2x} = \int \frac{1}{u}\,du$$
3. **คำนวณปริพันธ์พื้นฐาน:**
   $$= \ln|u| + C = \ln(x^2+1) + C \quad (\text{เนื่องจาก } x^2+1 > 0 \text{ เสมอ})$$
""",
            },
            "แนวทาง B": {
                "type": "error",
                "message": "**ยังไม่เหมาะสม:** หากให้ $u = 2x$ จะได้ตัวส่วนเป็น $(u/2)^2+1$ ซึ่งยังคงเป็นเศษส่วนพีชคณิตและไม่ช่วยให้ง่ายขึ้น",
            },
        },
        "default_feedback": {
            "type": "warning",
            "message": "**ไม่มีการเปลี่ยนแปลง:** การให้ $u = x$ ไม่ได้ช่วยลดความซับซ้อนของฟังก์ชัน",
        },
    },
    {
        "id": 6,
        "total": 6,
        "title": "พหุนามยกกำลังและอนุพันธ์ภายใน",
        "selector_title": "กรณีที่ 6: พหุนามยกกำลังและอนุพันธ์ภายใน (3x² (x³ + 5)⁴)",
        "latex": r"\int 3x^2 (x^3+5)^4 \, dx",
        "description": None,
        "question": "**ท่านจะเลือกกำหนดตัวแปร $u$ เป็นฟังก์ชันใด?**",
        "radio_label": "ท่านจะเลือกกำหนด u เป็นฟังก์ชันใด?",
        "radio_key": "radio_u_case6",
        "options": [
            "แนวทาง A: ให้ u = x³ + 5 (ฟังก์ชันฐานในวงเล็บยกกำลัง)",
            "แนวทาง B: ให้ u = 3x² (สัมประสิทธิ์ด้านหน้า)",
            "แนวทาง C: ให้ u = (x³ + 5)⁴",
        ],
        "feedbacks": {
            "แนวทาง A": {
                "type": "success",
                "message": r"**ถูกต้องตามหลักการ:** หาอนุพันธ์ของฐาน $u = x^3 + 5$ ได้ $du = 3x^2\,dx$ ตัดกับ $3x^2$ ด้านหน้าหมด เหลือเพียง $\int u^4\,du$",
                "latex_ans": r"\int 3x^2 (x^3+5)^4 \, dx = \frac{(x^3+5)^5}{5} + C",
                "worked_steps": r"""
1. **กำหนดตัวแปรและหาอนุพันธ์:**
   $$u = x^3 + 5 \implies du = 3x^2\,dx \implies dx = \frac{du}{3x^2}$$
2. **แทนค่าและตัดทอน:**
   $$\int 3x^2(x^3+5)^4\,dx = \int 3x^2 \cdot u^4 \cdot \frac{du}{3x^2} = \int u^4\,du$$
3. **คำนวณปริพันธ์และแทนค่ากลับ:**
   $$= \frac{u^5}{5} + C = \frac{(x^3+5)^5}{5} + C$$
""",
            },
            "แนวทาง C": {
                "type": "error",
                "message": "**รูปจะซับซ้อนขึ้น:** การเลือกยกกำลัง 4 จะทำให้เกิดพจน์อนุพันธ์ลูกโซ่ซับซ้อนย้อนกลับไปหาร",
            },
        },
        "default_feedback": {
            "type": "error",
            "message": "**ยังไม่เหมาะสม:** หาอนุพันธ์ของ $3x^2$ ได้ $6x$ ซึ่งไม่สามารถตัดทอนพจน์ $(x^3+5)^4$ ได้",
        },
    },
]


# =============================================================================
# 2. Integration by Parts Cases (6 Cases)
# =============================================================================
BY_PARTS_CASES: list[dict[str, Any]] = [
    {
        "id": 1,
        "total": 6,
        "title": "พหุนามคูณกับเอกซ์โพเนนเชียล",
        "selector_title": "กรณีที่ 1: พหุนามคูณกับเอกซ์โพเนนเชียล (x e^x)",
        "latex": r"\int x e^x \, dx",
        "description": "โจทย์ข้อนี้เกิดจากฟังก์ชันพีชคณิต ($A$: $x$) คูณกับเอกซ์โพเนนเชียล ($E$: $e^x$)",
        "question": "**ตามกฎ LIATE ท่านควรเลือก $u$ และ $dv$ อย่างไร?**",
        "radio_label": "ตามกฎ LIATE ท่านควรเลือก u และ dv อย่างไร?",
        "radio_key": "radio_parts_case1",
        "options": [
            "แนวทางที่ 1: ให้ u = x และ dv = e^x dx",
            "แนวทางที่ 2: ให้ u = e^x และ dv = x dx",
        ],
        "feedbacks": {
            "แนวทางที่ 1": {
                "type": "success",
                "message": "**ถูกต้องตามหลักการ (A มาก่อน E ในกฎ LIATE):** หาอนุพันธ์ของ $u = x$ ดีกรีลดลงเหลือ $1$ ส่วน $e^x$ หาปริพันธ์ง่ายและคงรูปเดิม",
                "latex_ans": r"\int x e^x \, dx = e^x(x - 1) + C",
                "worked_steps": r"""
1. **คำนวณส่วนประกอบ:**
   * กำหนด $u = x \implies du = dx$ (ดีกรีลดลงเหลือค่าคงที่)
   * กำหนด $dv = e^x dx \implies v = \int e^x dx = e^x$
2. **แทนค่าลงในสูตร By Parts:**
   $$\int u \, dv = uv - \int v \, du$$
   $$\int x e^x \, dx = x e^x - \int e^x \, dx$$
3. **คำนวณอินทิกรัลส่วนที่เหลือ:**
   $$= x e^x - e^x + C = e^x(x - 1) + C$$
""",
            },
        },
        "default_feedback": {
            "type": "error",
            "message": r"**รูปสมการจะซับซ้อนขึ้น:** หากเลือก $dv = x dx$ จะได้ $v = \frac{x^2}{2}$ ทำให้อินทิกรัลใหม่กลายเป็น $x^2 e^x$ ซึ่งดีกรีสูงขึ้นและยากกว่าเดิม",
        },
    },
    {
        "id": 2,
        "total": 6,
        "title": "ฟังก์ชันเดี่ยว (ln x)",
        "selector_title": "กรณีที่ 2: ฟังก์ชันเดี่ยวที่หาอนุพันธ์ง่ายแต่อินทิเกรตยาก (ln x)",
        "latex": r"\int \ln(x) \, dx",
        "description": None,
        "question": r"**ตามกฎ LIATE ท่านควรแบ่งบทบาท $u$ และ $dv$ อย่างไรสำหรับ $\int \ln(x) \cdot 1 \, dx$?**",
        "radio_label": "ท่านจะแบ่งบทบาทอย่างไร?",
        "radio_key": "radio_parts_case2",
        "options": [
            "แนวทางที่ 1: ให้ u = 1 และ dv = ln(x) dx",
            "แนวทางที่ 2: ให้ u = ln(x) และ dv = 1 dx",
        ],
        "feedbacks": {
            "แนวทางที่ 2": {
                "type": "success",
                "message": r"**ถูกต้องตามหลักการ (L มาเป็นอันดับแรกในกฎ LIATE):** $\ln(x)$ หาปริพันธ์ตรงยาก แต่หาอนุพันธ์ได้ $\frac{1}{x}$ พีชคณิต ซึ่งตัดทอนกับ $v = x$ ได้ลงตัว",
                "latex_ans": r"\int \ln(x) \, dx = x(\ln x - 1) + C",
                "worked_steps": r"""
1. **กำหนดส่วนประกอบ:**
   * $u = \ln(x) \implies du = \frac{1}{x} dx$ (เปลี่ยนลอการิทึมเป็นเศษส่วนพีชคณิต)
   * $dv = dx \implies v = x$
2. **แทนในสูตร By Parts:**
   $$\int \ln(x) \, dx = (\ln x)(x) - \int x \cdot \frac{1}{x} \, dx = x \ln(x) - \int 1 \, dx$$
3. **สรุปผลลัพธ์:**
   $$= x \ln(x) - x + C = x(\ln x - 1) + C \quad (x > 0)$$
""",
            },
        },
        "default_feedback": {
            "type": "error",
            "message": r"**ทางตัน:** หากเลือก $dv = \ln(x) dx$ ท่านจะต้องหา $v = \int \ln(x) dx$ ซึ่งก็คือโจทย์ตั้งต้นนั่นเอง",
        },
    },
    {
        "id": 3,
        "total": 6,
        "title": "พหุนามดีกรีสูงกว่า 1",
        "selector_title": "กรณีที่ 3: พหุนามดีกรีสูงกว่า 1 ต้องทำซ้ำหลายชั้น (x² e^x)",
        "latex": r"\int x^2 e^x \, dx",
        "description": None,
        "question": "**ขั้นตอนการลดรูปพหุนามควรเป็นอย่างไร?**",
        "radio_label": "ขั้นตอนการลดรูปควรเป็นอย่างไร?",
        "radio_key": "radio_parts_case3",
        "options": [
            "แนวทาง A: ทำรอบที่ 1 ลดเหลือ x e^x แล้วทำรอบที่ 2 ลดเหลือค่าคงที่",
            "แนวทาง B: สลับ u และ dv ในรอบที่ 2 เพื่อความรวดเร็ว",
        ],
        "feedbacks": {
            "แนวทาง A": {
                "type": "success",
                "message": r"**ถูกต้องตามหลักการ (ลดทอนดีกรีแบบต่อเนื่อง):** พหุนามดีกรี 2 ต้องทำ 2 รอบ ($x^2 \to 2x \to 2$) จนกระทั่งเหลืออินทิกรัลพื้นฐาน",
                "latex_ans": r"\int x^2 e^x \, dx = e^x(x^2 - 2x + 2) + C",
                "worked_steps": r"""
1. **รอบที่ 1:** ให้ $u = x^2 \implies du = 2x dx$, $dv = e^x dx \implies v = e^x$
   $$\int x^2 e^x dx = x^2 e^x - 2\int x e^x dx$$
2. **รอบที่ 2 (ทำซ้ำกับก้อน $\int x e^x dx$):** ให้ $u = x \implies du = dx$, $dv = e^x dx \implies v = e^x$
   $$\int x e^x dx = x e^x - e^x$$
3. **ประกอบผลลัพธ์:**
   $$\int x^2 e^x dx = x^2 e^x - 2(x e^x - e^x) + C = e^x(x^2 - 2x + 2) + C$$
""",
            },
        },
        "default_feedback": {
            "type": "error",
            "message": "**ข้อควรระวัง:** การสลับบทบาท $u$ และ $dv$ ในรอบถัดไปจะทำให้พจน์ตัดทอนกันหมดกลายเป็น $0 = 0$",
        },
    },
    {
        "id": 4,
        "total": 6,
        "title": "ฟังก์ชันวนลูปไม่รู้จบ (Cyclic Integration)",
        "selector_title": "กรณีที่ 4: ฟังก์ชันวนลูปไม่รู้จบ (e^x cos x)",
        "latex": r"I = \int e^x \cos(x) \, dx",
        "description": None,
        "question": "**ท่านจะเริ่มต้นกำหนด $u$ และ $dv$ รอบแรกอย่างไร?**",
        "radio_label": "ท่านจะเริ่มต้นกำหนด u และ dv รอบแรกอย่างไร?",
        "radio_key": "radio_parts_case4",
        "options": [
            "แนวทางที่ 1: กำหนด u = cos(x) และ dv = e^x dx (แล้วทำรอบสองให้สอดคล้องกัน)",
            "แนวทางที่ 2: กำหนด u = e^x และ dv = cos(x) dx (แล้วทำรอบสองให้สอดคล้องกัน)",
            "แนวทางที่ 3: รอบแรกเลือก u = cos(x) แต่รอบสองสลับกลับมาเลือก u = e^x",
        ],
        "feedbacks": {
            "แนวทางที่ 3": {
                "type": "error",
                "message": "**ข้อควรระวัง:** หากรอบแรกกำหนดฟังก์ชันหนึ่งเป็น $u$ แต่รอบที่สองสลับกลับมา ผลลัพธ์จะหักล้างกันกลายเป็น $I = I$ หรือ $0 = 0$",
            },
        },
        "default_feedback": {
            "type": "success",
            "message": r"**ถูกต้องตามหลักการ (Cyclic By Parts):** ทั้ง $e^x$ และ $\cos(x)$ วนกลับมารูปเดิม ทำ By Parts 2 รอบแล้วย้ายข้างสมการทางพีชคณิตเพื่อหาคำตอบ",
            "latex_ans": r"\int e^x \cos(x) \, dx = \frac{e^x(\sin x + \cos x)}{2} + C",
            "worked_steps": r"""
1. **รอบที่ 1 ($u = e^x, dv = \cos(x) dx$):**
   $$u = e^x \implies du = e^x dx, \quad dv = \cos(x) dx \implies v = \sin(x)$$
   $$I = e^x \sin(x) - \int e^x \sin(x) \, dx$$
2. **รอบที่ 2 (ทำ By Parts ซ้ำกับ $\int e^x \sin x dx$ โดยคงบทบาทเดิม):**
   $$u = e^x \implies du = e^x dx, \quad dv = \sin(x) dx \implies v = -\cos(x)$$
   $$\int e^x \sin(x) \, dx = -e^x \cos(x) - \int (-e^x \cos x) \, dx = -e^x \cos(x) + I$$
3. **นำผลรอบที่ 2 แทนกลับในสมการแรกแล้วย้ายข้าง:**
   $$I = e^x \sin(x) - \left[ -e^x \cos(x) + I \right] = e^x \sin(x) + e^x \cos(x) - I$$
   $$2I = e^x(\sin x + \cos x) \implies I = \frac{e^x}{2}(\sin x + \cos x) + C$$
""",
        },
    },
    {
        "id": 5,
        "total": 6,
        "title": "พีชคณิตคูณกับตรีโกณมิติ",
        "selector_title": "กรณีที่ 5: พีชคณิตคูณกับฟังก์ชันตรีโกณมิติ (x sin x)",
        "latex": r"\int x \sin(x) \, dx",
        "description": None,
        "question": "**ตามกฎ LIATE ท่านควรเลือก $u$ และ $dv$ อย่างไร?**",
        "radio_label": "ท่านจะเลือกกำหนด u และ dv อย่างไร?",
        "radio_key": "radio_parts_case5",
        "options": [
            "แนวทางที่ 1: ให้ u = x และ dv = sin(x) dx",
            "แนวทางที่ 2: ให้ u = sin(x) และ dv = x dx",
        ],
        "feedbacks": {
            "แนวทางที่ 1": {
                "type": "success",
                "message": r"**ถูกต้องตามกฎ LIATE (A มาก่อน T):** เลือก $u = x$ ทำให้หาอนุพันธ์ได้ $du = dx$ ดีกรีลดลง ส่วน $\sin(x)$ หาปริพันธ์ได้ $-\cos(x)$",
                "latex_ans": r"\int x \sin(x) \, dx = -x\cos(x) + \sin(x) + C",
                "worked_steps": r"""
1. **กำหนดตัวแปรและหาอนุพันธ์/ปฏิยานุพันธ์:**
   * $u = x \implies du = dx$
   * $dv = \sin(x)dx \implies v = -\cos(x)$
2. **แทนค่าในสูตร By Parts:**
   $$\int x\sin(x)\,dx = (x)(-\cos x) - \int (-\cos x)\,dx = -x\cos(x) + \int \cos(x)\,dx$$
3. **คำนวณผลลัพธ์สุดท้าย:**
   $$= -x\cos(x) + \sin(x) + C$$
""",
            },
        },
        "default_feedback": {
            "type": "error",
            "message": r"**รูปสมการจะซับซ้อนขึ้น:** หากเลือก $dv = x dx$ จะได้ $v = \frac{x^2}{2}$ ทำให้อินทิกรัลใหม่กลายเป็น $x^2 \cos(x)$ ซึ่งดีกรีสูงขึ้น",
        },
    },
    {
        "id": 6,
        "total": 6,
        "title": "พีชคณิตคูณกับลอการิทึม",
        "selector_title": "กรณีที่ 6: พีชคณิตคูณกับลอการิทึม (x ln x)",
        "latex": r"\int x \ln(x) \, dx",
        "description": None,
        "question": "**ตามกฎ LIATE ท่านควรเลือก $u$ เป็นฟังก์ชันใด?**",
        "radio_label": "ตามกฎ LIATE ท่านควรเลือก u เป็นฟังก์ชันใด?",
        "radio_key": "radio_parts_case6",
        "options": [
            "แนวทางที่ 1: ให้ u = ln(x) และ dv = x dx",
            "แนวทางที่ 2: ให้ u = x และ dv = ln(x) dx",
        ],
        "feedbacks": {
            "แนวทางที่ 1": {
                "type": "success",
                "message": r"**ถูกต้องตามกฎ LIATE (L มาก่อน A เสมอ):** แม้ $x$ จะเป็นพหุนาม แต่ $\ln(x)$ หาปริพันธ์ยาก จึงต้องเลือกเป็น $u$ เพื่อหาอนุพันธ์ให้เป็นพีชคณิต $\frac{1}{x}$",
                "latex_ans": r"\int x \ln(x) \, dx = \frac{x^2}{4}(2\ln x - 1) + C",
                "worked_steps": r"""
1. **กำหนดตัวแปรและหาอนุพันธ์:**
   * $u = \ln(x) \implies du = \frac{1}{x}dx$
   * $dv = x dx \implies v = \frac{x^2}{2}$
2. **แทนค่าลงในสูตร By Parts:**
   $$\int x\ln(x)\,dx = (\ln x)\left(\frac{x^2}{2}\right) - \int \frac{x^2}{2} \cdot \frac{1}{x}\,dx = \frac{x^2\ln x}{2} - \frac{1}{2}\int x\,dx$$
3. **คำนวณผลลัพธ์สุดท้าย:**
   $$= \frac{x^2\ln x}{2} - \frac{x^2}{4} + C = \frac{x^2}{4}(2\ln x - 1) + C$$
""",
            },
        },
        "default_feedback": {
            "type": "error",
            "message": r"**ทางตัน:** หากเลือก $dv = \ln(x)dx$ จะต้องหาปริพันธ์ของ $\ln(x)$ ซึ่งต้องใช้ By Parts ซ้ำซ้อนและผิดหลัก LIATE",
        },
    },
]


# =============================================================================
# 3. Decision Case Renderer
# =============================================================================
def render_decision_case(case: dict[str, Any]) -> None:
    """Render a single tactile Bauhaus decision challenge card."""
    badge_text = f"กรณีศึกษาที่ {case['id']} / {case.get('total', 6)}"
    subtitle = case.get("title", "")

    with st.container(border=True):
        st.markdown(
            f"""
            <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 8px;">
                <span style="background-color: #FEF08A; border: 1.5px solid #18181B; border-radius: 6px; padding: 2px 10px; font-size: 13px; font-weight: 700; box-shadow: 1.5px 1.5px 0px #18181B;">{badge_text}</span>
                <span style="font-size: 13px; font-weight: 700; color: #4B5563;">{subtitle}</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

        if case.get("latex"):
            st.latex(case["latex"])

        if case.get("description"):
            st.markdown(case["description"])

        st.markdown(case.get("question", "**โปรดเลือกแนวทาง:**"))

        choice = st.radio(
            case.get("radio_label", "ตัวเลือก"),
            options=case["options"],
            index=None,
            key=case["radio_key"],
            label_visibility="collapsed",
        )

        p_choice = choice or ""
        if not p_choice:
            st.info("โปรดเลือกแนวทางด้านบนเพื่อตรวจสอบความเข้าใจและรับผลป้อนกลับ")
            return

        # Find matching feedback by option trigger
        fb = None
        for trigger, fb_item in case.get("feedbacks", {}).items():
            if trigger in p_choice:
                fb = fb_item
                break

        if fb is None:
            fb = case.get("default_feedback")

        if not fb:
            return

        fb_type = fb.get("type", "info")
        msg = fb.get("message", "")

        if fb_type == "success":
            st.success(msg)
            if fb.get("latex_ans"):
                st.markdown("##### ผลลัพธ์สุดท้าย")
                st.latex(fb["latex_ans"])
            if fb.get("worked_steps"):
                with st.container(border=True):
                    st.markdown("**วิธีทำทีละขั้นตอนอย่างละเอียด:**")
                    st.markdown(fb["worked_steps"])
        elif fb_type == "error":
            st.error(msg)
        elif fb_type == "warning":
            st.warning(msg)
        else:
            st.info(msg)
