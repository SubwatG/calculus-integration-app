"""utils/keypad.py — แผงปุ่มลัดสัญลักษณ์คณิตศาสตร์ (Math Keypad)

คอมโพเนนต์ปุ่มลัดสำหรับพิมพ์สูตรคณิตศาสตร์ใน Streamlit
ใช้ร่วมกันระหว่าง pages/solver.py, pages/limit_approach.py และโมดูลอื่นๆ
"""

import streamlit as st


def render_math_keypad(
    target_key: str,
    key_prefix: str = "kp",
    expanded: bool = False,
    include_infinity: bool = True,
    title: str = "แผงปุ่มลัดสัญลักษณ์คณิตศาสตร์ (Math Keypad)",
) -> None:
    """แสดงแผงปุ่มลัดสำหรับพิมพ์นิพจน์คณิตศาสตร์ลงใน st.session_state[target_key]"""

    def _append(tok: str) -> None:
        curr = st.session_state.get(target_key, "")
        if tok == "CLEAR":
            st.session_state[target_key] = ""
        elif tok == "BACKSPACE":
            st.session_state[target_key] = curr[:-1] if curr else ""
        elif tok == "^2":
            if curr and (curr[-1].isalnum() or curr[-1] in ")_"):
                st.session_state[target_key] = curr + "^2"
            else:
                st.session_state[target_key] = curr + "x^2" if curr else "x^2"
        else:
            st.session_state[target_key] = curr + tok if curr else tok

    with st.expander(title, expanded=expanded):
        st.caption("ตัวแปรและตัวดำเนินการ:")
        r1_cols = st.columns(10)
        row1_tokens = [
            ("x", "x"),
            ("t", "t"),
            ("y", "y"),
            ("+", " + "),
            ("-", " - "),
            ("×", " * "),
            ("÷", " / "),
            ("x²", "^2"),
            ("(", "("),
            (")", ")"),
        ]
        for idx, (lbl, tok) in enumerate(row1_tokens):
            with r1_cols[idx]:
                st.button(
                    lbl,
                    key=f"{key_prefix}_r1_{idx}",
                    use_container_width=True,
                    on_click=_append,
                    args=(tok,),
                )

        st.caption("ฟังก์ชันและค่าคงที่:")
        n_cols_r2 = 9 if include_infinity else 8
        r2_cols = st.columns(n_cols_r2)
        row2_tokens = [
            ("√", "sqrt("),
            ("π", "pi"),
            ("e", "e"),
            ("ln", "ln("),
            ("sin", "sin("),
            ("cos", "cos("),
            ("tan", "tan("),
            ("exp", "exp("),
        ]
        if include_infinity:
            row2_tokens.append(("∞", "inf"))

        for idx, (lbl, tok) in enumerate(row2_tokens):
            with r2_cols[idx]:
                st.button(
                    lbl,
                    key=f"{key_prefix}_r2_{idx}",
                    use_container_width=True,
                    on_click=_append,
                    args=(tok,),
                )

        st.caption("นิพจน์เพิ่มเติมและแก้ไข:")
        r3_cols = st.columns(4)
        row3_tokens = [
            ("1/x", "1/x"),
            ("|x|", "abs("),
            ("ลบตัวสุดท้าย", "BACKSPACE"),
            ("ล้างทั้งหมด", "CLEAR"),
        ]
        for idx, (lbl, tok) in enumerate(row3_tokens):
            with r3_cols[idx]:
                st.button(
                    lbl,
                    key=f"{key_prefix}_r3_{idx}",
                    use_container_width=True,
                    on_click=_append,
                    args=(tok,),
                )
