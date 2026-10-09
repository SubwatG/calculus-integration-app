import streamlit as st
from utils.keypad import render_math_keypad
from utils.math_render import preview_math_expr, render_latex, render_steps, render_syntax_guide
from utils.sympy_solver import compute_limit, detect_variable, differentiate, integrate
from utils.theme import render_hero

render_hero("แคลคูลัส", "เครื่องคิดเลขสัญลักษณ์ SymPy พร้อมวิธีทำทีละขั้นตอน")

op_options = ["อินทิเกรต", "อนุพันธ์", "ลิมิต"]
if "solver_op" not in st.session_state:
    st.session_state["solver_op"] = "อินทิเกรต"

if "solver_expr" not in st.session_state:
    st.session_state["solver_expr"] = "x^2"

if "limit_point" not in st.session_state:
    st.session_state["limit_point"] = 0.0

def _clear_input() -> None:
    st.session_state["solver_expr"] = ""
    st.session_state["solver_res"] = None
    st.session_state["last_calc_sig"] = None
    st.session_state["solver_custom_var"] = "x"

def _set_preset(val: str, pt: float | None = None) -> None:
    st.session_state["solver_expr"] = val
    if pt is not None:
        st.session_state["limit_point"] = pt
    st.session_state["solver_res"] = None
    st.session_state["last_calc_sig"] = None
    st.session_state["solver_custom_var"] = detect_variable(val)

cur_expr_raw = st.session_state.get("solver_expr", "").strip()
detected_var = detect_variable(cur_expr_raw) if cur_expr_raw else "x"

col_op, col_tools = st.columns([3, 2])
with col_op:
    if hasattr(st, "segmented_control"):
        operation = st.segmented_control(
            "ประเภทการคำนวณ",
            op_options,
            key="solver_op",
        )
    else:
        operation = st.selectbox("ประเภทการคำนวณ", op_options, key="solver_op")

# Point input for limit
point_val = 0.0
if st.session_state["solver_op"] == "ลิมิต":
    point_val = st.number_input(
        f"จุดที่ {detected_var} เข้าใกล้ (a)",
        key="limit_point",
        step=1.0,
    )

# Input field, Variable selector & Clear button
col_in, col_var, col_clear = st.columns([4, 1.2, 1])
with col_in:
    expr_input = st.text_input(
        f"ใส่โจทย์ฟังก์ชัน f({detected_var})",
        key="solver_expr",
        placeholder="เช่น x^2, 3t^2 + 2t, sin(t), e^u, (y^2-4)/(y-2)",
    )
with col_var:
    var_override = st.text_input(
        "เทียบตัวแปร",
        value=detected_var,
        key="solver_custom_var",
        help="ตัวแปรอิสระที่ต้องการคำนวณ (ระบบจะตรวจจับให้อัตโนมัติ หรือท่านสามารถพิมพ์เปลี่ยนเองได้ เช่น x, t, y, u)",
    )
with col_clear:
    st.write("")
    st.write("")
    st.button("🗑️ ล้าง", key="btn_clear_input", use_container_width=True, help="ล้างช่องใส่โจทย์", on_click=_clear_input)

active_var = (var_override or "").strip() or detected_var

if active_var != "x":
    st.info(f"✨ **ระบบตรวจจับตัวแปรอัตโนมัติ (Auto-detect):** คำนวณเทียบกับตัวแปร `{active_var}` (ปริพันธ์ $d{active_var}$ / อนุพันธ์ $\\frac{{d}}{{d{active_var}}}$)")

preview_math_expr(st.session_state.get("solver_expr", ""))
render_syntax_guide()

# Math Keypad Reusable Component
render_math_keypad(target_key="solver_expr", key_prefix="solver_kp", expanded=True, include_infinity=True)

# Quick Preset Examples based on operation
st.caption("🎯 ตัวอย่างโจทย์ยอดนิยม (คลิกเพื่อทดสอบทันที):")
if st.session_state["solver_op"] == "อินทิเกรต":
    ex_cols = st.columns(6)
    presets = [
        ("x²", "x^2"),
        ("3x² - 4x + 5", "3*x^2 - 4*x + 5"),
        ("1/x", "1/x"),
        ("sin(x)", "sin(x)"),
        ("e^x", "e^x"),
        ("√x", "sqrt(x)"),
    ]
    for idx, (lbl, val) in enumerate(presets):
        with ex_cols[idx]:
            st.button(lbl, key=f"preset_int_{idx}", use_container_width=True, on_click=_set_preset, args=(val, None))
elif st.session_state["solver_op"] == "อนุพันธ์":
    ex_cols = st.columns(6)
    presets = [
        ("x⁴", "x^4"),
        ("x³ - 3x", "x^3 - 3*x"),
        ("sin(x)cos(x)", "sin(x)*cos(x)"),
        ("(x²+1)/(x-1)", "(x^2 + 1)/(x - 1)"),
        ("e^(2x)", "e^(2*x)"),
        ("1/x", "1/x"),
    ]
    for idx, (lbl, val) in enumerate(presets):
        with ex_cols[idx]:
            st.button(lbl, key=f"preset_diff_{idx}", use_container_width=True, on_click=_set_preset, args=(val, None))
else:
    ex_cols = st.columns(4)
    presets_lim = [
        ("(x²-4)/(x-2) → 2", "(x^2 - 4)/(x - 2)", 2.0),
        ("sin(x)/x → 0", "sin(x)/x", 0.0),
        ("1/x → 0", "1/x", 0.0),
        ("(√x - 1)/(x - 1) → 1", "(sqrt(x) - 1)/(x - 1)", 1.0),
    ]
    for idx, (lbl, val, pt) in enumerate(presets_lim):
        with ex_cols[idx]:
            st.button(lbl, key=f"preset_lim_{idx}", use_container_width=True, on_click=_set_preset, args=(val, pt))

st.write("")
calc_clicked = st.button("🚀 คำนวณผลลัพธ์", type="primary", key="btn_do_calc", use_container_width=True)

cur_expr = st.session_state.get("solver_expr", "").strip()
current_op = st.session_state["solver_op"]
sig = f"{current_op}:{cur_expr}:{active_var}:{point_val}"

if calc_clicked or (cur_expr and st.session_state.get("last_calc_sig") != sig):
    if not cur_expr:
        st.error("กรุณาใส่โจทย์ก่อนทำการคำนวณ")
        st.session_state["solver_res"] = None
    else:
        if current_op == "อินทิเกรต":
            res = integrate(cur_expr, var=active_var)
        elif current_op == "อนุพันธ์":
            res = differentiate(cur_expr, var=active_var)
        else:
            res = compute_limit(cur_expr, point_val, var=active_var)
        st.session_state["solver_res"] = res
        st.session_state["last_calc_sig"] = sig

res = st.session_state.get("solver_res")
if res:
    if res["ok"]:
        res_var = res.get("variable", "x")
        if res_var != "x":
            st.success(f"🎯 **คำนวณสำเร็จเทียบกับตัวแปรอัตโนมัติ:** `{res_var}`")
        st.markdown("### สมการผลลัพธ์")
        render_latex(res["latex"])

        # Render step-by-step solution cleanly
        render_steps(res["steps"])
    else:
        st.error(res["error"])
