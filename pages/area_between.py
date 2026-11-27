"""pages/area_between.py : บทเรียน interactive: พื้นที่ระหว่างเส้นโค้ง (Area Between Curves)

คำนวณพื้นที่ปิดล้อมระหว่างสองฟังก์ชัน f(x) และ g(x) พร้อมวิเคราะห์จุดตัด แรเงากราฟแบบตอบสนอง และแสดงขั้นตอนวิธีทำ
"""

import streamlit as st

from utils.area_solver import compute_area_between, find_curve_intersections
from utils.math_render import preview_math_expr, render_latex, render_syntax_guide, render_steps
from utils.plotter import plot_area_between, plot_area_between_plotly
from utils.theme import inject_css, render_hero
from utils.theory import THEORY_CONTENT

inject_css()
render_hero("พื้นที่ระหว่างเส้นโค้ง", "วิเคราะห์จุดตัดและคำนวณพื้นที่ระหว่างเส้นโค้งสองเส้น")

if "area_f" not in st.session_state:
    st.session_state["area_f"] = "x"
if "area_g" not in st.session_state:
    st.session_state["area_g"] = "x**2"
if "area_a" not in st.session_state:
    st.session_state["area_a"] = 0.0
if "area_b" not in st.session_state:
    st.session_state["area_b"] = 1.0

theory = THEORY_CONTENT["area_between"]

# ---------------------------------------------------------------------------
# Concept Anchor & What to Observe
# ---------------------------------------------------------------------------
with st.container(border=True):
    col_badge, col_concept = st.columns([1, 4])
    with col_badge:
        st.markdown(
            """<span style="
                background-color: #FEF08A;
                border: 1.5px solid #18181B;
                border-radius: 8px;
                padding: 4px 10px;
                font-family: 'Fredoka', 'Mali', sans-serif;
                font-size: 13px;
                font-weight: 700;
                color: #18181B;
                display: inline-block;
            ">หลักการสำคัญ</span>""",
            unsafe_allow_html=True,
        )
    with col_concept:
        st.markdown("#### พื้นที่ระหว่างเส้นโค้งสองเส้น")

    st.latex(r"A = \int_a^b [f(x) - g(x)]\,dx \quad \left(\text{โดยที่ } f(x) \ge g(x) \text{ บนช่วง } [a, b]\right)")

    st.markdown(
        r"""
| ขั้นตอน | การดำเนินการ | สิ่งที่ต้องสังเกต |
| :---: | :--- | :--- |
| 1. หาจุดตัด | แก้สมการ $f(x) = g(x)$ | เป็นขอบเขตธรรมชาติ หากสลับบนล่างต้องแบ่งช่วงย่อย |
| 2. เส้นบน ลบ เส้นล่าง | ตรวจสอบ $f(x) \ge g(x)$ | ฟังก์ชันที่อยู่สูงกว่า ลบด้วยฟังก์ชันล่าง เพื่อให้พื้นที่เป็นบวกเสมอ |
| 3. คำนวณปริพันธ์ | หา $\int_a^b [f(x) - g(x)]\,dx$ | ได้ขนาดพื้นที่จริงที่ปิดล้อมระหว่างสองเส้นโค้ง |
        """
    )

st.divider()
st.markdown("### ลองคำนวณ")

st.markdown("**ตัวอย่างโจทย์:**")


def _set_area_preset(f_val: str, g_val: str, a_val: float, b_val: float) -> None:
    st.session_state["area_f"] = f_val
    st.session_state["area_g"] = g_val
    st.session_state["area_a"] = a_val
    st.session_state["area_b"] = b_val


def _apply_bounds(a_target: float, b_target: float) -> None:
    st.session_state["area_a"] = float(a_target)
    st.session_state["area_b"] = float(b_target)


p_cols = st.columns(4)
with p_cols[0]:
    st.button("$x$ และ $x^2$", key="pre_area_1", use_container_width=True, on_click=_set_area_preset, args=("x", "x**2", 0.0, 1.0))
with p_cols[1]:
    st.button("$2 - x^2$ และ $x^2$", key="pre_area_2", use_container_width=True, on_click=_set_area_preset, args=("2 - x**2", "x**2", -1.0, 1.0))
with p_cols[2]:
    st.button(r"$\cos(x)$ และ $x$", key="pre_area_3", use_container_width=True, on_click=_set_area_preset, args=("cos(x)", "x", 0.0, 1.6))
with p_cols[3]:
    st.button("$x^{1/3}$ และ $x$", key="pre_area_4", use_container_width=True, on_click=_set_area_preset, args=("x**(1/3)", "x", -1.0, 1.0))

col_f, col_g = st.columns(2)
with col_f:
    f_input = st.text_input(
        "เส้นโค้ง f(x)",
        key="area_f",
        placeholder="เช่น x, x**2, sin(x), x**(1/3)",
    )
    preview_math_expr(f_input, label="พรีวิว f(x)")
with col_g:
    g_input = st.text_input(
        "เส้นโค้ง g(x)",
        key="area_g",
        placeholder="เช่น x**2, x - 1, 0",
    )
    preview_math_expr(g_input, label="พรีวิว g(x)")

render_syntax_guide()

from utils.keypad import render_math_keypad
render_math_keypad(target_key="area_f", key_prefix="area_f_kp", title="แผงปุ่มลัดสัญลักษณ์คณิตศาสตร์ (พิมพ์ลงใน f(x))", expanded=False)

# ---------------------------------------------------------------------------
# Step 1: Analyze intersection points before choosing integration interval
# ---------------------------------------------------------------------------
if f_input.strip() and g_input.strip():
    inter_res = find_curve_intersections(f_input, g_input)

    with st.container(border=True):
        st.markdown("#### การวิเคราะห์จุดตัดของเส้นโค้ง ($f(x) = g(x)$)")
        if inter_res["ok"]:
            v = inter_res.get("variable", "x")
            count = inter_res.get("count", 0)
            roots = inter_res.get("roots", [])
            roots_latex = inter_res.get("roots_latex", [])

            if count >= 2:
                roots_disp = ", ".join(f"${v} = {rl}$" for rl in roots_latex)
                st.success(f"พบจุดตัด {count} จุดที่ {roots_disp}: เส้นโค้งตัดกันและปิดล้อมพื้นที่จำกัดโดยธรรมชาติ")

                # Shortcut buttons to select integration interval based on detected intersections
                nat_a, nat_b = inter_res["natural_bounds"]
                btn_cols = st.columns(min(len(roots), 3))
                with btn_cols[0]:
                    st.button(
                        f"ใช้จุดตัดขอบนอก [{roots_latex[0]}, {roots_latex[-1]}] เป็นช่วงอินทิเกรต",
                        key="btn_apply_all_intersections",
                        use_container_width=True,
                        on_click=_apply_bounds,
                        args=(nat_a, nat_b),
                    )

                if count > 2:
                    sub_intervals = inter_res.get("sub_intervals", [])
                    for idx, (sub_l, sub_r) in enumerate(sub_intervals[:2], start=1):
                        with btn_cols[idx]:
                            st.button(
                                f"ใช้ช่วงย่อยที่ {idx} [{roots_latex[idx-1]}, {roots_latex[idx]}]",
                                key=f"btn_apply_sub_loop_{idx}",
                                use_container_width=True,
                                on_click=_apply_bounds,
                                args=(sub_l, sub_r),
                            )
            elif count == 1:
                st.warning(
                    f"พบจุดตัดเพียง 1 จุดที่ ${v} = {roots_latex[0]}$: เส้นโค้งไม่สามารถปิดล้อมพื้นที่จำกัดได้ด้วยตัวเอง "
                    "จำเป็นต้องระบุขอบเขต $a$ และ $b$ ด้านล่าง (เช่น เส้นขอบเขตที่โจทย์กำหนด) เพื่อคำนวณพื้นที่ในช่วงที่ต้องการ"
                )
            else:
                st.info(
                    "ไม่พบจุดตัดระหว่างเส้นโค้งทั้งสอง (กราฟไม่ตัดกัน): เส้นโค้งไม่ปิดล้อมพื้นที่จำกัดโดยธรรมชาติ "
                    "จำเป็นต้องระบุขอบเขต $a$ และ $b$ ด้านล่าง เพื่อหาพื้นที่ในช่วงที่สนใจ"
                )
        else:
            st.warning(f"ไม่สามารถหาจุดตัดได้อัตโนมัติ: {inter_res.get('error')}")

# ---------------------------------------------------------------------------
# Step 2: Select or specify integration interval [a, b]
# ---------------------------------------------------------------------------
st.markdown("#### เลือกช่วงอินทิเกรตที่ต้องการ $[a, b]$")
col_a, col_b = st.columns(2)
with col_a:
    a_val = st.number_input("ขอบล่าง a", key="area_a")
with col_b:
    b_val = st.number_input("ขอบบน b", key="area_b")

if not f_input.strip() or not g_input.strip():
    st.info("กรุณาระบุฟังก์ชัน f(x) และ g(x) หรือคลิกเลือกตัวอย่างด้านบน")
elif a_val >= b_val:
    st.warning("ขอบล่าง a ต้องน้อยกว่าขอบบน b (กรุณาปรับค่าขอบเขต)")
else:
    res = compute_area_between(f_input, g_input, a_val, b_val)
    if res["ok"]:
        v_name = res.get("variable", "x")
        if v_name != "x":
            st.info(f"ตรวจพบตัวแปร **${v_name}$**: ระบบคำนวณและวาดกราฟเทียบกับตัวแปร ${v_name}$ อัตโนมัติ")

        st.markdown("### ผลลัพธ์")
        render_latex(res["latex"])
        st.divider()

        st.markdown("### กราฟพื้นที่ระหว่างเส้นโค้ง")

        try:
            fig_plotly = plot_area_between_plotly(
                res["f_expr"],
                res["g_expr"],
                a_val,
                b_val,
                crossings=res.get("crossings"),
            )
            st.plotly_chart(fig_plotly, use_container_width=True, config={"scrollZoom": True, "displayModeBar": True})
        except Exception as e:
            st.warning("แสดงผลกราฟ interactive ขัดข้อง กำลังสลับไปใช้กราฟสำรอง")
            try:
                fig, ax = plot_area_between(res["f_expr"], res["g_expr"], a_val, b_val)
                st.pyplot(fig)
            except Exception as e2:
                st.warning(f"ไม่สามารถวาดกราฟได้: {e2}")

        st.markdown("### ขั้นตอนการคำนวณอย่างละเอียด")
        render_steps(res["steps"])
    else:
        st.error(res["error"])
