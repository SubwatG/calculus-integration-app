import random
from typing import Any
import streamlit as st
from utils.math_render import format_math_spacing
from utils.quiz_engine import load_quiz
from utils.theme import inject_css, render_hero

ALL_TOPIC_KEYS = [
    "tangent",
    "limits",
    "basic_rules",
    "riemann",
    "techniques",
    "area_between",
    "improper_integrals",
    "volume_revolution",
]

QUIZ_OPTIONS = {
    "[ทั้งหมด] ทำโจทย์ทุกบท (80 ข้อ)": "all",
    "[เส้นสัมผัส] 1. เส้นสัมผัสและอนุพันธ์ (10 ข้อ)": "tangent",
    "[ลิมิต] 2. ลิมิตและความต่อเนื่อง (10 ข้อ)": "limits",
    "[กฎพื้นฐาน] 3. กฎพื้นฐานและทฤษฎีบท (10 ข้อ)": "basic_rules",
    "[รีมันน์] 4. ผลรวมรีมันน์และการประมาณค่า (10 ข้อ)": "riemann",
    "[เทคนิค] 5. เทคนิคการเปลี่ยนตัวแปร & By Parts (10 ข้อ)": "techniques",
    "[พื้นที่ระหว่างเส้น] 6. พื้นที่ระหว่างเส้นโค้ง (10 ข้อ)": "area_between",
    "[ปริพันธ์ไม่ตรงแบบ] 7. ปริพันธ์ไม่ตรงแบบ (10 ข้อ)": "improper_integrals",
    "[ปริมาตรรูปทรงตัน] 8. ปริมาตรของรูปทรงตันจากการหมุน (10 ข้อ)": "volume_revolution",
}

TOPIC_LABELS = {
    "all": "รวมโจทย์มโนทัศน์ทุกบท",
    "tangent": "1. เส้นสัมผัสและอนุพันธ์",
    "limits": "2. ลิมิตและความต่อเนื่อง",
    "basic_rules": "3. กฎพื้นฐานและทฤษฎีบท",
    "riemann": "4. ผลรวมรีมันน์และการประมาณค่า",
    "techniques": "5. เทคนิคการเปลี่ยนตัวแปร & By Parts",
    "area_between": "6. พื้นที่ระหว่างเส้นโค้ง",
    "improper_integrals": "7. ปริพันธ์ไม่ตรงแบบ",
    "volume_revolution": "8. ปริมาตรของรูปทรงตันจากการหมุน",
}

inject_css()

# Custom Bauhaus styling for Quiz components
st.markdown(
    """
    <style>
    /* Radio options styled as tactile Bauhaus cards */
    div[data-testid="stRadio"] div[role="radiogroup"]:not([aria-orientation="horizontal"]) {
        display: flex !important;
        flex-direction: column !important;
        gap: 12px !important;
        margin-top: 10px !important;
        margin-bottom: 16px !important;
    }
    div[data-testid="stRadio"] div[role="radiogroup"]:not([aria-orientation="horizontal"]) > label {
        background-color: #FFFFFF !important;
        border: 2.5px solid #18181B !important;
        border-radius: 14px !important;
        box-shadow: 3.5px 3.5px 0px #18181B !important;
        padding: 14px 18px !important;
        margin: 0 !important;
        cursor: pointer !important;
        transition: all 0.12s ease-out !important;
        width: 100% !important;
        display: flex !important;
        align-items: center !important;
    }
    div[data-testid="stRadio"] div[role="radiogroup"]:not([aria-orientation="horizontal"]) > label:hover {
        background-color: #FEF08A !important;
        transform: translate(-1.5px, -1.5px) !important;
        box-shadow: 5px 5px 0px #18181B !important;
    }
    div[data-testid="stRadio"] div[role="radiogroup"]:not([aria-orientation="horizontal"]) > label:has(input:checked) {
        background-color: #FEF9C3 !important;
        border: 2.5px solid #18181B !important;
        box-shadow: 4px 4px 0px #18181B !important;
    }
    div[data-testid="stRadio"] div[role="radiogroup"]:not([aria-orientation="horizontal"]) > label p {
        font-family: "Mali", "Outfit", sans-serif !important;
        font-size: 1.05rem !important;
        font-weight: 600 !important;
        line-height: 1.5 !important;
        margin: 0 !important;
        color: #18181B !important;
    }
    /* Horizontal radio badges for Topic Selector */
    div[data-testid="stRadio"] div[role="radiogroup"][aria-orientation="horizontal"] {
        gap: 10px !important;
        flex-wrap: wrap !important;
    }
    div[data-testid="stRadio"] div[role="radiogroup"][aria-orientation="horizontal"] > label {
        background-color: #FFFFFF !important;
        border: 2px solid #18181B !important;
        border-radius: 999px !important;
        padding: 6px 16px !important;
        box-shadow: 2px 2px 0px #18181B !important;
        transition: all 0.12s ease-out !important;
    }
    div[data-testid="stRadio"] div[role="radiogroup"][aria-orientation="horizontal"] > label:hover {
        background-color: #FEF08A !important;
        transform: translate(-1px, -1px) !important;
        box-shadow: 3px 3px 0px #18181B !important;
    }
    div[data-testid="stRadio"] div[role="radiogroup"][aria-orientation="horizontal"] > label:has(input:checked) {
        background-color: #BAE6FD !important;
        font-weight: 700 !important;
        box-shadow: 3px 3px 0px #18181B !important;
    }
    /* Question Bauhaus Card with solid background and tactile frame */
    div.st-key-quiz_question_box,
    div[data-testid="stVerticalBlock"].st-key-quiz_question_box {
        background-color: #FFFFFF !important;
        border: 2.5px solid #18181B !important;
        border-radius: 16px !important;
        box-shadow: 4px 4px 0px #18181B !important;
        padding: 1.25rem 1.5rem !important;
        margin-top: 8px !important;
        margin-bottom: 16px !important;
    }
    div.st-key-quiz_question_box p,
    div[data-testid="stVerticalBlock"].st-key-quiz_question_box p {
        font-family: "Mali", "Outfit", sans-serif !important;
        font-size: 1.12rem !important;
        font-weight: 600 !important;
        line-height: 1.6 !important;
        color: #18181B !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

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

col_topic_info, col_topic_btn = st.columns([3, 1])
with col_topic_info:
    st.caption("🎲 ระบบสุ่มลำดับตัวเลือก (A, B, C, D) และสุ่มลำดับโจทย์แบบไดนามิกทุกรอบ เพื่อฝึกมโนทัศน์แท้จริง")
with col_topic_btn:
    if st.button("🎲 สุ่มรอบใหม่", key="btn_reshuffle_now", use_container_width=True):
        init_quiz_session(QUIZ_TOPIC)
        st.rerun()


def get_quiz_questions(topic: str) -> list[dict[str, Any]]:
    if topic == "all":
        all_q = []
        for key in ALL_TOPIC_KEYS:
            all_q.extend(load_quiz(key))
        return all_q
    return load_quiz(topic)


def prepare_shuffled_questions(
    raw_questions: list[dict[str, Any]], shuffle_q_order: bool = True
) -> list[dict[str, Any]]:
    """Shuffle choices for each question so the correct answer is randomly distributed across A, B, C, D,
    and optionally shuffle question order."""
    prepared = []
    for q in raw_questions:
        q_copy = dict(q)
        choices = list(q["choices"])
        random.shuffle(choices)
        q_copy["choices"] = choices
        prepared.append(q_copy)
    if shuffle_q_order:
        random.shuffle(prepared)
    return prepared


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


def init_quiz_session(topic: str) -> None:
    raw = get_quiz_questions(topic)
    st.session_state.quiz_questions = prepare_shuffled_questions(raw, shuffle_q_order=True)
    st.session_state.quiz_active_topic = topic
    st.session_state.quiz_total_count = len(st.session_state.quiz_questions)
    reset_quiz()


if (
    "quiz_questions" not in st.session_state
    or st.session_state.get("quiz_active_topic") != QUIZ_TOPIC
):
    init_quiz_session(QUIZ_TOPIC)

questions = st.session_state.quiz_questions


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
            st.markdown(f"**คำถาม:**\n\n{format_math_spacing(q['question'])}")
            st.markdown(f"**คำตอบของคุณ:** {format_math_spacing(user_ans)}")
            st.markdown(f"**คำตอบที่ถูกต้อง:** {format_math_spacing(q['answer'])}")
            st.info(f"**คำอธิบาย:**\n\n{format_math_spacing(q['explanation'])}")

    st.write("")
    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        if st.button("ทำแบบทดสอบอีกครั้ง (สุ่มตัวเลือกใหม่)", key="btn_quiz_restart", use_container_width=True):
            init_quiz_session(QUIZ_TOPIC)
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
        topic_name = TOPIC_LABELS.get(QUIZ_TOPIC, "มโนทัศน์")

        # Top Bauhaus Status Header
        st.markdown(
            f"""
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px; flex-wrap: wrap; gap: 8px;">
                <div style="display: inline-flex; align-items: center; gap: 8px;">
                    <span style="background-color: #FEF08A; border: 2px solid #18181B; border-radius: 999px; padding: 4px 14px; font-weight: 700; font-size: 14px; font-family: 'Mali', 'Outfit', sans-serif; box-shadow: 2px 2px 0px #18181B;">
                        ข้อที่ {q_idx + 1} / {len(questions)}
                    </span>
                    <span style="background-color: #E0E7FF; border: 2px solid #18181B; border-radius: 999px; padding: 4px 14px; font-weight: 600; font-size: 13px; font-family: 'Mali', 'Outfit', sans-serif; box-shadow: 2px 2px 0px #18181B;">
                        {topic_name}
                    </span>
                </div>
                <span style="background-color: #BAE6FD; border: 2px solid #18181B; border-radius: 999px; padding: 4px 14px; font-weight: 700; font-size: 14px; font-family: 'Mali', 'Outfit', sans-serif; box-shadow: 2px 2px 0px #18181B; display: inline-flex; align-items: center;">
                    คะแนนสะสม: {st.session_state.quiz_score} คะแนน
                </span>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.progress((q_idx + 1) / len(questions))

        # Question Bauhaus Card
        with st.container(border=True, key="quiz_question_box"):
            st.markdown(
                f"""
                <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 10px; border-bottom: 2px dashed #E4E4E7; padding-bottom: 8px;">
                    <div style="display: inline-flex; align-items: center; gap: 8px;">
                        <span style="background-color: #F43F5E; color: #FFFFFF; border: 1.5px solid #18181B; border-radius: 6px; padding: 2px 8px; font-size: 12px; font-weight: 800; box-shadow: 1.5px 1.5px 0px #18181B;">✦ โจทย์มโนทัศน์</span>
                        <span style="font-size: 13px; font-weight: 700; color: #4B5563;">คำถามข้อที่ {q_idx + 1}</span>
                    </div>
                    <span style="font-size: 12px; font-weight: 700; color: #71717A; background-color: #F4F4F5; border: 1.5px solid #18181B; border-radius: 6px; padding: 2px 8px;">
                        1 คะแนน
                    </span>
                </div>
                """,
                unsafe_allow_html=True,
            )
            st.markdown(f"**{format_math_spacing(q['question'])}**")

        correct_idx = q["choices"].index(q["answer"]) if q["answer"] in q["choices"] else 0
        correct_prefix = choice_prefixes[correct_idx]

        if not revealed:
            if show_hint:
                st.warning(
                    f"**[คำแนะนำ / แนวคิดสำหรับทดลอง]:**\n\n"
                    f"{format_math_spacing(q.get('hint', 'ลองพิจารณาสูตรและนิยามอีกครั้ง'))}\n\n"
                    f"*สามารถสลับไปทดลองในเครื่องคิดเลข SymPy หรือตัวจำลองกราฟในแอปเพื่อหาคำตอบได้*"
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
                st.success("✓ **ถูกต้องยอดเยี่ยม!** ได้รับ 1 คะแนน")
            else:
                st.error(f"✗ **ยังไม่ถูกต้อง** (คำตอบที่ถูกต้องคือ: ข้อ **{correct_prefix}**)")

            st.markdown("##### ตัวเลือกทั้งหมด:")
            for i, choice_text in enumerate(q["choices"]):
                prefix = choice_prefixes[i]
                formatted = format_math_spacing(choice_text)
                if choice_text == q["answer"]:
                    st.success(f"**[{prefix}]** {formatted} &nbsp; *(✓ คำตอบที่ถูกต้อง)*")
                elif choice_text == current_choice:
                    st.error(f"**[{prefix}]** {formatted} &nbsp; *(✗ คำตอบที่คุณเลือก)*")
                else:
                    st.markdown(f"- **[{prefix}]** {formatted}")

            st.info(f"**[คำอธิบายอย่างละเอียด]**\n\n{format_math_spacing(q['explanation'])}")

            st.write("")
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
