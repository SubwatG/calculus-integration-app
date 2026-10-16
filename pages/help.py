import streamlit as st
from utils.theme import render_hero

render_hero(
    "📖 คู่มือการใช้งานและโครงงาน (User Guide) ✨",
    "💡 แนวทางการใช้งานเว็บแอปพลิเคชัน ไวยากรณ์คณิตศาสตร์ และข้อแนะนำในการเรียนรู้ 🚀",
)

st.markdown(
    """
    <style>
    .help-step-card {
        background: #FFFFFF;
        border: 2px solid #18181B;
        border-radius: 12px;
        padding: 14px 18px;
        box-shadow: 3px 3px 0px #18181B;
        margin-bottom: 12px;
        display: flex;
        align-items: flex-start;
        gap: 14px;
    }
    .help-step-num {
        width: 36px;
        height: 36px;
        border-radius: 50%;
        border: 2px solid #18181B;
        display: flex;
        align-items: center;
        justify-content: center;
        font-family: 'Fredoka', sans-serif;
        font-weight: 700;
        font-size: 16px;
        flex-shrink: 0;
        box-shadow: 2px 2px 0px #18181B;
    }
    .syntax-tag {
        display: inline-block;
        background-color: #FEF08A;
        border: 1.5px solid #18181B;
        border-radius: 8px;
        padding: 2px 8px;
        font-family: monospace;
        font-weight: 700;
        color: #18181B;
        box-shadow: 1.5px 1.5px 0px #18181B;
        margin: 2px 0;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown("### 🚀 ขั้นตอนการเริ่มต้นใช้งาน (Getting Started)")

st.markdown(
    """
    <div class="help-step-card">
        <div class="help-step-num" style="background-color: #FECDD3;">1</div>
        <div>
            <h4 style="font-family: 'Fredoka', 'Mali', sans-serif; font-size: 15px; margin: 0 0 4px 0; color: #18181B;">
                📚 เลือกโมดูลการเรียนรู้ที่สนใจ
            </h4>
            <p style="font-family: 'Mali', sans-serif; font-size: 13.5px; color: #4B5563; margin: 0; line-height: 1.5;">
                เข้าไปที่เมนูด้านซ้ายหรือหน้าหลัก เพื่อเลือกหัวข้อ เช่น ลิมิต, เส้นสัมผัส, รีมันน์ หรือ ปริมาตรทรงตัน
            </p>
        </div>
    </div>
    <div class="help-step-card">
        <div class="help-step-num" style="background-color: #FEF08A;">2</div>
        <div>
            <h4 style="font-family: 'Fredoka', 'Mali', sans-serif; font-size: 15px; margin: 0 0 4px 0; color: #18181B;">
                🎛️ โต้ตอบกับกราฟและจำลองมโนทัศน์
            </h4>
            <p style="font-family: 'Mali', sans-serif; font-size: 13.5px; color: #4B5563; margin: 0; line-height: 1.5;">
                ปรับเปลี่ยนค่าตัวแปรในแถบเลื่อน (Slider) เพื่อสังเกตการเคลื่อนที่ของจุด เส้นสัมผัส หรือแท่งรีมันน์แบบเรียลไทม์
            </p>
        </div>
    </div>
    <div class="help-step-card">
        <div class="help-step-num" style="background-color: #BAE6FD;">3</div>
        <div>
            <h4 style="font-family: 'Fredoka', 'Mali', sans-serif; font-size: 15px; margin: 0 0 4px 0; color: #18181B;">
                🧮 ทดลองแก้โจทย์ด้วยเครื่องคิดเลขสัญลักษณ์ SymPy
            </h4>
            <p style="font-family: 'Mali', sans-serif; font-size: 13.5px; color: #4B5563; margin: 0; line-height: 1.5;">
                ป้อนฟังก์ชันทางคณิตศาสตร์เพื่อดูขั้นตอนการคำนวณทีละขั้นตอนอย่างละเอียด
            </p>
        </div>
    </div>
    <div class="help-step-card">
        <div class="help-step-num" style="background-color: #BBF7D0;">4</div>
        <div>
            <h4 style="font-family: 'Fredoka', 'Mali', sans-serif; font-size: 15px; margin: 0 0 4px 0; color: #18181B;">
                💡 ทดสอบความเข้าใจด้วยแบบทดสอบ 80 ข้อ
            </h4>
            <p style="font-family: 'Mali', sans-serif; font-size: 13.5px; color: #4B5563; margin: 0; line-height: 1.5;">
                ฝึกตอบคำถามมโนทัศน์ หากติดขัดสามารถกดดูคำใบ้ทีละระดับเพื่อช่วยนำทางกระบวนการคิด
            </p>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.divider()

st.markdown("### ⌨️ รูปแบบการใส่โจทย์ (SymPy Syntax Guide)")

col_syn1, col_syn2 = st.columns(2)

with col_syn1:
    with st.container(border=True):
        st.markdown("#### 📐 พหุนามและเลขยกกำลัง")
        st.markdown(
            """
            * <span class="syntax-tag">x**2</span> แทน $x^2$
            * <span class="syntax-tag">x**3 + 2*x - 5</span> แทน $x^3 + 2x - 5$
            * <span class="syntax-tag">sqrt(x)</span> แทน $\\sqrt{x}$
            * <span class="syntax-tag">(x**2 - 4)/(x - 2)</span> แทนเศษส่วน $\\frac{x^2 - 4}{x - 2}$
            """,
            unsafe_allow_html=True,
        )

with col_syn2:
    with st.container(border=True):
        st.markdown("#### 🌊 ฟังก์ชันอดิศัย (Trigonometric & Exp)")
        st.markdown(
            """
            * <span class="syntax-tag">sin(x)</span>, <span class="syntax-tag">cos(x)</span>, <span class="syntax-tag">tan(x)</span>
            * <span class="syntax-tag">exp(x)</span> แทน $e^x$
            * <span class="syntax-tag">log(x)</span> แทน $\\ln(x)$ (ลอการิทึมธรรมชาติ)
            * <span class="syntax-tag">abs(x)</span> แทน $|x|$ (ค่าสัมบูรณ์)
            """,
            unsafe_allow_html=True,
        )

st.divider()

st.markdown("### ℹ️ ข้อแนะนำและข้อจำกัดของระบบ (System Notes)")

with st.container(border=True):
    st.markdown(
        """
        * **เครื่องมือคำนวณ SymPy:** รองรับฟังก์ชันพื้นฐานส่วนใหญ่ในระดับแคลคูลัส 1 และ 2 โดยเน้นการแสดงขั้นตอนกฎกำลัง กฎผลคูณ/ผลหาร และการเปลี่ยนตัวแปร
        * **การบันทึกประวัติ:** ผลคะแนนจะบันทึกอยู่ในเซสชันปัจจุบัน (Session State) ในเบราว์เซอร์ หากรีเฟรชหน้าต่างใหม่ข้อมูลจะเริ่มใหม่เพื่อความเป็นส่วนตัว
        * **การแสดงผลสมการ:** ใช้เอนจิน KaTeX เพื่อความคมชัด ถูกต้อง และสวยงามตามมาตรฐานสากล
        """
    )
