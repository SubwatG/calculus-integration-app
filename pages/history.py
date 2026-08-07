import streamlit as st
from utils.theme import render_hero


render_hero("ประวัติที่ทำ", "บันทึกการเรียนและคะแนนในเซสชันนี้")

quiz_scores = st.session_state.get("quiz_scores", {})

if not quiz_scores:
    st.markdown("ยังไม่มีประวัติ — ทำแบบทดสอบในหน้าเกมทบทวนก่อน")
else:
    table_data = []
    topic_titles = {
        "basic_rules": "Basic Integration Rules Quiz",
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
