import streamlit as st
from utils.theme import render_hero


render_hero("ประวัติที่ทำ", "บันทึกการเรียนและคะแนนในเซสชันนี้")

quiz_scores = st.session_state.get("quiz_scores", {})

if not quiz_scores:
    st.markdown("ยังไม่มีประวัติ — ทำแบบทดสอบในหน้าเกมทบทวนก่อน")
else:
    table_data = []
    topic_titles = {
        "all": "แบบทดสอบรวมทุกบท (80 ข้อ)",
        "tangent": "1. เส้นสัมผัสและอนุพันธ์",
        "limits": "2. ลิมิตและความต่อเนื่อง",
        "basic_rules": "3. กฎพื้นฐานและทฤษฎีบท",
        "riemann": "4. ผลรวมรีมันน์และการประมาณค่า",
        "techniques": "5. เทคนิคการเปลี่ยนตัวแปร & By Parts",
        "area_between": "6. พื้นที่ระหว่างเส้นโค้ง",
        "improper_integrals": "7. ปริพันธ์ไม่ตรงแบบ",
        "volume_revolution": "8. ปริมาตรของรูปทรงตันจากการหมุน",
    }

    for topic_key, result in quiz_scores.items():
        if isinstance(result, dict):
            s = result.get("score", 0)
            t = result.get("total", 1)
            pct = (s / t * 100) if t > 0 else 0
            title = topic_titles.get(topic_key, topic_key)
            table_data.append(
                {
                    "หัวข้อ": title,
                    "คะแนน": s,
                    "คะแนนเต็ม": t,
                    "คิดเป็น (%)": f"{pct:.1f}%",
                }
            )

    if table_data:
        st.table(table_data)
    else:
        st.markdown("ยังไม่มีประวัติ — ทำแบบทดสอบในหน้าเกมทบทวนก่อน")
