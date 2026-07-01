# Basic Integration Rules

## Learning objectives

เมื่อเรียนจบบทนี้ ผู้เรียนควรสามารถ

1. ใช้กฎคูณด้วยค่าคงที่ (constant multiple rule) ได้
2. ใช้กฎผลบวก (sum rule) เพื่อแยกพจน์ก่อนอินทิเกรตได้
3. ใช้กฎยกกำลัง (power rule) กับ $x^n$ เมื่อ $n\ne -1$ ได้
4. เขียนคำตอบของ indefinite integral พร้อม $+C$ ได้

## Constant rule

เมื่ออินทิเกรตค่าคงที่ จะได้ค่าคงที่คูณกับตัวแปร

$$
\int a\,dx = ax+C
$$

ตัวอย่าง:

$$
\int 5\,dx = 5x+C
$$

## Power rule

ถ้า $n\ne -1$ แล้ว

$$
\int x^n\,dx = \frac{x^{n+1}}{n+1}+C
$$

ตัวอย่าง:

$$
\int x^4\,dx = \frac{x^5}{5}+C
$$

ข้อควรระวัง: สูตรนี้ใช้กับ $n=-1$ ไม่ได้ เพราะจะเกิดการหารด้วยศูนย์

$$
\int x^{-1}\,dx = \int \frac{1}{x}\,dx = \ln|x|+C
$$

## Constant multiple rule

ค่าคงที่สามารถดึงออกมาหน้าเครื่องหมายอินทิเกรตได้

$$
\int kf(x)\,dx = k\int f(x)\,dx
$$

ตัวอย่าง:

$$
\int 3x^2\,dx = 3\int x^2\,dx = 3\cdot\frac{x^3}{3}+C = x^3+C
$$

## Sum rule

อินทิเกรตของผลบวกเท่ากับผลบวกของอินทิเกรต

$$
\int (f(x)+g(x))\,dx = \int f(x)\,dx+\int g(x)\,dx
$$

ตัวอย่าง:

$$
\int (3x^2-4x+5)\,dx
$$

แยกทีละพจน์:

$$
= \int 3x^2\,dx-\int 4x\,dx+\int 5\,dx
$$

ใช้กฎพื้นฐาน:

$$
= x^3-2x^2+5x+C
$$

## Common mistakes

- เพิ่มเลขชี้กำลังแล้วลืมหารด้วยเลขชี้กำลังใหม่
- ลืมกระจายเครื่องหมายลบก่อนอินทิเกรต
- ใช้ power rule กับ $\int \frac{1}{x}\,dx$ ทั้งที่ต้องได้ $\ln|x|+C$
- ลืม $+C$ ในคำตอบสุดท้าย

## Try it yourself

จงหา

$$
\int (6x^2+2x-7)\,dx
$$

แนวคิด: แยกเป็นสามพจน์ ใช้ power rule กับสองพจน์แรก และใช้ constant rule กับพจน์สุดท้าย
