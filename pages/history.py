import streamlit as st
from utils.theme import render_hero

render_hero(
    "🏆 ประวัติคะแนนและการเรียนรู้ (Learning History) ✨",
    "📊 บันทึกผลคะแนนแบบทดสอบและสถิติการเรียนรู้ในเซสชันปัจจุบัน 🌟",
)

quiz_scores = st.session_state.get("quiz_scores", {})

if not quiz_scores:
    st.markdown(
        """
        <div style="background-color: #FFFFFF; border: 2.5px dashed #18181B; border-radius: 14px; padding: 24px; text-align: center; box-shadow: 4px 4px 0px #18181B; margin: 16px 0 24px 0;">
            <div style="font-size: 42px; margin-bottom: 8px;">💡</div>
            <h4 style="font-family: 'Fredoka', 'Mali', sans-serif; font-size: 1.15rem; color: #18181B; margin: 0 0 6px 0;">
                ยังไม่มีบันทึกคะแนนในเซสชันนี้
            </h4>
            <p style="font-family: 'Mali', sans-serif; font-size: 0.95rem; color: #4B5563; margin: 0 0 16px 0;">
                ไปลองฝึกทำแบบทดสอบมโนทัศน์ 80 ข้อ ครอบคลุม 8 บทเรียน พร้อมระบบคำใบ้และสุ่มตัวเลือกกันเลย!
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    if st.button("🎯 เริ่มทำแบบทดสอบมโนทัศน์", type="primary", use_container_width=True):
        st.switch_page("pages/quiz.py")
else:
    table_data = []
    topic_titles = {
        "all": "🌟 แบบทดสอบรวมทุกบท (80 ข้อ)",
        "tangent": "📈 1. เส้นสัมผัสและอนุพันธ์",
        "limits": "🎯 2. ลิมิตและความต่อเนื่อง",
        "basic_rules": "📐 3. กฎพื้นฐานและทฤษฎีบท",
        "riemann": "📊 4. ผลรวมรีมันน์และการประมาณค่า",
        "techniques": "🔄 5. เทคนิคการเปลี่ยนตัวแปร & By Parts",
        "area_between": "📉 6. พื้นที่ระหว่างเส้นโค้ง",
        "improper_integrals": "♾️ 7. ปริพันธ์ไม่ตรงแบบ",
        "volume_revolution": "🌀 8. ปริมาตรของรูปทรงตันจากการหมุน",
    }

    total_correct = 0
    total_questions = 0

    for topic_key, result in quiz_scores.items():
        if isinstance(result, dict):
            s = result.get("score", 0)
            t = result.get("total", 1)
            total_correct += s
            total_questions += t
            pct = (s / t * 100) if t > 0 else 0
            title = topic_titles.get(topic_key, topic_key)
            table_data.append(
                {
                    "หัวข้อแบบทดสอบ": title,
                    "คะแนนที่ได้": s,
                    "คะแนนเต็ม": t,
                    "คิดเป็นร้อยละ (%)": f"{pct:.1f}%",
                }
            )

    mcol1, mcol2, mcol3 = st.columns(3)
    with mcol1:
        st.metric("คะแนนสะสมรวม", f"{total_correct} / {total_questions}")
    with mcol2:
        overall_pct = (total_correct / total_questions * 100) if total_questions > 0 else 0
        st.metric("ความแม่นยำเฉลี่ย", f"{overall_pct:.1f}%")
    with mcol3:
        st.metric("จำนวนหมวดที่ทำแล้ว", f"{len(table_data)} หมวด")

    st.write("")
    if table_data:
        st.table(table_data)

    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        if st.button("💡 ทำแบบทดสอบเพิ่ม", type="primary", use_container_width=True):
            st.switch_page("pages/quiz.py")
    with col_btn2:
        if st.button("🏠 กลับสู่หน้าหลัก", use_container_width=True):
            st.switch_page("pages/home.py")
