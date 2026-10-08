from pathlib import Path
import streamlit as st
from utils.theme import render_hero

render_hero("แบบประเมินความพึงพอใจ", "การประเมินการใช้งานเว็บแอปพลิเคชันช่วยสอนแคลคูลัส (SUS)")

st.markdown(
    """
    ขอความอนุเคราะห์ผู้เรียนและผู้ร่วมทดลองใช้งานทุกท่าน ร่วมตอบแบบประเมินเพื่อนำข้อมูลไปวิเคราะห์
    และพัฒนาปรับปรุงเว็บแอปพลิเคชันช่วยสอนแคลคูลัสฉบับนี้ โดยข้อมูลทั้งหมดเป็นแบบ **นิรนาม (Anonymous)** 
    และประมวลผลในภาพรวมทางสถิติเท่านั้น
    """
)

col1, col2 = st.columns([1, 1])

with col1:
    st.markdown("### สแกน QR Code ผ่านสมาร์ตโฟน")
    qr_path = Path(__file__).resolve().parent.parent / "docs" / "calculus-survey-qr.png"
    if qr_path.exists():
        st.image(str(qr_path), width=280, caption="สแกนเพื่อเปิดแบบสอบถามบนโทรศัพท์มือถือ")

with col2:
    st.markdown("### หรือเปิดทำแบบสอบถามบนเบราว์เซอร์")
    st.info("แบบสอบถามประกอบด้วย 4 ตอน ใช้เวลาทำประมาณ 3-5 นาที")
    st.link_button(
        "เปิดทำแบบสอบถามออนไลน์ (Google Forms)",
        url="https://docs.google.com/forms/d/e/1FAIpQLSeKgS8Wl1phirB6tJuJMNM4SP8y_4k6v5xSQy_NkkM57Nxvzg/viewform",
        type="primary",
        use_container_width=True,
    )
    st.markdown(
        """
        **โครงสร้างแบบประเมิน:**
        - **ตอนที่ 1:** ข้อมูลทั่วไปและภูมิหลังทางการศึกษา (กลุ่มโรงเรียน/มหาวิทยาลัย และประสบการณ์แคลคูลัส)
        - **ตอนที่ 2:** การประเมินความพึงพอใจต่อคุณลักษณะของระบบ (มาตรประมาณค่า 5 ระดับ ครอบคลุม 4 ด้าน)
        - **ตอนที่ 3:** แบบประเมินความสะดวกในการใช้งานตามมาตรฐานสากล (System Usability Scale: SUS 10 ข้อ)
        - **ตอนที่ 4:** ข้อเสนอแนะและความคิดเห็นเพิ่มเติมเพื่อการพัฒนาระบบ
        """
    )
