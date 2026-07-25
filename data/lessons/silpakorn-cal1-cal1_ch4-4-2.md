## 4.2 4.2.3 ฟังก์ชันที่มีรูปแบบไม่กำหนดแบบ $0^\circ$, $1^\infty$ และ $\infty^\circ$

ฟังก์ชันที่มีรูปแบบไม่กำหนดกลุ่มสุดท้ายที่เราจะกล่าวถึงคือรูปแบบ $0^\circ$, $1^\infty$ และ $\infty^\circ$ รูปแบบเหล่านี้เกิดจากฟังก์ชันในรูป $f(x)^{g(x)}$ กล่าวคือ

1.  ถ้า $\lim_{x \to c} f(x) = \lim_{x \to c} g(x) = 0$ แล้ว $f(x)^{g(x)}$ มีรูปแบบไม่กำหนดแบบ $0^\circ$ ที่ $c$
2.  ถ้า $\lim_{x \to c} f(x) = 1$ และ $\lim_{x \to c} g(x) = \pm\infty$ แล้ว $f(x)^{g(x)}$ มีรูปแบบไม่กำหนดแบบ $1^\infty$ ที่ $c$
3.  ถ้า $\lim_{x \to c} f(x) = \pm\infty$ และ $\lim_{x \to c} g(x) = 0$ แล้ว $f(x)^{g(x)}$ มีรูปแบบไม่กำหนดแบบ $\infty^\circ$ ที่ $c$

ในการหาลิมิตของฟังก์ชันทั้ง 3 รูปแบบเราจะเริ่มต้นโดยให้

สาขาวิชาคณิตศาสตร์


$$ y = f(x)^{g(x)} $$
จากนั้นใส่ลอการิทึมฐาน e เข้าทั้ง 2 ข้างของสมการ ซึ่งทำให้ได้ว่า
$$ \ln y = \ln f(x)^{g(x)} = g(x)\ln f(x) $$
ถ้า y มีรูปแบบไม่กำหนดแบบ $0^0$, $\infty^0$ หรือ $1^\infty$ ที่ $x=c$ แล้ว $\ln y$ มีรูปแบบไม่กำหนดแบบ $0\cdot\infty$ ที่ $c$
จากนั้นเราสามารถเปลี่ยน $\ln y$ ให้มีรูปแบบไม่กำหนดแบบ $\frac{0}{0}$ หรือ $\frac{\infty}{\infty}$ ที่ $c$ ดังในหัวข้อ 4.2.1 เนื่องจาก $\ln y$ เป็นฟังก์ชันต่อเนื่อง จะได้ว่า
$$ \lim_{x\to c} \ln y = \ln \lim_{x\to c} y = \lim_{x\to c} \ln y = L $$

จะได้ว่า
$$ \lim_{x\to c} y = \lim_{x\to c} e^{\ln y} = e^{L} $$
นั่นคือ
$$ \lim_{x\to c} f(x)^{g(x)} = e^L $$
จากที่กล่าวมาข้างต้นเราอาจสรุปแนวทางในการหา $\lim_{x\to c} f(x)^{g(x)}$ เมื่อ $f(x)^{g(x)}$ มีรูปแบบไม่กำหนดแบบ $0^0$, $1^\infty$ หรือ $\infty^0$ ที่ $c$ ดังนี้
1. ให้ $y = f(x)^{g(x)}$
2. ใส่ลอการิทึมฐาน $e$ เข้าทั้ง 2 ข้างของสมการใน (1) เราได้
    $$ \ln y = \ln f(x)^{g(x)} = g(x)\ln f(x) $$
3. หา $\lim_{x\to c} \ln y$ ถ้าลิมิตดังกล่าวนี้มีค่า
4. ถ้า $\lim_{x\to c} \ln y = L$ แล้ว $\lim_{x\to c} f(x)^{g(x)} = e^L$

**ตัวอย่าง 4.2.4** จงหา $\lim_{x\to 0^+} (1+3x)^{\frac{1}{2x}}$
วิธีทำ เนื่องจาก $\lim_{x\to 0^+} (1+3x) = 1$ และ $\lim_{x\to 0^+} \frac{1}{2x} = +\infty$ ดังนั้น $(1+3x)^{\frac{1}{2x}}$ มีรูปแบบไม่กำหนดแบบ $1^\infty$ ที่ $0$ โดยแนวทางข้างต้นเราให้ $y = (1+3x)^{\frac{1}{2x}}$ จะได้ว่า
$$ \ln y = \ln(1+3x)^{\frac{1}{2x}} = \frac{1}{2x}\ln(1+3x) = \frac{\ln(1+3x)}{2x} $$


จะได้ว่า $\ln y$ มีรูปแบบไม่กำหนดแบบ $\frac{0}{0}$ ที่ $0$ ดังนั้น

$$\lim_{x \to 0} \ln y = \lim_{x \to 0} \frac{\ln(1+3x)}{2x} = \lim_{x \to 0} \frac{1+3x}{2x} = \frac{3}{2}$$

จะได้ว่า $\lim_{x \to 0} (1+3x)^{\frac{1}{2x}} = e^{\frac{3}{2}}$

ตัวอย่าง 4.2.5 จงหา $\lim_{x \to 0^+} x^x$

วิธีทำ เนื่องจาก $\lim_{x \to 0^+} x = 0$ ดังนั้น $x^x$ มีรูปแบบไม่กำหนดแบบ $0^0$ ที่ $0$ โดยแนวทางข้างต้น เราให้ $y = x^x$ จะได้ว่า

$$\ln y = \ln x^x = x \ln x$$

จากนั้นหาลิมิต จะได้

$$\lim_{x \to 0^+} \ln y = \lim_{x \to 0^+} x \ln x = 0$$

ดังนั้น $\lim_{x \to 0^+} x^x = e^0 = 1$

ตัวอย่าง 4.2.6 จงหา $\lim_{x \to \frac{\pi}{2}} (\tan x)^{\cos x}$

วิธีทำ เนื่องจาก $\lim_{x \to \frac{\pi}{2}} \tan x = +\infty$ และ $\lim_{x \to \frac{\pi}{2}} \cos x = 0$ ดังนั้น $(\tan x)^{\cos x}$ มีรูปแบบไม่กำหนดแบบ $\infty^0$

ที่ $\frac{\pi}{2}$ โดยแนวทางข้างต้นเราให้ $y = (\tan x)^{\cos x}$ จะได้ว่า

$$\ln y = \ln(\tan x)^{\cos x} = (\cos x)(\ln \tan x) = \frac{\ln \tan x}{\sec x}$$

ทำให้ได้ว่า

$$\lim_{x \to \frac{\pi}{2}} \ln y = \lim_{x \to \frac{\pi}{2}} \frac{\ln \tan x}{\sec x} = \lim_{x \to \frac{\pi}{2}} \frac{\sec^2 x}{\sec x} = \lim_{x \to \frac{\pi}{2}} \frac{\sec^2 x}{\sec x} = \lim_{x \to \frac{\pi}{2}} \frac{\cos x}{\sin x} = 0$$

ดังนั้น $\lim_{x \to \frac{\pi}{2}} (\tan x)^{\cos x} = e^0 = 1$

ภาคผนวก คณิตศาสตร์ มีรูปแบบไม่กำหนดแบบ $\frac{0}{0}$ ที่ $\frac{\pi}{2}$

216


เราจะจบหัวข้อนี้โดยการกล่าวถึงทฤษฎีบทเกี่ยวกับลิมิตที่สำคัญบทหนึ่งซึ่งใช้ความรู้ข้างต้นในการพิสูจน์ดังต่อไปนี้

**ทฤษฎีบท 4.2.7**
1. $\lim_{n \to +\infty} \sqrt[n]{a} = 1$ เมื่อ $a$ เป็นจำนวนจริงบวกใด ๆ
2. $\lim_{n \to +\infty} \sqrt[n]{n} = 1$
3. $\lim_{n \to +\infty} \left(1+\frac{a}{n}\right)^n = e^a$ เมื่อ $a$ เป็นจำนวนจริงใด ๆ

**บทพิสูจน์ 1.** ให้ $y = \sqrt[n]{a} = a^{1/n}$ จากนั้นใส่ลอการิทึมฐาน $e$ เข้าทั้ง 2 ข้างของสมการ เราได้ว่า $\ln y = \ln a^{1/n} = \frac{1}{n} \ln a$ เมื่อหาลิมิตของ $\ln y$ จะได้ว่า
$\lim_{n \to +\infty} \ln y = \lim_{n \to +\infty} \frac{1}{n} \ln a = 0$
ดังนั้น $\lim_{n \to +\infty} y = \lim_{n \to +\infty} e^0 = 1$

2. ให้ $y = \sqrt[n]{n} = n^{1/n}$ จากนั้นใส่ลอการิทึมฐาน $e$ เข้าทั้ง 2 ข้างของสมการ จะได้
$\ln y = \ln n^{1/n} = \frac{1}{n} \ln n$ เมื่อหาลิมิตของ $\ln y$ จะได้ว่า
$\lim_{n \to +\infty} \ln y = \lim_{n \to +\infty} \frac{\ln n}{n} = \lim_{n \to +\infty} \frac{1}{n} = 0$
ดังนั้น $\lim_{n \to +\infty} y = \lim_{n \to +\infty} e^0 = 1$

3. ให้ $y = \left(1+\frac{a}{n}\right)^n$ จากนั้นใส่ลอการิทึมฐาน $e$ เข้าทั้ง 2 ข้างของสมการ เราได้ว่า
$\ln y = \ln \left(1+\frac{a}{n}\right)^n = n \ln \left(1+\frac{a}{n}\right)$ เมื่อหาลิมิตของ $\ln y$ เมื่อ $n \to +\infty$ จะได้ว่า
$\lim_{n \to +\infty} \ln y = \lim_{n \to +\infty} n \ln \left(1+\frac{a}{n}\right) = \lim_{n \to +\infty} \frac{\ln \left(1+\frac{a}{n}\right)}{n} = \lim_{n \to +\infty} \frac{1+\frac{a}{n}}{-\frac{a}{n}} = \lim_{n \to +\infty} \frac{1+\frac{a}{n}}{-\frac{a}{n}} = \lim_{n \to +\infty} \frac{n+1-a}{-a} = \lim_{n \to +\infty} -\frac{n+1-a}{a} = -\frac{a}{a} = -1$
ดังนั้น $\lim_{n \to +\infty} y = \lim_{n \to +\infty} \left(1+\frac{a}{n}\right)^n = e^{-1} = \frac{1}{e}$

☐
