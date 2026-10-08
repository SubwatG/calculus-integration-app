import streamlit as st
from utils.math_render import format_math_spacing
from utils.quiz_engine import load_quiz
from utils.theme import render_hero

QUIZ_OPTIONS = {
    "[ทั้งหมด] ทำโจทย์ทั้งหมด (30 ข้อ)": "all",
    "[กฎพื้นฐาน] กฎพื้นฐานและทฤษฎีบท (10 ข้อ)": "basic_rules",
    "[รีมันน์] ผลบวกรีมันน์และการประมาณค่า (10 ข้อ)": "riemann",
    "[เทคนิค] เทคนิคการเปลี่ยนตัวแปร & By Parts (10 ข้อ)": "techniques",
}

render_hero("เกมทบทวนมโนทัศน์", "ตอบคำถามเพื่อสร้างความเข้าใจ พร้อมระบบคำแนะนำและสะสมคะแนน")

st.markdown("### เลือกชุดข้อสอบมโนทัศน์")
selected_topic_name = st.radio(
    "คลิกเลือกชุดข้อสอบที่ต้องการทำ:",
    list(QUIZ_OPTIONS.keys()),
    index=0,
    horizontal=True,
    key="quiz_topic_selector_main",
)
QUIZ_TOPIC = QUIZ_OPTIONS[selected_topic_name]


def get_quiz_questions(topic: str):
    if topic == "all":
        return load_quiz("basic_rules") + load_quiz("riemann") + load_quiz("techniques")
    return load_quiz(topic)


questions = get_quiz_questions(QUIZ_TOPIC)

if "quiz_q_index" not in st.session_state:
    st.session_state.quiz_q_index = 0
if "quiz_score" not in st.session_state:
    st.session_state.quiz_score = 0
if "quiz_user_answers" not in st.session_state:
    st.session_state.quiz_user_answers = {}
if "quiz_revealed" not in st.session_state:
    st.session_state.quiz_revealed = False
if "quiz_show_hint" not in st.session_state:
    st.session_state.quiz_show_hint = False
if "quiz_done" not in st.session_state:
    st.session_state.quiz_done = False
if "quiz_current_choice" not in st.session_state:
    st.session_state.quiz_current_choice = None
if "quiz_attempt_count" not in st.session_state:
    st.session_state.quiz_attempt_count = 0

# self-contained init
if "quiz_scores" not in st.session_state:
    st.session_state.quiz_scores = {}
if "quiz_answers" not in st.session_state:
    st.session_state.quiz_answers = {}
if "quiz_submitted" not in st.session_state:
    st.session_state.quiz_submitted = False


def reset_quiz() -> None:
    st.session_state.quiz_q_index = 0
    st.session_state.quiz_score = 0
    st.session_state.quiz_user_answers = {}
    st.session_state.quiz_revealed = False
    st.session_state.quiz_show_hint = False
    st.session_state.quiz_done = False
    st.session_state.quiz_current_choice = None
    st.session_state.quiz_attempt_count = 0


if (
    st.session_state.get("quiz_active_topic") != QUIZ_TOPIC
    or st.session_state.get("quiz_total_count") != len(questions)
):
    st.session_state.quiz_active_topic = QUIZ_TOPIC
    st.session_state.quiz_total_count = len(questions)
    reset_quiz()


if st.session_state.quiz_done:
    final_score = st.session_state.quiz_score
    total_q = len(questions)
    percentage = (final_score / total_q * 100) if total_q > 0 else 0

    st.markdown("### สรุปผลการทดสอบ")
    col_sc1, col_sc2 = st.columns(2)
    with col_sc1:
        st.metric("คะแนนสะสมของคุณ", f"{final_score} / {total_q}")
    with col_sc2:
        st.metric("คิดเป็นร้อยละ", f"{percentage:.1f}%")

    st.progress(final_score / total_q if total_q > 0 else 0)

    if percentage >= 80:
        st.success("ผลการประเมิน: ระดับดีมาก มีความเข้าใจมโนทัศน์แคลคูลัสอย่างแม่นยำ")
    elif percentage >= 50:
        st.info("ผลการประเมิน: ระดับผ่านเกณฑ์ มีความเข้าใจพื้นฐานที่ดี สามารถทบทวนเพิ่มเติมในหัวข้อที่ตอบผิดได้จากหน้าบทเรียน")
    else:
        st.warning("ผลการประเมิน: ควรทบทวนเพิ่มเติม แนะนำให้ใช้เครื่องมือจำลองในหน้ารีมันน์และการแทนค่าตัวแปรเพื่อสร้างมโนทัศน์")

    st.divider()
    st.markdown("### สรุปคำตอบและคำอธิบายรายข้อ")

    saved_answers = st.session_state.quiz_user_answers
    for idx, q in enumerate(questions):
        user_ans = saved_answers.get(idx, "ไม่ได้ตอบ")
        is_correct = user_ans == q["answer"]
        status_symbol = "✓ ถูกต้อง" if is_correct else "✗ ยังไม่ถูก"

        with st.expander(f"ข้อ {idx + 1}: {status_symbol}", expanded=False):
            st.markdown(f"**คำถาม:** {format_math_spacing(q['question'])}")
            st.markdown(f"**คำตอบของคุณ:** {format_math_spacing(user_ans)}")
            st.markdown(f"**คำตอบที่ถูกต้อง:** {format_math_spacing(q['answer'])}")
            st.markdown(f"**คำอธิบาย:** {format_math_spacing(q['explanation'])}")

    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        if st.button("ทำแบบทดสอบอีกครั้ง", key="btn_quiz_restart", use_container_width=True):
            reset_quiz()
            st.rerun()
    with col_btn2:
        if st.button("กลับสู่หน้าหลัก", key="btn_quiz_home", use_container_width=True):
            st.switch_page("pages/home.py")
else:
    q_idx = st.session_state.quiz_q_index
    if q_idx >= len(questions):
        st.session_state.quiz_done = True
        st.session_state.quiz_scores[QUIZ_TOPIC] = {
            "score": st.session_state.quiz_score,
            "total": len(questions),
        }
        st.session_state.quiz_answers[QUIZ_TOPIC] = st.session_state.quiz_user_answers
        st.session_state.quiz_submitted = True
        st.rerun()
    else:
        q = questions[q_idx]
        choice_prefixes = ["A", "B", "C", "D"]
        revealed = st.session_state.quiz_revealed
        show_hint = st.session_state.quiz_show_hint
        current_choice = st.session_state.quiz_current_choice

        col_h1, col_h2 = st.columns([2, 1])
        with col_h1:
            st.markdown(f"### ข้อที่ {q_idx + 1} / {len(questions)}")
        with col_h2:
            st.markdown(f"**คะแนนสะสม:** {st.session_state.quiz_score}")

        st.progress((q_idx + 1) / len(questions))

        st.markdown(f"**คำถาม:**\n\n{format_math_spacing(q['question'])}")
        st.divider()

        correct_idx = q["choices"].index(q["answer"]) if q["answer"] in q["choices"] else 0
        correct_prefix = choice_prefixes[correct_idx]

        if not revealed:
            if show_hint:
                st.warning(
                    f"**[คำแนะนำ / แนวคิดสำหรับทดลอง]:**\n\n"
                    f"{format_math_spacing(q.get('hint', 'ลองพิจารณาสูตรและนิยามอีกครั้ง'))}\n\n"
                    f"*สามารถสลับไปทดลองในเครื่องคำนวณหรือตัวจำลองกราฟในแอปเพื่อหาคำตอบได้*"
                )

            selected_idx = st.radio(
                "เลือกคำตอบที่ถูกต้อง:",
                options=list(range(len(q["choices"]))),
                format_func=lambda i: f"**{choice_prefixes[i]}.** {format_math_spacing(q['choices'][i])}",
                index=None,
                key=f"radio_choice_{q_idx}_{st.session_state.quiz_attempt_count}",
            )

            st.write("")
            col_act1, col_act2 = st.columns([1, 1])
            with col_act1:
                can_submit = selected_idx is not None
                if st.button(
                    "ตรวจคำตอบ",
                    type="primary",
                    disabled=not can_submit,
                    use_container_width=True,
                    key=f"btn_submit_{q_idx}",
                ):
                    chosen = q["choices"][selected_idx]
                    st.session_state.quiz_current_choice = chosen
                    st.session_state.quiz_user_answers[q_idx] = chosen

                    if chosen == q["answer"]:
                        st.session_state.quiz_score += 1
                        st.session_state.quiz_revealed = True
                        st.session_state.quiz_show_hint = False
                    else:
                        if not show_hint:
                            st.session_state.quiz_show_hint = True
                            st.session_state.quiz_revealed = False
                            st.session_state.quiz_attempt_count += 1
                        else:
                            st.session_state.quiz_revealed = True
                            st.session_state.quiz_show_hint = False
                    st.rerun()

            with col_act2:
                if show_hint:
                    if st.button(
                        "ขอดูเฉลยและวิธีทำ",
                        use_container_width=True,
                        key=f"btn_force_reveal_{q_idx}",
                    ):
                        st.session_state.quiz_revealed = True
                        st.session_state.quiz_show_hint = False
                        st.rerun()

        else:
            if current_choice == q["answer"]:
                st.success("✓ **ถูกต้อง!** ได้รับ 1 คะแนน")
            else:
                st.error(f"✗ **ยังไม่ถูกต้อง** (คำตอบที่ถูกต้องคือ: ข้อ **{correct_prefix}**)")

            st.markdown("##### ตัวเลือกทั้งหมด:")
            for i, choice_text in enumerate(q["choices"]):
                prefix = choice_prefixes[i]
                formatted = format_math_spacing(choice_text)
                if choice_text == q["answer"]:
                    st.markdown(f"- **[{prefix}]** {formatted} &nbsp; **(✓ คำตอบที่ถูกต้อง)**")
                elif choice_text == current_choice:
                    st.markdown(f"- **[{prefix}]** {formatted} &nbsp; *(✗ คำตอบที่คุณเลือก)*")
                else:
                    st.markdown(f"- **[{prefix}]** {formatted}")

            st.info(f"**[คำอธิบายอย่างละเอียด]**\n\n{format_math_spacing(q['explanation'])}")

            if st.button("ข้อถัดไป →", type="primary", use_container_width=True, key=f"btn_next_q_{q_idx}"):
                if q_idx + 1 < len(questions):
                    st.session_state.quiz_q_index += 1
                    st.session_state.quiz_revealed = False
                    st.session_state.quiz_show_hint = False
                    st.session_state.quiz_current_choice = None
                    st.session_state.quiz_attempt_count = 0
                else:
                    st.session_state.quiz_done = True
                    st.session_state.quiz_scores[QUIZ_TOPIC] = {
                        "score": st.session_state.quiz_score,
                        "total": len(questions),
                    }
                    st.session_state.quiz_answers[QUIZ_TOPIC] = (
                        st.session_state.quiz_user_answers
                    )
                    st.session_state.quiz_submitted = True
                st.rerun()
