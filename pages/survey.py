from pathlib import Path
import streamlit as st
from utils.theme import render_hero

render_hero(
    "📝 แบบประเมินความพึงพอใจ (SUS) ✨",
    "✨ ร่วมประเมินการใช้งานเว็บแอปพลิเคชันช่วยสอนแคลคูลัส เพื่อการวิจัยและพัฒนาปรับปรุงอย่างต่อเนื่อง 💖",
)

st.markdown(
    """
    <style>
    .survey-banner {
        background: linear-gradient(135deg, #FEF08A 0%, #FED7AA 50%, #FECDD3 100%);
        border: 2.5px solid #18181B;
        border-radius: 14px;
        padding: 14px 18px;
        box-shadow: 4px 4px 0px #18181B;
        margin-bottom: 22px;
        font-family: 'Mali', sans-serif;
        font-size: 14px;
        color: #18181B;
        line-height: 1.6;
    }
    .survey-section-card {
        background: #FFFFFF;
        border: 2px solid #18181B;
        border-radius: 12px;
        padding: 12px 14px;
        box-shadow: 2.5px 2.5px 0px #18181B;
        margin-bottom: 8px;
        font-family: 'Mali', sans-serif;
        font-size: 13px;
        color: #374151;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="survey-banner">
        <b>🙏 ขอความอนุเคราะห์ผู้เรียนและผู้ร่วมทดลองใช้งานทุกท่าน:</b><br>
        ร่วมตอบแบบประเมินความพึงพอใจ เพื่อนำข้อมูลไปวิเคราะห์และพัฒนาปรับปรุงเว็บแอปพลิเคชันช่วยสอนแคลคูลัสฉบับนี้
        โดยข้อมูลทั้งหมดจะถูกเก็บเป็นแบบ <b>นิรนาม (Anonymous)</b> และนำไปประมวลผลทางสถิติเพื่อการศึกษาเท่านั้น 🌸
    </div>
    """,
    unsafe_allow_html=True,
)

col1, col2 = st.columns([1, 1])

with col1:
    st.markdown("### 📱 สแกน QR Code ผ่านสมาร์ตโฟน")
    qr_path = Path(__file__).resolve().parent.parent / "docs" / "calculus-survey-qr.png"
    if qr_path.exists():
        with st.container(border=True):
            st.image(str(qr_path), width=270, caption="📷 ใช้กล้องมือถือสแกนเพื่อเปิดแบบสอบถาม")

with col2:
    st.markdown("### 💻 หรือเปิดทำแบบสอบถามบนเบราว์เซอร์")
    st.info("⏱️ แบบสอบถามประกอบด้วย 4 ตอน ใช้เวลาทำประมาณ 3-5 นาทีเท่านั้น")
    st.link_button(
        "📝 เปิดทำแบบสอบถามออนไลน์ (Google Forms)",
        url="https://docs.google.com/forms/d/e/1FAIpQLSeKgS8Wl1phirB6tJuJMNM4SP8y_4k6v5xSQy_NkkM57Nxvzg/viewform",
        type="primary",
        use_container_width=True,
    )
    st.write("")
    st.markdown("#### 📋 โครงสร้างแบบประเมิน:")
    st.markdown(
        """
        <div class="survey-section-card" style="border-left: 6px solid #F43F5E;">
            <b>ตอนที่ 1: ข้อมูลทั่วไปและภูมิหลังทางการศึกษา 🎓</b><br>
            กลุ่มโรงเรียน/มหาวิทยาลัย และประสบการณ์การเรียนรู้แคลคูลัส
        </div>
        <div class="survey-section-card" style="border-left: 6px solid #F59E0B;">
            <b>ตอนที่ 2: ความพึงพอใจต่อคุณลักษณะของระบบ ⭐</b><br>
            มาตรวัดประมาณค่า 5 ระดับ ครอบคลุมด้านเนื้อหา, กราฟิก, ความถูกต้อง และการโต้ตอบ
        </div>
        <div class="survey-section-card" style="border-left: 6px solid #0284C7;">
            <b>ตอนที่ 3: ความสะดวกในการใช้งานตามมาตรฐานสากล (SUS) 📊</b><br>
            System Usability Scale 10 ข้อ เพื่อคำนวณคะแนนประสิทธิภาพของระบบ
        </div>
        <div class="survey-section-card" style="border-left: 6px solid #10B981;">
            <b>ตอนที่ 4: ข้อเสนอแนะและความคิดเห็นเพิ่มเติม 💬</b><br>
            เปิดรับไอเดียและข้อเสนอแนะเพื่อการต่อยอดโครงงานในอนาคต
        </div>
        """,
        unsafe_allow_html=True,
    )
