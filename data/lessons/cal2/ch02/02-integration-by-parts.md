---
title: "2.2 การอินทิเกรตโดยการแจงส่วน (Integration by Parts)"
course: cal2
chapter: 2
section: "2.2"
type: content
source: "Calculus2-ch2-integrals.pdf"
status: transformed
---

# 2.2 การอินทิเกรตโดยการแจงส่วน (Integration by Parts)

ถ้า $u = f(x)$ และ $v = g(x)$ เป็นฟังก์ชันที่มีอนุพันธ์ต่อเนื่อง แล้ว

$$\int u \, dv = uv - \int v \, du$$

สืบเนื่องจากกฎผลคูณของการหาอนุพันธ์ $(uv)' = u'v + uv'$ นำมาอินทิเกรตสองข้างแล้วจัดรูปใหม่

**เมื่อใดควรใช้:** ใช้เมื่ออินทิกรัลมีลักษณะผลคูณ เช่น $\int x\sin x\,dx$, $\int x e^x\,dx$, $\int \ln x\,dx$ ที่การแทนค่าไม่พอ

**ตัวอย่าง 2.2.1** จงหา $\int x\sin x\,dx$

เลือก $u = x$, $dv = \sin x\,dx$ จะได้ $du = dx$, $v = -\cos x$

$$\begin{align}
\int x\sin x\,dx &= -x\cos x - \int(-\cos x)\,dx \\
&= -x\cos x + \sin x + C
\end{align}$$

**วิธีเลือก $u$ (มเนติก LIATE):** ลำดับความสำคัญ Logarithmic > Inverse trig > Algebraic > Trigonometric > Exponential

**การใช้ซ้ำ (Repeated IBP):** บางครั้งต้องใช้การอินทิเกรตโดยการแจงส่วนสองครั้ง เช่น $\int x^2 e^{3x}\,dx$
