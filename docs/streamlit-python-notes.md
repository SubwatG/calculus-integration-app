# Streamlit และ Python Notes สำหรับโปรเจกต์นี้

เอกสารนี้เป็นคู่มืออ่านประกอบสำหรับนักศึกษาที่จะพัฒนา `calculus-integration-app`
เป้าหมายคือเข้าใจ code ที่มีอยู่ และเห็นตัวอย่าง Python/Streamlit ที่สามารถนำไปต่อยอดได้

## 1. Streamlit คืออะไร

Streamlit คือ library ของ Python สำหรับสร้างเว็บแอปอย่างรวดเร็ว เหมาะกับงานสอน
งานวิเคราะห์ข้อมูล และ prototype เพราะเขียนด้วย Python เป็นหลัก ไม่ต้องเริ่มจาก HTML,
CSS และ JavaScript เต็มรูปแบบ

แนวคิดสำคัญคือ เมื่อผู้ใช้กดปุ่มหรือเปลี่ยน widget Streamlit จะ rerun script ใหม่
ตั้งแต่ต้น ดังนั้นค่าที่ต้องจำข้ามการ rerun เช่น คะแนน quiz ต้องเก็บใน
`st.session_state`

## 2. โครงสร้างของโปรเจกต์นี้

```text
app.py
pages/
  home.py
  lessons.py
  quiz.py
data/
  lessons/
    overview.md
    basic_rules.md
  quizzes/
    basic_rules.json
utils/
  content_loader.py
  quiz_engine.py
```

แนวคิดหลักคือแยก code ออกจากเนื้อหา

- `pages/*.py` คือหน้าเว็บ
- `data/lessons/*.md` คือบทเรียนภาษาไทย
- `data/quizzes/*.json` คือข้อสอบ
- `utils/*.py` คือ logic ที่ใช้ซ้ำ

## 3. Router ด้วย `st.navigation`

ไฟล์ `app.py` เป็น entrypoint ของแอป หน้าที่หลักคือกำหนดหน้าและสั่งให้ Streamlit run หน้าที่เลือก

```python
import streamlit as st

st.set_page_config(
    page_title="Calculus Tutor: Integration",
    page_icon="∫",
    layout="wide",
)

home = st.Page("pages/home.py", title="Home")
lessons = st.Page("pages/lessons.py", title="Lessons")
quiz = st.Page("pages/quiz.py", title="Quiz")

pg = st.navigation(
    {
        "Main": [home],
        "Learn": [lessons],
        "Assess": [quiz],
    }
)

pg.run()
```

ข้อควรจำ:

- `app.py` ไม่ควรใส่เนื้อหาบทเรียนเยอะ
- เมื่อใช้ `st.navigation` แล้ว ต้องเรียก `pg.run()`
- ไฟล์ใน `pages/` จะถูกใช้ผ่าน `st.Page` ไม่ใช่ระบบ auto-discovery แบบเก่า

## 4. แสดงข้อความด้วย `st.markdown`

ใช้ `st.markdown()` สำหรับข้อความยาว ภาษาไทย รายการหัวข้อ และสูตร LaTeX

```python
import streamlit as st

st.markdown(
    r"""
## Learning objectives

เมื่อเรียนจบบทนี้ ผู้เรียนควรสามารถ

1. อธิบายความหมายของอินทิเกรตได้
2. ใช้กฎพื้นฐานของอินทิเกรตได้

สูตรสำคัญคือ

$$
\int x^n\,dx = \frac{x^{n+1}}{n+1}+C,\quad n\ne -1
$$
"""
)
```

ใช้ `r"""..."""` เมื่อมี LaTeX เพราะช่วยลดปัญหา backslash ใน Python string

## 5. แสดงสูตรด้วย `st.latex`

ถ้าเป็นสูตรเดี่ยวที่อยากให้เด่น ใช้ `st.latex()`

```python
import streamlit as st

st.latex(r"\int_a^b f(x)\,dx = F(b)-F(a)")
```

ใน Markdown ให้ใช้:

- inline math: `$...$`
- display math: `$$...$$`

ตัวอย่าง:

```markdown
ถ้า $F'(x)=f(x)$ แล้ว

$$
\int f(x)\,dx = F(x)+C
$$
```

## 6. โหลดบทเรียนจาก Markdown

ไฟล์ `utils/content_loader.py` ใช้ `Path` เพื่อโหลดไฟล์ Markdown จาก `data/lessons`

```python
from pathlib import Path

import streamlit as st


PROJECT_ROOT = Path(__file__).resolve().parents[1]
LESSON_DIR = PROJECT_ROOT / "data" / "lessons"


@st.cache_data
def load_lesson(filename: str) -> str:
    path = LESSON_DIR / filename
    return path.read_text(encoding="utf-8")
```

จุดที่น่าสนใจ:

- `Path(__file__).resolve()` ทำให้หา path จากตำแหน่งไฟล์จริง
- `encoding="utf-8"` สำคัญสำหรับภาษาไทย
- `@st.cache_data` ช่วยให้ไม่ต้องอ่านไฟล์ซ้ำทุกครั้งที่ rerun

## 7. Sidebar สำหรับเลือกบทเรียน

หน้า `pages/lessons.py` ใช้ `st.sidebar.radio()` เพื่อเลือกบทเรียน

```python
import streamlit as st

from utils.content_loader import load_lesson


LESSONS = {
    "Integration Overview": "overview.md",
    "Basic Integration Rules": "basic_rules.md",
}

selected_lesson = st.sidebar.radio(
    "Lesson",
    list(LESSONS.keys()),
    key="lesson_selector",
)

content = load_lesson(LESSONS[selected_lesson])
st.markdown(content)
```

แนวคิดคือให้ dictionary เป็นตัวจับคู่ชื่อที่ผู้ใช้เห็นกับชื่อไฟล์จริง

## 8. Quiz ด้วย JSON

เก็บข้อสอบไว้ใน `data/quizzes/basic_rules.json`

```json
{
  "topic": "basic_rules",
  "question": "จงหา $\\int 3x^2\\,dx$",
  "choices": [
    "$x^3 + C$",
    "$3x^3 + C$",
    "$6x + C$",
    "$x^2 + C$"
  ],
  "answer": "$x^3 + C$",
  "explanation": "ใช้ power rule: $\\int 3x^2\\,dx = x^3+C$"
}
```

ข้อดีของ JSON:

- คนทำเนื้อหาเพิ่มข้อสอบได้โดยไม่ต้องแก้ Python มาก
- ตรวจคำตอบง่าย
- ใช้ร่วมกับ quiz engine ได้

ข้อควรระวัง:

- ใน JSON ต้องเขียน backslash เป็น `\\`
- string ต้องใช้ double quotes
- ห้ามมี comma เกินท้ายรายการสุดท้าย

## 9. ตรวจ quiz ด้วย Python

ไฟล์ `utils/quiz_engine.py` แยก logic การโหลดและตรวจข้อสอบออกจากหน้าเว็บ

```python
import json
from pathlib import Path
from typing import Any

import streamlit as st


PROJECT_ROOT = Path(__file__).resolve().parents[1]
QUIZ_DIR = PROJECT_ROOT / "data" / "quizzes"


@st.cache_data
def load_quiz(topic: str) -> list[dict[str, Any]]:
    path = QUIZ_DIR / f"{topic}.json"
    return json.loads(path.read_text(encoding="utf-8"))


def grade_quiz(
    questions: list[dict[str, Any]],
    answers: dict[int, str | None],
) -> dict[str, int]:
    score = 0

    for index, question in enumerate(questions):
        if answers.get(index) == question["answer"]:
            score += 1

    return {"score": score, "total": len(questions)}
```

จุดที่น่าสนใจ:

- `json.loads()` แปลงข้อความ JSON เป็น Python object
- `enumerate()` ใช้เมื่อต้องการทั้ง index และค่าของ item
- type hint เช่น `list[dict[str, Any]]` ช่วยให้อ่าน code ง่ายขึ้น

## 10. ใช้ `st.form` ในหน้า quiz

Quiz ควรใช้ `st.form` เพราะไม่ต้องการให้ตรวจคำตอบทุกครั้งที่ผู้เรียนคลิกตัวเลือก

```python
import streamlit as st

from utils.quiz_engine import grade_quiz, load_quiz


questions = load_quiz("basic_rules")

with st.form("basic_rules_quiz"):
    answers = {}

    for index, question in enumerate(questions):
        st.markdown(f"### ข้อ {index + 1}")
        st.markdown(question["question"])
        answers[index] = st.radio(
            "เลือกคำตอบ",
            question["choices"],
            index=None,
            key=f"basic_rules_q_{index}",
        )

    submitted = st.form_submit_button("ส่งคำตอบ")

if submitted:
    result = grade_quiz(questions, answers)
    st.session_state.quiz_scores["basic_rules"] = result
```

ข้อควรจำ:

- widget ใน form จะรอจนกด submit
- `index=None` ทำให้ radio ยังไม่เลือกคำตอบล่วงหน้า
- `key` ต้องไม่ซ้ำกัน

## 11. เก็บคะแนนด้วย `st.session_state`

เพราะ Streamlit rerun script บ่อย ค่าที่ต้องจำต้องเก็บใน `st.session_state`

```python
import streamlit as st


if "quiz_scores" not in st.session_state:
    st.session_state.quiz_scores = {}

st.session_state.quiz_scores["basic_rules"] = {
    "score": 4,
    "total": 5,
}
```

อ่านค่ากลับมาแสดง:

```python
score = st.session_state.quiz_scores.get("basic_rules")

if score is None:
    st.info("ยังไม่มีคะแนน quiz")
else:
    st.metric("Basic Rules Quiz", f"{score['score']}/{score['total']}")
    st.progress(score["score"] / score["total"])
```

ข้อควรระวัง:

- กำหนดค่าเริ่มต้นก่อนใช้งานเสมอ
- อย่าตั้งค่า widget ผ่าน `st.session_state` หลัง widget ถูกสร้างแล้ว

## 12. ตัวอย่าง Python ที่น่าสนใจ: เพิ่มบทเรียนใหม่

ถ้าต้องการเพิ่มบทเรียน `substitution.md`

1. สร้างไฟล์ `data/lessons/substitution.md`
2. เพิ่ม entry ใน `pages/lessons.py`

```python
LESSONS = {
    "Integration Overview": "overview.md",
    "Basic Integration Rules": "basic_rules.md",
    "Integration by Substitution": "substitution.md",
}
```

เพียงเท่านี้ sidebar จะมีบทเรียนใหม่

## 13. ตัวอย่าง Python ที่น่าสนใจ: สุ่มข้อสอบ

ตัวอย่างนี้ใช้ `random.sample()` เพื่อสุ่มข้อสอบบางส่วน

```python
import random


def pick_questions(questions: list[dict], count: int) -> list[dict]:
    if count >= len(questions):
        return questions
    return random.sample(questions, count)
```

การใช้งาน:

```python
questions = load_quiz("basic_rules")
questions = pick_questions(questions, 3)
```

ข้อควรระวัง: ถ้าสุ่มใหม่ทุกครั้งที่ rerun ผู้เรียนอาจเห็นโจทย์เปลี่ยนระหว่างทำ
ควรเก็บชุดที่สุ่มแล้วไว้ใน `st.session_state`

## 14. ตัวอย่าง Python ที่น่าสนใจ: ตรวจว่าข้อสอบครบ field หรือไม่

ใช้ตรวจคุณภาพ JSON ก่อนนำไปใช้จริง

```python
REQUIRED_FIELDS = {"topic", "question", "choices", "answer", "explanation"}


def validate_question(question: dict) -> list[str]:
    errors = []

    missing_fields = REQUIRED_FIELDS - set(question)
    if missing_fields:
        errors.append(f"Missing fields: {sorted(missing_fields)}")

    if "choices" in question and len(question["choices"]) < 2:
        errors.append("A question must have at least two choices.")

    if "answer" in question and "choices" in question:
        if question["answer"] not in question["choices"]:
            errors.append("Answer must be one of the choices.")

    return errors
```

แนวคิดนี้ช่วยลดปัญหา quiz พังเพราะ JSON ไม่ครบหรือเฉลยไม่ตรงกับตัวเลือก

## 15. ตัวอย่างเสริม: วาดกราฟพื้นที่ใต้เส้นโค้ง

ตัวอย่างนี้ต้องติดตั้ง `matplotlib` และ `numpy` เพิ่มก่อน

```powershell
pip install matplotlib numpy
```

ตัวอย่าง code:

```python
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st


def plot_area_under_curve(a: float, b: float) -> None:
    x = np.linspace(-1, 5, 400)
    y = x**2

    xs = np.linspace(a, b, 200)
    ys = xs**2

    fig, ax = plt.subplots()
    ax.plot(x, y, label=r"$f(x)=x^2$")
    ax.fill_between(xs, ys, alpha=0.3)
    ax.axhline(0, linewidth=0.8)
    ax.set_xlabel("x")
    ax.set_ylabel("f(x)")
    ax.legend()

    st.pyplot(fig)


a = st.slider("a", 0.0, 4.0, 1.0)
b = st.slider("b", 0.0, 4.0, 3.0)
plot_area_under_curve(a, b)
```

ส่วนนี้เหมาะกับหัวข้อ definite integral เพราะทำให้เห็นความหมายของพื้นที่ใต้กราฟ

## 16. ตัวอย่างเสริม: ใช้ SymPy ตรวจ antiderivative

ตัวอย่างนี้ต้องติดตั้ง `sympy` เพิ่มก่อน

```powershell
pip install sympy
```

ตัวอย่าง code:

```python
import sympy as sp


x = sp.symbols("x")


def check_antiderivative(integrand_str: str, answer_str: str) -> bool:
    integrand = sp.sympify(integrand_str)
    answer = sp.sympify(answer_str)
    derivative = sp.diff(answer, x)
    return sp.simplify(derivative - integrand) == 0


print(check_antiderivative("3*x**2", "x**3"))
print(check_antiderivative("2*x", "x**2 + 5"))
```

แนวคิดคือไม่เปรียบเทียบคำตอบตรง ๆ แต่ differentiate คำตอบของผู้เรียนกลับไปดูว่าได้ integrand เดิมหรือไม่

ข้อควรระวัง:

- สำหรับผู้เริ่มต้น ควรใช้ multiple choice ก่อน
- การรับ free text ทางคณิตศาสตร์มีความซับซ้อน
- อย่าปล่อยให้ SymPy กลายเป็นเครื่องทำเฉลยแทนการเรียนรู้

## 17. Checklist ก่อนแก้ code

ก่อนแก้ code ให้ถามตัวเอง:

1. ไฟล์นี้เป็นเนื้อหาหรือ logic
2. ถ้าเป็นเนื้อหา ควรอยู่ใน `data/lessons` หรือ `data/quizzes`
3. ถ้าเป็น logic ที่ใช้ซ้ำ ควรอยู่ใน `utils`
4. มี `learning objectives` หรือยัง
5. Quiz มี `explanation` ทุกข้อหรือยัง
6. สูตรใช้ `$...$` และ `$$...$$` ถูกต้องหรือยัง

## 18. คำสั่งที่ใช้บ่อย

เปิดแอป:

```powershell
streamlit run app.py
```

ตรวจ JSON:

```powershell
python -m json.tool data/quizzes/basic_rules.json
```

ตรวจ Python syntax:

```powershell
python -m py_compile app.py pages/home.py pages/lessons.py pages/quiz.py
```

ดูสถานะ Git:

```powershell
git status
```

ดึงงานล่าสุด:

```powershell
git pull
```

ส่ง branch ขึ้น GitHub:

```powershell
git push -u origin your-branch-name
```
