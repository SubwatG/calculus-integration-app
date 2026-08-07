---
title: "2.1 การอินทิเกรตโดยการแทน"
course: cal2
chapter: 2
section: "2.1"
type: content
source: "Calculus2-ch2-integrals.pdf"
status: transformed
---

# 2.1 การอินทิเกรตโดยการแทน

ถ้า $u$ เป็นฟังก์ชันของ $x$ และ $n$ เป็นจำนวนจริงใด ๆ โดยที่ $n \neq -1$ แล้วโดยกฎลูกโซ่ เราจะได้ว่า

$$\frac{d}{dx} \left( u \frac{n+1}{n+1} \right) = u^n \frac{du}{dx} \quad (2.1.1)$$

จากสมการ (2.1.1) เราสามารถกล่าวได้ว่านิพจน์ $\frac{u^{n+1}}{n+1}$ เป็นปฏิญานุพันธ์ของฟังก์ชัน $u^n \frac{du}{dx}$ ดังนั้น

$$\int \left( u^n \frac{du}{dx} \right) dx = \frac{u^{n+1}}{n+1} + C$$

อินทิกรัลทางซ้ายมือของสมการข้างต้นมักจะเขียนให้อยู่ในรูปดิฟเฟ่อเรลเชียลอย่างง่าย $\int u^n du$

ถ้า $u$ เป็นฟังก์ชันใด ๆ ที่สามารถหาอนุพันธ์ได้แล้ว เราจะได้ว่า


$$ \int u^n du = \frac{u^{n+1}}{n+1} + C $$
เมื่อ $n \neq -1$ (2.1.2)

จากสูตร (2.1.2) ถ้า $u$ คือฟังก์ชันของตัวแปร $x$ แล้ว เราอาจจะกล่าวได้ว่า

$$ \int (\text{นิพจน์ในตัวแปร } x)^n d(\text{นิพจน์ในตัวแปร } x) = \frac{(\text{นิพจน์ในตัวแปรของ } x)^{n+1}}{n+1} + C $$
เมื่อ $n \neq -1$ (2.1.3)

ทำให้เราสามารถประยุกต์สูตร (2.1.3) ข้างต้นในการอินทิเกรตได้ดังตัวอย่างต่อไปนี้

**ตัวอย่าง 2.1.1** จงหา
1. $\int (x+1)^{100} dx$
2. $\int 2\sqrt{1+x^2} dx$

วิธีทำ 1. เนื่องจาก $d(x+1) = dx$ และเมื่อแทนค่าจะได้
$$ \int (x+1)^{100} dx = \int (x+1)^{100} d(x+1) $$

ซึ่ง $\int (x+1)^{100} d(x+1)$ อยู่ในรูปทางซ้ายมือของสูตร (2.1.3) ทำให้ได้
$$ \int (x+1)^{100} dx = \int (x+1)^{100} d(x+1) = \frac{(x+1)^{101}}{101} + C $$

ตรวจสอบคำตอบ
$$ \frac{d}{dx}\left[\frac{(x+1)^{101}}{101} + C\right] = \frac{(101)(x+1)^{100} d(x+1)}{101} + 0 = (x+1)^{100} $$

2. เนื่องจาก $d(1+x^2)=2xdx$ และเมื่อแทนค่าจะทำให้ได้ $\int \sqrt{1+x^2} d(1+x^2)$ ซึ่งอยู่ในรูปทางซ้ายมือของสูตร (2.1.3) ดังนั้น
$$
\begin{align*}
\int 2\sqrt{1+x^2} dx  &= \int \sqrt{1+x^2} d(1+x^2) \\[0.5em]
&= \int (1+x^2)^{1/2} d(1+x^2) = \frac{3(1+x^2)^{3/2}}{2} + C
\end{align*}
$$

ตรวจสอบคำตอบ
$$ \frac{d}{dx}\left[ \frac{2(1+x^2)^{3/2}}{3} + C \right] = \frac{2}{3} \left[ \frac{3(1+x^2)^{1/2}}{2}(1+x^2)^{3/2} \right] dx + 0 = 2\sqrt{1+x^2} $$


สังเกตว่าในตัวอย่าง 2.1.1 $d(x+1)=dx$ และ $d(1+x^2)=2x dx$ โดยความเป็นจริงแล้ว ได้มีการสมมติตัวแปรใหม่ในรูปฟังก์ชันของตัวแปรเดิม กล่าวคือให้
$u=x+1$ และ $u=1+x^2$
จะได้ $du = dx$ และ $du = 2x dx$ ตามลำดับ ซึ่งทำให้ได้
$\int (x+1)^{100} dx = \int u^{100} du$ และ $\int 2x\sqrt{1+x^2} dx = \int \sqrt{u} du$
อยู่ในรูปสูตรพื้นฐานสูตรที่ 2 จากตารางสูตรพื้นฐานในบทที่ 1 (หน้า 4) ซึ่งลักษณะการอินทิเกรตโดยสมมติตัวแปรใหม่ขึ้นแล้วได้อินทิกรัลของตัวแปรใหม่อยู่ในรูปสูตรพื้นฐานหรือในรูปที่ทราบปฏิญานุพันธ์แล้ว เราเรียกว่า การอินทิเกรตโดยการแทน (integration by substitutions)

ถ้าให้ $F$ เป็นปฏิญานุพันธ์ของ $f$ แล้วโดยกฎลูกโซ่ของอนุพันธ์จะได้
$$
\frac{d}{dx} F(g(x)) = F'(g(x)) g'(x)
$$
และถ้า $u=g(x)$ แล้ว
$$
\int f(g(x)) g'(x) dx = \int \frac{d}{dx} F(g(x)) dx \\
= F(g(x)) + C \\
= F(u) + C \\
= \int f(u) du
$$
เราจึงสามารถสรุปสูตรการอินทิเกรตโดยการแทนได้ดังต่อไปนี้ ถ้า $u=g(x)$ ซึ่งเป็นฟังก์ชันที่หาอนุพันธ์ได้บนช่วง $I$ และ $f$ เป็นฟังก์ชันต่อเนื่องบน $I$ แล้ว

สูตรการอินทิเกรตโดยการแทน
$$
\int f(g(x)) g'(x) dx = \int f(u) du
$$
เทคนิคการอินทิเกรตโดยการแทนนี้ จะใช้ได้ต้องสามารถดัดแปลงอินทิกรัลให้เขียนได้ในรูป $\int f(g(x)) g'(x) dx$ ได้ เมื่อ $f$ และ $g'$ เป็นฟังก์ชันต่อเนื่อง และจะมีขั้นตอนในการทำดังนี้
1. ให้ $u=g(x)$ และ $du=g'(x)dx$ จากนิพจน์อินทิกรัลข้างต้น ทำให้เราได้
    $\int f(u) du$
2. หาค่าอินทิกรัลเทียบกับตัวแปร $u$
3. แทนค่า $u$ กลับในเทอมของ $g(x)$

ภาควิชาคณิตศาสตร์


ตัวอย่าง 2.1.2 จงหา
1. $\int x^2 e^{x^3} dx$
2. $\int e^u \sqrt{1+e^u} du$
3. $\int \frac{\ln x}{x} dx$

วิธีทำ 1. ให้ $u = x^3$ จะได้ $du = 3x^2 dx$ หรือ $x^2 dx = \frac{du}{3}$ ดังนั้น
$\int x^2 e^{x^3} dx = \int e^{u} \frac{du}{3} = \frac{1}{3} \int e^u du = \frac{e^u}{3} + C = \frac{e^x}{3} + C$

2. ให้ $u = 1 + e^x$ จะได้ $du = e^x dx$ ดังนั้น
$\int e^x \sqrt{1+e^x} dx = \int \sqrt{u} du = \frac{2}{3}(1+e^x)^3 + C$

3. ให้ $u = \ln x$ จะได้ $du = \frac{dx}{x}$ ดังนั้น
$\int \frac{\ln x}{x} dx = \int u du = \frac{u^2}{2} + C = \frac{(\ln x)^2}{2} + C$

ตัวอย่าง 2.1.3 จงหา
1. $\int \frac{dx}{x^2+4x+5}$
2. $\int \frac{(2x+4)}{\sqrt{x^2+4x+5}} dx$

วิธีทำ 1. เพราะว่า $\int \frac{dx}{x^2+4x+5} = \int \frac{dx}{(x+2)^2+1}$ จึงให้ $t = x + 2$ แล้วได้ $dt = dx$ ดังนั้น
$\int \frac{dx}{x^2+4x+5} = \int \frac{dt}{t^2+1} = \tan^{-1} t + C = \tan^{-1}(x+2)+C$

2. ให้ $v = x^2 + 4x + 5$ จะได้ $dv = (2x+4)dx$ จึงได้
$\int \frac{(2x+4)}{\sqrt{x^2+4x+5}} dx = \int \frac{dv}{\sqrt{v}} = 2\sqrt{v} + C = 2\sqrt{x^2+4x+5} + C$

ตัวอย่าง 2.1.4 จงหา $\int \frac{(x+1)dx}{\sqrt[3]{2x+1}}$

วิธีทำ ให้ $u = 2x + 1$ จะได้ $du = 2dx$ และ $x = \frac{u-1}{2}$ ทำให้ได้
$\int \frac{(x+1)dx}{\sqrt[3]{2x+1}} = \int \frac{(u+1)du}{\sqrt[3]{u}} = \frac{1}{4} \int \frac{u+1}{\sqrt[3]{u}} du = \frac{1}{4} \left[ u^3 du + \int \frac{du}{\sqrt[3]{u}} \right]$

$= \frac{1}{4} \left[ \frac{5}{3} u^3 + \frac{2}{3} u^3 \right] + C = \frac{3}{20}(2x+1)^5 + \frac{3}{8}(2x+1)^3 + C$

ภาควิชาคณิตศาสตร์

38


หมายเหตุ ตัวอย่าง 2.1.4 เป็นการอินทิเกรตฟังก์ชันในรูปแบบ $\frac{p(x)}{(ax+b)^n}$ เมื่อ $p(x)$ เป็นพหุนาม ใน $x$ และ $a$ และ $b$ เป็นค่าคงตัว $n$ เป็นจำนวนเต็มที่มากกว่า 1 ซึ่งเรามีวิธีการอินทิเกรตในกรณีทั่วไปแสดงในตัวอย่าง 2.1.5 ต่อไปนี้

**ตัวอย่าง 2.1.5** กำหนดให้ $a$ และ $b$ เป็นค่าคงตัว $n$ เป็นจำนวนเต็มที่มากกว่า 3 จงหา
1. $\int \frac{dx}{(ax+b)^n}$
2. $\int \frac{(x^2+1)}{(ax+b)^n} dx$

**วิธีทำ 1.** ให้ $u = ax + b$ แล้ว $du =adx$ หรือ $dx = \frac{du}{a}$ เพราะฉะนั้น
$\int \frac{dx}{(ax+b)^n} = \frac{1}{a} \int \frac{du}{u^n} = \frac{1}{a} \left[ \frac{u^{-n+1}}{-n+1} \right]_0^1 + C = \frac{(ax+b)^{n+1}}{a(-n+1)} + C$

**วิธีทำ 2.** ให้ $u = ax + b$ แล้ว $du =adx$ และ $x = \frac{u-b}{a}$ เพราะฉะนั้น
$\int \frac{(x^2+1)}{(ax+b)^n} dx = \frac{1}{a} \int \frac{\left(\frac{u-b}{a}\right)^2+1}{u^n} du = \frac{1}{a} \int \frac{u^2 - 2bu + b^2 + a^2}{u^n} du$
$= \frac{1}{a} \int \left[ u^{2-n} - 2bu^{1-n} + (b^2+a^2)u^{-n} \right] du$
$= \frac{1}{a} \left[ \frac{u^{3-n}}{3-n} - \frac{2bu^{1-n}}{2-n} + \frac{(b^2+a^2)u^{-n}}{1-n} \right]_0^1 + C$
$= \frac{1}{a} \left[ \frac{(ax+b)^{3-n}}{3-n} - \frac{2b(ax+b)^{1-n}}{2-n} + \frac{(b^2+a^2)(ax+b)^{-n}}{1-n} \right]_0^1 + C$

**ตัวอย่าง 2.1.6** จงหา
1. $\int \tan u du$
2. $\int \frac{dx}{x\ln x}$

**วิธีทำ 1.** โดยการพิจารณาว่า $\tan u = \frac{\sin u}{\cos u}$ และ $d(\cos u) = -\sin u du$ เราจึงให้ $t = \cos u$ ซึ่งจะได้ว่า $dt = -\sin u du$ เพราะฉะนั้น
$\int \tan u du = \int \frac{\sin u}{\cos u} dt = -\int \frac{\sin u}{t} dt = -\ln|t| + C = \ln|t|^{-1} + C$
$= \ln|\cos u|^{-1} + C = \ln|\sec u| + C$

ภาคีวิชาการ
39


2. สังเกตว่า $d(\ln x) = \frac{dx}{x}$ ดังนั้นจึงสมมติให้ $u = \ln x$ และได้ $du = \frac{dx}{x}$
เพราะฉะนั้น
$\int \frac{dx}{x \ln x} = \int \frac{du}{u} = \ln|u| + C = \ln|\ln|x|| + C$
O

**ตัวอย่าง 2.1.7 จงหา**
1. $\int \frac{dt}{\sqrt{4-9t^2}}$
2. $\int \frac{tdt}{\sqrt{4-9t^2}}$

วิธีทำ 1. สังเกตว่าอินทิกรัลที่กำหนดให้อยู่ในรูปคล้ายกับสูตรพื้นฐานสูตรที่ 12 เราจึงแปลง
$\sqrt{4-9t^2} = \sqrt{4(1-\frac{9}{4}t^2)} = 2\sqrt{1-\left(\frac{3}{2}\right)t^2}$
แล้วให้ $u = \frac{3}{2}t$ และได้ $du = \frac{3}{2} dt$ ซึ่งทำให้ได้
$\int \frac{dt}{\sqrt{4-9t^2}} = \int \frac{dt}{2\sqrt{1-\left(\frac{3}{2}\right)t^2}} = \int \frac{du}{2\sqrt{1-u^2}} = \frac{1}{3} \int \frac{du}{\sqrt{1-u^2}}$
$= \frac{1}{3} \sin^{-1} u + C = \frac{1}{3} \sin^{-1}\left(\frac{3}{2}t\right) + C$

2. การหาอินทิเกรตข้อนี้จะต่างจากตัวอย่าง 2.1.7 ข้อ 1 เพราะมี $t$ คูณอยู่ด้วยซึ่งเป็นอนุพันธ์ของ $t^2$ เราจึงให้ $u = 4 - 9t^2$ แล้วได้ $du = -18dt$ หรือ $tdt = \frac{-du}{18}$ ดังนั้น
$\int \frac{tdt}{\sqrt{4-9t^2}} = -\int \frac{du}{18\sqrt{u}} = \frac{-1}{18} \int \frac{du}{\sqrt{u}}$
$= -\left(-\frac{1}{18}(2\sqrt{u})\right) + C = -\frac{\sqrt{u}}{9} + C = -\frac{\sqrt{4-9t^2}}{9} + C$
O

**ตัวอย่าง 2.1.8 จงหา**
$\int x \left[9+4(\ln x)^2\right] dx$

วิธีทำ การอินทิเกรตข้อนี้ต้องใช้การเปลี่ยนตัวแปรสองครั้ง ดังนี้
ครั้งที่ 1 : ให้ $u = \ln x$ จะได้ $du = \frac{dx}{x}$ ซึ่งทำให้ได้
$\int x \left[9+4(\ln x)^2\right] dx = \int \frac{du}{9+4u^2}$
ครั้งที่ 2 : สังเกตว่า $\frac{1}{9+4u^2} = \frac{1}{9}\left(1+\frac{4u^2}{9}\right)$ อยู่ในรูปที่คล้ายกับสูตรพื้นฐานการอินทิเกรตสูตรที่ 13 เราจึงให้ $v = 2u$ และได้ $dv = 2du$ ซึ่งทำให้ได้


$$ \int \frac{du}{9+4u^2} = \frac{1}{2} \int \frac{dv}{9+v^2} = \frac{1}{6} \int \frac{d(v/3)}{1+(v/3)^2} = \frac{1}{6} \tan^{-1}\left(\frac{v}{3}\right)+C $$
เพราะฉะนั้น
$$ \int x \left[ 9+4 (\ln x)^2 \right] dx = \frac{1}{6} \tan^{-1}\left(\frac{2u}{3}\right)+C = \frac{1}{6} \tan^{-1}\left(\frac{2 \ln x}{3}\right)+C $$
หมายเหตุ เราอาจเปลี่ยนตัวแปรในตัวอย่าง 2.1.8 เพียงครั้งเดียว โดยให้ $u = \frac{2}{3} \ln x$

**ตัวอย่าง 2.1.9** จงหา $\int \sec x dx$

วิธีทำ ให้ $u = \sec x + \tan x$ แล้ว $du = (\sec x \tan x + \sec^2 x) dx = \sec x (\sec x + \tan x) dx$
เพราะฉะนั้น
$$ \int \sec x dx = \int \frac{\sec x (\sec x + \tan x)}{\sec x + \tan x} dx = \int \frac{du}{u} du = \ln |u| + C = \ln |\sec x + \tan x| + C $$

**หมายเหตุ** การเปลี่ยนตัวแปรในตัวอย่าง 2.1.9 ข้างต้นเป็นลักษณะเฉพาะของการหาอินทิกรัลในรูป $\int \sec x dx$ และ $\int \csc x dx$ ซึ่งผู้อ่านควรฝึกการหาอินทิกรัล $\int \csc x dx$ เป็นแบบฝึกหัด

จากเรื่องการอินทิเกรต เราได้ว่า $\int f(x) dx$ เป็นสัญลักษณ์แทนปฏิยานุพันธ์ของ $f(x)$ ซึ่งรวมค่าคงตัว ดังนั้นโดยทฤษฎีบทหลักมูลของแคลคูลัส เราจึงได้
$$ \int_a^b f(x) dx = \left[ \int f(x) dx \right]_a^b $$
ในการจะประยุกต์เทคนิคของการอินทิเกรตโดยการแทนกับการหาค่าอินทิกรัลจำกัดเขตต้องคำนึงว่าเมื่อตัวแปรได้เปลี่ยนไป ลิมิตล่างและลิมิตบนของอินทิกรัลในตัวแปรใหม่นั่นคือขอบเขตของตัวแปรใหม่ต้องเปลี่ยนไปด้วย กล่าวคือ

$$ \int_{x=a}^{x=b} f(g(x))g'(x)dx = \int_{u=g(a)}^{u=g(b)} f(u) du $$

**ตัวอย่าง 2.1.10** จงหาอินทิกรัลจำกัดเขตต่อไปนี้
1. $\int_a^b \frac{(\ln x)^2 + 1}{x \ln x} dx$
2. $\int_0^\pi x^2 \sqrt{1+x} dx$
3. $\int_0^{\pi/4} e^{\tan x} \sec^2 x dx$


วิธีทำ 1. ให้ $u = \ln x$ จะได้ $du = \frac{dx}{x}$ ทำให้ได้
$$
\begin{align*}
\int \frac{(\ln x)^2 + 1}{x \ln x} dx  &= \int \frac{u^2 + 1}{u} du = \int \left(u + \frac{1}{u}\right) du = \frac{u^2}{2} + \ln u + C \\[0.5em]
&= \frac{(\ln x)^2}{2} + \ln(\ln x) + C
\end{align*}
$$
ดังนั้น
$$
\begin{align*}
\int e^{(\ln x)^2+1} dx  &= \left[\frac{(\ln x)^2}{2} + \ln(\ln x)\right]_0^1 = \left[e^{\frac{(\ln x)^2}{2}} + \ln(\ln x)\right]_0^1 \\[0.5em]
&= \left[e^{\frac{(1)^2}{2}} + \ln(1)\right] - \left[e^{\frac{0^2}{2}} + \ln(0)\right] \\[0.5em]
&= \left[e^{\frac{1}{2}} + 0\right] - \left[e^0 + \ln(0)\right] \\[0.5em]
&= \left[e^{0.5} + 0\right] - \left[1 + \ln(0)\right] \\[0.5em]
&= \left[e^{0.5}\right] - \left[1 + \ln(0)\right]
\end{align*}
$$
เราสามารถหาอินทิกรัลจำกัดเขตข้างต้นได้อีกวิธีหนึ่งดังนี้ เนื่องจาก $e \leq x \leq e^2$ และลอการิทึม เป็นฟังก์ชันเพิ่ม ดังนั้น $\ln e \leq \ln x \leq \ln e^2$ ซึ่งสมมูลกับ $1 \leq u \leq 2$ ทำให้ได้
$$
\begin{align*}
\int e^{(\ln x)^2+1} dx  &= \int_{1}^{2} \left(u + \frac{1}{u}\right) du = \left[\frac{u^2}{2} + \ln u\right]_1^2 = \left[e^{\frac{2^2}{2}} + \ln(2)\right] - \left[e^{\frac{1^2}{2}} + \ln(1)\right] \\[0.5em]
&= \left[e^2 + \ln(2)\right] - \left[e^{0.5} + 0\right] \\[0.5em]
&= \frac{3}{2} + \ln(2)
\end{align*}
$$

2. ให้ $u = 1+x$ จะได้ $x^2 = (u-1)^2$ และ $dx = du$ นอกจากนี้ $0 \leq x \leq 3$ ก็ต่อเมื่อ $1 \leq 1+x \leq 4$ ดังนั้น
$$
\begin{align*}
\int_0^3 x^2 \sqrt{1+x} dx  &= \int_1^4 (u-1)^2 \sqrt{u} du = \int_1^4 (u^2 - 2u + 1) \sqrt{u} du \\[0.5em]
&= \int_1^4 \left(u^2 - 2u + 1\right) u^{3/2} du = \int_1^4 \left(\frac{2}{7}u^{7/2} - \frac{4}{5}u^{5/2} + \frac{2}{3}u^{3/2}\right) du \\[0.5em]
&= \left[\frac{2}{7} \cdot \frac{7}{3}u^{9/2} - \frac{4}{5} \cdot \frac{7}{3}u^{7/2} + \frac{2}{3}u^{3/2}\right]_1^4 \\[0.5em]
&= \left[\frac{2}{7}(2^3) - \frac{4}{5}(1) + \frac{2}{3}(4)\right] - \left[\frac{2}{7}(1) - \frac{4}{5}(1) + \frac{2}{3}(1)\right] \\[0.5em]
&= \left[\frac{16}{7} - \frac{4}{5} + \frac{8}{3}\right] - \left[-\frac{2}{7} - \frac{4}{5} + \frac{2}{3}\right] \\[0.5em]
&= \frac{16}{7} - \frac{4}{5} + \frac{8}{3} - (-\frac{2}{7} - \frac{4}{5} + \frac{2}{3}) \\[0.5em]
&= \frac{16}{7} - \frac{4}{5} + \frac{8}{3} + \frac{2}{7} + \frac{4}{5} - \frac{2}{3} \\[0.5em]
&= \frac{16}{7} + \frac{2}{7} + \frac{8}{3} + \frac{4}{5} - \frac{2}{3} \\[0.5em]
&= \frac{18}{7} + \frac{8}{3} + \frac{4}{5} - \frac{2}{3} \\[0.5em]
&= \frac{18}{7} + \frac{4}{3} + \frac{4}{5} - \frac{2}{3} \\[0.5em]
&= \frac{18}{7} + \frac{2}{3} + \frac{4}{5} \\[0.5em]
&= \frac{18}{7} + \frac{10}{15} + \frac{12}{15} \\[0.5em]
&= \frac{18}{7} + \frac{22}{15} \\[0.5em]
&= \frac{270}{105} + \frac{154}{105} \\[0.5em]
&= \frac{424}{105} \\[0.5em]
&= \frac{169.85}{105} \\[0.5em]
&= \frac{169.85}{105}
\end{align*}
$$

3. ให้ $t = \tan x$ จะได้ $dt = \sec^2 x dx$ และเพราะแทนเจนต์เป็นฟังก์ชันเพิ่มในช่วง $0$ ถึง $\frac{\pi}{4}$ ทำให้ได้ $0 \leq x \leq \frac{\pi}{4}$ ก็ต่อเมื่อ $0 = \tan 0 \leq \tan x \leq \tan \frac{\pi}{4} = 1$ ดังนั้น
$$
\begin{align*}
\int_0^{\frac{\pi}{4}} e^{\tan x} \sec^2 x dx  &= \int_0^{\frac{\pi}{4}} e^t dt = \left[e^t\right]_0^{\frac{\pi}{4}} = e^{-1} \\[0.5em]
&= e^{-1}
\end{align*}
$$
O

ถ้าอินทิเกรนด์ $f(x)$ ของอินทิกรัล $\int f(x) dx$ ประกอบด้วยพจน์ $\sqrt{ax+b}$ เมื่อ $n$ เป็น จำนวนเต็มบวก เราจะอินทิเกรตด้วยการเปลี่ยนตัวแปรใหม่ โดยให้


$u = \sqrt{ax+b}$ หรือ $u'' = ax + b$
แล้วได้ $x = \frac{u'' - b}{a}$ และ $dx = \frac{du^{n-1}}{a} du$
ซึ่งจะทำให้อินทิเกรนต์ในตัวแปร $x$ เปลี่ยนเป็นอินทิเกรนต์ในตัวแปร $u$ ซึ่งเป็นฟังก์ชันตรรกยะ

**ตัวอย่าง 2.1.11** จงหา
1. $\int \frac{x dx}{3+\sqrt{x+1}}$
2. $\int x^2 \sqrt{4x+5} dx$
3. $\int \frac{dx}{\sqrt{(x+1)^3} + \sqrt{x+1}}$

วิธีทำ 1. ให้ $u = \sqrt{x+1}$ หรือ $u^2 = x+1$ จะได้ $2udu=dx$ และ $x=u^2-1$ ทำให้ได้
$\int \frac{x dx}{3+\sqrt{x+1}} = \int \frac{(u^2-1)\cdot 2u}{3+u} du = 2 \int \frac{u^2-u}{3+u} du = 2 \int \left(u^2-3u+8-\frac{24}{u+3}\right) du$
$= \frac{2}{3} u^3 - 3u^2 + 16u - 48 \ln|u+3| + C$
$= \frac{2}{3}(x+1)^{3/2} - 3(x+1) + 16\sqrt{x+1} - 48 \ln(\sqrt{x+1}+3) + C$

2. ให้ $u=\sqrt{4x+5}$ จะได้ $u^3 = 4x+5$ หรือ $x = \frac{u^3-5}{4}$ และ $dx = \frac{3u^2 du}{4}$ ดังนั้น
$\int x^2 \sqrt{4x+5} dx = \int \left(\frac{u^3-5}{4}\right) \frac{3u^2 du}{4} = \frac{3}{64} \int u^3 (u^6-10u^3+25) du = \frac{3}{64} \int (u^9-10u^6+25u^3) du$
$= \frac{3}{64} \left[\frac{u^{10}}{10} - \frac{10}{7} u^7 + \frac{25u^4}{4}\right] + C$
$= \frac{3}{64} \left[(4x+5)^{10/3}/10 - \frac{10}{7}(4x+5)^{7/3} + \frac{25}{4}(4x+5)^{4/3}\right] + C$

3. ให้ $u^2 = x + 1$ จะได้ $(x + 1)^{3/2} = (u^2)^{3/2} = u^3$, $(x + 1)^{1/2} = u$ และ $dx = 2udu$ ดังนั้น
$\int \frac{dx}{\sqrt{(x+1)^3} + \sqrt{x+1}} = \int \frac{2udu}{u^3+u} = \int \frac{2udu}{u(u^2+1)} = 2 \int \frac{du}{u^2+1}$
$= 2 \tan^{-1}u+C = 2\tan^{-1}\sqrt{x+1} + C$

ภาควิชาคณิตศาสตร์
43


แบบฝึกหัด 2.1

1. จงหาค่าอินทิกรัลในแต่ละข้อต่อไปนี้ โดยการแทนด้วยตัวแปร $u$ ที่กำหนด
    1.1 $\int \frac{xdx}{1+x}, u = 1+x$
    1.2 $\int \frac{e^x dx}{x^2}, u = \frac{1}{x}$
    1.3 $\int \frac{x^{2}-3}{(x+1)^{4}}dx, u = x+1$
    1.4 $\int \frac{xdx}{1+x^{4}}, u = x^{2}$
    1.5 $\int \frac{dx}{\sqrt{x(1+\sqrt{x})}}, u=1+\sqrt{x}$
    1.6 $\int e^x dx, u = 1+e^x$

2. จงหาค่าอินทิกรัลโดยการแทนด้วยตัวแปร $u$ ที่กำหนดให้ พร้อมตรวจสอบคำตอบ
    2.1 $\int 3(1+3x)^{5} dx, u = 1+3x$
    2.2 $\int \tan \theta \sec^{2} \theta d\theta, u = \tan \theta$
    2.3 $\int \frac{dx}{\sqrt{1-9x^{2}}}, u = 3x$
    2.4 $\int \frac{(lnx)^{4}}{x} dx, u = \ln x$
    2.5 $\int \frac{xdx}{\sqrt{1+x^{2}}}, u = 1+x^{2}$
    2.6 $\int \frac{(2x+3)}{x^{2}+3x+2} dx, u = x^{2}+3x+2$

3. จงหาค่าอินทิกรัลในแต่ละข้อต่อไปนี้ โดยการแทนด้วยตัวแปรตามความเหมาะสม
    3.1 $\int e^{-2x} dx$
    3.2 $\int \cos(ax+b) dx$
    3.3 $\int \sqrt{3x+4} dx$
    3.4 $\int e^{x} \sin(e^{x}) dx$
    3.5 $\int (x+2)(x^{2}+4x+9)^{\frac{1}{3}} dx$
    3.6 $\int (t-1)^{4} (2t-6) dt$
    3.7 $\int_{0}^{\pi/2} x^{3}(x^{2}+1)^{-\frac{1}{2}} dx$
    3.8 $\int e^{2x} \sin(e^{2x}) dx$
    3.9 $\int \sin x e^{\cos x} dx$
    3.10 $\int_{0}^{\pi/2} \sin^{2} x \cos x dx$
    3.11 $\int_{0}^{\sqrt{\pi}} x \cos x^{2} dx$
    3.12 $\int_{0}^{\infty} e^{x} e^{x} dx$
    3.13 $\int \frac{xdx}{(4x+1)^{5}}$
    3.14 $\int \frac{\sin x}{\cos^{3} x} dx$
    3.15 $\int \frac{\cos(\ln x)}{x} dx$
    3.16 $\int_{1/2}^{\sqrt{3}/2} \frac{\sin^{-1} x}{\sqrt{1-x^{2}}} dx$
    3.17 $\int \frac{x}{1+x^{4}} dx$
    3.18 $\int \frac{x}{\sqrt{1-x^{4}}} dx$
    3.19 $\int \frac{x^{3}}{1+x^{4}} dx$
    3.20 $\int \frac{\ln x}{1+(lnx)^{2}} dx$
    3.21 $\int \frac{dx}{2x^{2}+3}$


3.22 $\int_0^{\frac{x^3}{\sqrt{x^2+1}}}\frac{x^3}{\sqrt{x^2+1}}dx$
3.23 $\int_0^x x^2(x^3-19)^3 dx$
3.24 $\int x^2 e^{x^2} dx$
3.25 $\int \frac{dt}{\sqrt{2t+7}}$
3.26 $\int \frac{dx}{2x\sqrt{x-2}}$
3.27 $\int \frac{\sqrt{3x}}{x+5} dx$
3.28 $\int x^2 \sqrt{3x-1} dx$
3.29 $\int x^2 (x-3)^3 dx$
3.30 $\int \frac{\sqrt{x+1+3}}{\sqrt{x+1-1}} dx$

## 2.2 การอินทิเกรตทีละส่วน

ดังได้กล่าวแล้วว่าการอินทิเกรตและการหาอนุพันธ์เป็นการดำเนินการผกผันของกันและกัน ดังนั้นสูตรการหาอนุพันธ์จึงอาจผกผันให้เป็นสูตรของการอินทิเกรตได้ ดังเช่นการอินทิเกรตโดยการแทนดังที่กล่าวแล้วในหัวข้อ 2.1 ก็เป็นสูตรที่ผกผันมาจากกฎลูกโซ่ของอนุพันธ์ ในหัวข้อนี้เราจะให้สูตรการอินทิเกรตที่เรียกว่า **การอินทิเกรตทีละส่วน (integration by parts)** ซึ่งผกผันมาจากกฎผลคูณของการหาอนุพันธ์ ดังนี้

$(f(x)g(x))' = f(x)g'(x) + f'(x)g(x)$

ถ้าเราอินทิเกรตทั้งสองข้างของสมการนี้จะได้

$\int [f(x)g(x)]' dx = \int f(x)g'(x) dx + \int f'(x)g(x) dx$

ค่าทางซ้ายมือของสมการคือ $f(x)g(x)$ เพราะเป็นปฏิยานุพันธ์ของ $(f(x)g(x))'$ และเมื่อจัดพจน์ใหม่ เราจะได้สูตรการอินทิเกรตทีละส่วนดังต่อไปนี้

**สูตรการอินทิเกรตทีละส่วน**
$\int f(x)g'(x) dx = f(x)g(x) - \int g(x)f'(x) dx$

ถ้าเราให้ $u = f(x)$ และ $v = g(x)$ แล้วจะได้ $du = f'(x) dx$ และ $dv = g'(x) dx$ ทำให้ได้สูตรการอินทิเกรตทีละส่วนในรูปตัวแปร $u$ และ $dv$ ดังนี้

**สูตรการอินทิเกรตทีละส่วน**
$\int udv = uv - \int v du$

ขอให้สังเกตว่าในการคำนวณค่าอินทิกรัล $\int v du$ เราอาจจะค่าคงตัวของการอินทิเกรตไว้ก่อนได้ แต่จะนำไปรวมเป็นค่าคงตัวของการอินทิเกรต $\int udv$


ตัวอย่าง 2.2.1 จงหา
1. $\int \ln x dx$
2. $\int x\sqrt{x-1} dx$
3. $\int \cos^{-1} ax dx$

วิธีทำ 1. ให้ $u = \ln x$ และ $dv = dx$ แล้วจะได้ $du = \frac{dx}{x}$ และ $v = x$ ซึ่งทำให้ได้
$\int \ln x dx = x \ln x - \int x \ln x dx = x \ln x - \int x \ln x dx + C$

2. ให้ $u = x$ และ $dv = \sqrt{x-1} dx$
    แล้วจะได้ $du = dx$ และ $v = \int \sqrt{x-1} dx = \int \sqrt{x-1} d(x-1) = \frac{2}{3}(x-1)^{\frac{3}{2}}$
    เพราะฉะนั้น
    $\int x\sqrt{x-1} dx = \frac{2x}{3}(x-1)^{\frac{3}{2}} - \int \frac{2}{3}(x-1)^{\frac{3}{2}} dx$
    $= \frac{2x}{3}(x-1)^{\frac{3}{2}} - \frac{2}{3} \cdot \frac{(x-1)^{\frac{5}{2}}}{\frac{5}{2}}(x-1) + C$
    $= \frac{2x}{3}(x-1)^{\frac{3}{2}} - \frac{4}{5}(x-1)^{\frac{5}{2}} + C$

[ขอให้สังเกตว่าเราอาจอินทิเกรต $\int x\sqrt{x-1} dx$ ด้วยเทคนิคการอินทิเกรตโดยการแทนได้เช่นกัน โดยให้ $u = \sqrt{x-1}$ หรือ $u^2 = x-1]$
3. สังเกตว่า $\frac{d}{dx} \cos^{-1} ax = -\frac{1}{\sqrt{1-(ax)^2}} \frac{d}{dx} (\cos^{-1} ax)$
    $= -\frac{a}{\sqrt{1-(ax)^2}}$

และเราสามารถหาอินทิกรัล $\int \frac{ax}{\sqrt{1-(ax)^2}} dx$ ได้ เราจึงควรเลือก $u = \cos^{-1} ax$ และ $dv = dx$
ซึ่งทำให้ได้ $du = -\frac{adx}{\sqrt{1-(ax)^2}}$ และ $v = x$ เพราะฉะนั้น
$\int \cos^{-1} ax dx = x \cos^{-1} ax + \int \frac{ax}{\sqrt{1-(ax)^2}} dx$
$= x \cos^{-1} ax + \frac{ax}{\sqrt{1-(ax)^2}}$
$= x \cos^{-1} ax - \frac{1}{2a} \frac{d}{dx} \left( \frac{1-a^2 x^2}{\sqrt{1-a^2 x^2}} \right)$
$= x \cos^{-1} ax - \frac{1}{2a} \frac{d}{dx} \left( \frac{1-a^2 x^2}{\sqrt{1-a^2 x^2}} \right) + C$

ด้วยวิธีการเดียวกับการอินทิเกรตฟังก์ชัน arc cos ของตัวอย่าง 2.2.1 ข้อ 3 เราสามารถ อินทิเกรตฟังก์ชันตรีโกณมิติผกผันได้ทั้งหมด ให้ผู้อ่านฝึกทำเป็นแบบฝึกหัด

ตัวอย่าง 2.2.2 จงหา
1. $\int xe^x dx$
2. $\int x^2 e^x dx$

วิธีทำ 1. ให้ $u = x$ และ $dv = e^x dx$ ซึ่งจะได้ $du = dx$ และ $v = \int e^x dx = e^x$ เพราะฉะนั้น
46


$$ \int x e^x dx = x e^x - \int e^x dx = x e^x - e^x + C $$

2. ให้ $u = x^2$ และ $dv = e^x dx$ จะได้ $du = 2x dx$ และ $v = \int e^x dx = e^x$
เพราะฉะนั้น
$$ \int x^2 e^x dx = x^2 e^x - 2 \int x e^x dx $$
และจากตัวอย่าง 2.2.2 ข้อ 1 ซึ่งแสดงแล้วว่า $\int x e^x dx = x e^x - e^x + C$ ดังนั้น
$$ \int x^2 e^x dx = x^2 e^x - 2x e^x + 2e^x + C $$

ขอให้สังเกตว่าบางครั้งเราต้องทำการอินทิเกรตทีละส่วนมากกว่า 1 ครั้ง อย่างไรก็ตาม การเลือก $u$ และ $dv$ จะต้องทำให้ได้อินทิกรัลที่เกิดใหม่มีรูปแบบในทางที่ดีขึ้น เช่นการเลือกใน ตัวอย่างข้างต้น เราได้อินทิกรัลที่มีกำลังของ $x$ ลดลง แต่ในทางตรงกันข้ามหากเราเปลี่ยนการ เลือกเป็น $u = e^x$ และ $dv = x^2 dx$ แล้วจะได้ $du = e^x dx$ (รูปแบบไม่เปลี่ยน) และ $v = \frac{x^3}{3}$ (กำลังเพิ่มขึ้น) ดังนั้น
$$ \int x^2 e^x dx = \frac{x^3}{3} e^x - \int \frac{x^3}{3} e^x dx $$
ซึ่งอินทิกรัล $\int x^3 e^x dx$ อยู่ในรูปแบบที่ยุ่งยากกว่าอินทิกรัลเดิม $\int x^2 e^x dx$ ดังนั้นเราจึงไม่ควร เลือก $u$ และ $dv$ แบบที่กล่าวทีหลัง

ตัวอย่าง 2.2.3 จงหา $\int x^n \ln x dx$ เมื่อ $n \neq -1$

วิธีทำ เราควรเลือกให้ $u = \ln x$ และ $dv = x^n dx$ ซึ่งทำให้ได้ $du = \frac{dx}{x}$ และ $v = \frac{x^{n+1}}{n+1}$ ดังนั้น
$$
\begin{align*}
\int x^n \ln x dx  &= \frac{x^{n+1} \ln x}{n+1} - \frac{1}{n+1} \int x^{n+1} dx = \frac{x^{n+1} \ln x}{n+1} - \frac{1}{n+1} \cdot \frac{x^{n+2}}{n+2} + C \\[0.5em]
&= \frac{x^{n+1} \ln x}{n+1} - \frac{x^{n+2}}{(n+1)(n+2)} + C
\end{align*}
$$

สังเกตว่าการเลือก $dv$ เป็นพหุนาม $x^n$ ของการหาอินทิกรัล $\int x^n \ln x dx$ แม้จะทราบว่า เมื่ออินทิเกรต $dv$ แล้วจะได้ $v$ ในรูปกำลังของ $x$ ที่เพิ่มขึ้น แต่เมื่อแทนค่ากลับจะได้ $\int x^n dx$ ซึ่ง เป็นอินทิกรัลของพหุนามใน $x$ เท่านั้นเพราะอนุพันธ์ของฟังก์ชันลอการิทึมเปลี่ยนรูป

จากตัวอย่างต่าง ๆ ดังกล่าวข้างต้น เราจึงสรุปเป็นหลักสังเกตการเลือก $u$ และ $dv$ ได้ ดังนี้


หลักสังเกตการเลือก $u$ และ $dv$
สังเกตว่าฟังก์ชันที่ต้องการอินทิเกรตหรือฟังก์ชันที่ต้องการหาอนุพันธ์ควรมีรูปแบบคงเดิม เช่น ฟังก์ชันเชิงกำลัง ฟังก์ชันตรีโกณมิติเป็นต้น เรายินยมเลือกให้เป็น $dv$ ในขณะที่ฟังก์ชันพหุนาม เมื่อหาอนุพันธ์แล้วกำลังลดลง แต่เมื่อทำการอินทิเกรตจะได้กำลังเพิ่มขึ้น หรือฟังก์ชันลอการิทึมจะเปลี่ยนรูป เป็นพหุนามเมื่อหาอนุพันธ์ และทำการอินทิเกรตโดยตรงได้ยาก เราจึงนิยมเลือกให้ฟังก์ชันเหล่านี้เป็น $u$

ตัวอย่าง 2.2.4 จงหาอินทิกรัลในข้อต่อไปนี้ เมื่อ $n > 0$
1. $\int x^n e^{ax} dx$
2. $\int x^n \cos ax dx$

วิธีทำ 1. จากหลักสังเกตการเลือก $u$ และ $dv$ เราจึงเลือกให้ $u = x^n$ และ $dv = e^{ax}$ ซึ่งทำให้ได้ $du = nx^{n-1} dx$ และด้วยการอินทิเกรตโดยการแทนกับ $\int e^{ax} dx$ เราจะได้ $v = \frac{e^{ax}}{a}$ เพราะฉะนั้น
$\int x^n e^{ax} dx = \frac{x^n e^{ax}}{a} - \frac{n}{a} \int x^{n-1} e^{ax} dx$ (2.2.1)

2. เราจะเลือกให้ $u = x^n$ และ $dv = \cos ax dx$ แล้วได้ $du = nx^{n-1} dx$ และด้วยการอินทิเกรตโดยการแทนกับ $\int \cos ax dx$ จะได้ $v = \frac{1}{a} \sin ax$ เพราะฉะนั้น
$\int x^n \cos ax dx = \frac{1}{a} x^n \sin ax - \frac{n}{a} \int x^{n-1} \sin ax dx$ (2.2.2)
O

หมายเหตุ เราเรียกสมการที่เขียนได้ในรูปลดทอนกำลังจาก $n$ เป็น $n-1$ เช่นเดียวกับสมการ (2.2.1) และ (2.2.2) ว่า สูตรลดทอน (reduction formulas)

ตัวอย่างต่อไปจะแสดงการอินทิเกรตทีละส่วนกับอินทิกรัลที่มีอินทิแกรนด์อยู่ในรูปผลคูณของสองฟังก์ชันซึ่งต่างก็มีรูปแบบคงเดิมไม่ว่าจะทำการอินทิเกรตหรือหาอนุพันธ์

ตัวอย่าง 2.2.5 จงหา $\int e^x \cos x dx$

วิธีทำ ลองให้ $u = e^x$ และ $dv = \cos x dx$ จะได้ $du = e^x dx$ และ $v = \sin x$ เพราะฉะนั้น
$\int e^x \cos x dx = e^x \sin x - \int e^x \sin x dx$

ภาควิชาคณิตศาสตร์
48


(สังเกตว่า $\int e^x \sin x dx$ เป็นอินทิกรัลที่ไม่ได้มีรูปแบบที่ดีขึ้นหรือแย่ลงกว่า $\int e^x \cos x dx$ แต่เมื่อพิจารณาให้ดีจะพบว่า ถ้าเราอินทิเกรต $\int e^x \sin x dx$ โดยการอินทิเกรตทีละส่วนอีกครั้งด้วยการสมมติในลักษณะเดิมแล้วจะได้อินทิกรัล $\int e^x \cos x dx$ กลับคืนมาในลักษณะที่มีเครื่องหมายตรงกันข้าม)
ต่อไปอินทิเกรต $\int e^x \sin x dx$ โดยให้ $u = e^x$ และ $dv = \sin x dx$ ซึ่งจะได้ $du = e^x dx$ และ $v = -\cos x$ แล้วได้
$$ \int e^x \sin x dx = -e^x \cos x + \int e^x \cos x dx $$

เพราะฉะนั้น
$$ \int e^x \cos x dx = e^x \sin x + e^x \cos x - \int e^x \cos x dx $$

ซึ่งสมมูลกับ
$$ 2 \int e^x \cos x dx = e^x \sin x + e^x \cos x + C_1 $$

ทำให้ได้
$$ \int e^x \cos x dx = \frac{e^x}{2} (\sin x + \cos x) + C $$

(เมื่อ $C = \frac{C_1}{2}$)

O

การอินทิเกรตของตัวอย่าง 2.2.5 เป็นวิธีการเฉพาะอันหนึ่ง กล่าวคือเมื่ออินทิเกรตทีละส่วนแล้วได้อินทิกรัลในรูปแบบที่ไม่ดีขึ้นหรือแย่ลงกว่าเดิมและเมื่ออินทิเกรตทีละส่วนซ้ำอีกครั้งหนึ่งกลับได้อินทิกรัลเดิมปรากฏขึ้น แต่ขอให้สังเกตว่าเครื่องหมายจะต้องตรงข้ามกับอินทิกรัลเดิม
หากในตัวอย่าง 2.2.5 เราเลือกให้ $u = \cos x$ และ $dv = e^x dx$ สำหรับอินทิกรัล $\int e^x \cos x dx$ เราจะได้
$$ \int e^x \cos x dx = e^x \sin x - e^x \sin x + \int e^x \cos x dx $$

ซึ่งจะทำให้ได้ $0 = 0$ ไม่เกิดประโยชน์อย่างใด จึงสังเกตว่าสำหรับอินทิกรัลที่มีอินทิแกรนด์ลักษณะเช่นนี้ เมื่อจะอินทิเกรตซ้ำต้องสมมติ $u$ และ $dv$ ในครั้งหลังให้เป็นลักษณะเดียวกับการสมมติในครั้งแรกเสมอ

ตัวอย่างต่อไปนี้แสดงวิธีการหาโดยใช้เทคนิคการอินทิเกรตทีละส่วนของอินทิกรัลจำกัดเขต

**ตัวอย่าง 2.2.6** จงหาอินทิกรัลจำกัดเขตต่อไปนี้
1. $\int_0^{\pi/2} x \sin 2x dx$
2. $\int_0^{\pi/3} x \tan^2 x dx$
3. $\int_0^4 e^{x} dx$

**วิธีทำ 1.** ให้ $u = x$ และ $dv = \sin 2x$ แล้วจะได้
$du = dx$ และ $v = \frac{1}{2} \int \sin 2x d(2x) = -\frac{1}{2} \cos 2x$ ทำให้ได้

ภาควิชาคณิตศาสตร์
49


$$
\begin{align*}
\int_0^{\pi/2} x \sin 2x \, dx  &= \left[ -\frac{x \cos 2x}{2} \right]_0^{\pi/2} - \left( -\frac{1}{2} \int_0^{\pi/2} \cos 2x \, dx \right) \\[0.5em]
&= \left[ -\frac{x \cos 2x}{2} \right]_0^{\pi/2} + \left[ \frac{\sin 2x}{4} \right]_0^{\pi/2} = -\frac{\pi \cos \pi}{4} + \left( \frac{\sin \pi}{4} - \frac{\sin 0}{4} \right) \\[0.5em]
\int_0^{\pi/2} x \sin 2x \, dx  &= \frac{\pi}{4}
\end{align*}
$$

2. $$
\int_0^{\pi/3} x \tan^2 x \, dx = \int_0^{\pi/3} x (\sec^2 x - 1) \, dx = \int_0^{\pi/3} x \sec^2 x \, dx - \int_0^{\pi/3} x \, dx
$$

แล้วประยุกต์เทคนิคการอินทิเกรตทีละส่วนกับ $\int_0^{\pi/3} x \sec^2 x \, dx$ ดังนี้

ให้ $u = x$ และ $dv = \sec^2 x \, dx$ แล้วได้ $du = dx$ และ $v = \sec^2 x \, dx$ จึงได้

$$
\begin{align*}
\int_0^{\pi/3} x \sec^2 x \, dx  &= \left[ x \tan x \right]_0^{\pi/3} - \int_0^{\pi/3} \tan x \, dx = \left[ x \tan x \right]_0^{\pi/3} - \left[ \ln |\sec x| \right]_0^{\pi/3} \\[0.5em]
&= \frac{\pi}{3} \tan \frac{\pi}{3} - \ln |\sec \frac{\pi}{3}| - \ln | \sec 0 | = \frac{\sqrt{3}}{3} \pi - \ln 2 - \ln 1 \\[0.5em]
&= \frac{\sqrt{3}}{3} \pi - \ln 2
\end{align*}
$$

เพราะฉะนั้น

$$
\begin{align*}
\int_0^{\pi/3} x \tan^2 x \, dx  &= \frac{\sqrt{3}}{3} \pi - \ln 2 - \int_0^{\pi/3} x \sec^2 x \, dx = \frac{\sqrt{3}}{3} \pi - \ln 2 - \left[ \frac{x^2}{2} \right]_0^{\pi/3} \\[0.5em]
&= \frac{\sqrt{3}}{3} \pi - \ln 2 - \frac{(\pi/3)^2}{2} = \frac{\sqrt{3}}{3} \pi - \ln 2 - \frac{\pi^2}{18}
\end{align*}
$$

3. เราจะประยุกต์เทคนิคการอินทิเกรตโดยการแทนก่อนการใช้เทคนิคการอินทิเกรตทีละ ส่วน โดยให้ $t = \sqrt{x}$ ซึ่งจะได้ $dt = \frac{dx}{2 \sqrt{x}}$ และเพราะ $0 \leq x \leq 4$ ทำให้ได้ $0 \leq \sqrt{x} \leq 2$ ดังนั้น

$$ \int e^{\sqrt{x}} dx = 2 \int te^{t} dt $$

ซึ่งเราจะประยุกต์เทคนิคการอินทิเกรตทีละส่วนกับ $\int te^{t} dt$ และโดยตัวอย่าง

2.2.2 ข้อ 1 เราจะได้

$$ \int e^{\sqrt{x}} dx = 2 \int te^{t} dt = 2 \left[ te^{t} - e^{t} \right]_0^2 = 2 \left[ (2e^2 - e^2) - (0 - e^0) \right]_0^2 = 2(e^2 + 1) $$

แบบฝึกหัด 2.2

1. จงหาอินทิกรัลในแต่ละข้อต่อไปนี้ โดยการอินทิเกรตทีละส่วน

50


2. จงพิจารณาว่าจะใช้เทคนิคใดในการหาอินทิกรัล ในแต่ละข้อต่อไปนี้

2.1 $\int \sqrt{4x^2 - 36} dx$
2.2 $\int e^{2x^3 + 3x} (2x^2 + 1) dx$
2.3 $\int xe^x dx$

2.4 $\int x \tan^{-1} x dx$
2.5 $\int x (3x+5)^{10} dx$
2.6 $\int e^{ax} \sin bx dx$

2.7. $\int (\ln x)^n dx$
2.8 $\int x^2 \ln(x) dx$

3. จงหาอินทิกรัลต่อไปนี้

3.1 $\int \sin \sqrt{x} dx$
3.2 $\int \sin \frac{\sqrt[3]{x}}{3} dx$
3.3 $\int e^{\sqrt[2]{x}} dx$

ข้อแนะนำ: อาจใช้เทคนิคการแทนรวมกับเทคนิคการอินทิเกรตทีละส่วน

4. จงแสดงว่า $\int \sin(\ln x) dx = \frac{x}{2} [\sin(\ln x) - \cos(\ln x)]$

ข้อแนะนำ: ให้ $u = x$ และ $dv = \frac{\sin(\ln x)}{x} dx$

## 2.3 การอินทิเกรตฟังก์ชันตรีโกณมิติ

ในหัวข้อนี้ เราจะแสดงการอินทิเกรตฟังก์ชันตรีโกณมิติ โดยใช้เอกลักษณ์ตรีโกณมิติเข้ามาช่วย ซึ่งเราจะแบ่งฟังก์ชันในรูปผลคูณของฟังก์ชันตรีโกณมิติออกได้เป็น 3 รูปแบบคือ

$\cos^n \theta \sin^n \theta$ หรือ $\tan^n \theta \sec^n \theta$ หรือ $\cot^n \theta \csc^n \theta$

(หมายเหตุ: สำหรับในบทนี้ให้ $k$ แทนจำนวนเต็มใด ๆ)

2.3.1 การหา $\int \cos^n \theta \sin^n \theta d\theta$

2.3.1.1 ถ้า $m$ หรือ $n$ เป็นจำนวนคี่ เราจะใช้ความสัมพันธ์

ภาควิชาคณิตศาสตร์
51


$$ d(\sin \theta)=\cos \theta d\theta \quad \text{หรือ} \quad d(\cos \theta)=-\sin \theta d\theta $$
แปลงอินทิกรัลดังนี้

$$
\begin{align*}
\int \cos ^ { m } \theta \sin ^ { 2 k + 1 } \theta d\theta  &= \int \cos ^ { m } \theta \sin ^ { 2 k } \theta (\sin \theta d\theta ) = - \int \cos ^ { m } \theta \sin ^ { 2 k } \theta d(\cos \theta) \\[0.5em]
&= - \int \cos ^ { m } \theta ( 1 - \cos ^ { 2 } \theta ) ^ { k } d( \cos \theta)
\end{align*}
$$

(ใช้สูตร $\sin ^ { 2 } \theta = 1 - \cos ^ { 2 } \theta$)

(สังเกตว่าอินทิกรัลเปลี่ยนเป็นรูปพหุนามของ $\cos \theta$ หรือในรูป $\int x ^ { m } ( 1 - x ^ { 2 } ) ^ { k } dx$ เมื่อให้ $x = \cos \theta$)
หรือ

$$
\begin{align*}
\int \cos ^ { 2 k + 1 } \theta \sin ^ { n } \theta d\theta  &= \int \cos ^ { 2 k } \theta \sin ^ { n } \theta (\cos \theta d\theta ) = \int \cos ^ { 2 k } \theta \sin ^ { n } \theta d( \sin \theta) \\[0.5em]
&= \int ( 1 - \sin ^ { 2 } \theta ) ^ { k } \sin ^ { n } \theta d( \sin \theta)
\end{align*}
$$

(ใช้สูตร $\cos ^ { 2 } \theta = 1 - \sin ^ { 2 } \theta$)

(สังเกตว่าอินทิกรัลเปลี่ยนเป็นรูปพหุนามของ $\sin \theta$ หรือในรูป $\int x ^ { m } ( 1 - x ^ { 2 } ) ^ { k } dx$ เมื่อให้ $x = \sin \theta$)

**ตัวอย่าง 2.3.1** จงหาอินทิกรัลของฟังก์ชันตรีโกณมิติ ต่อไปนี้

1.  $\int \sin ^ { 5 } \theta d\theta$

2.  $\int _ { \pi / 6 } ^ { \pi / 3 } \cos ^ { 3 } \theta \sqrt { \sin \theta } d\theta$

วิธีทำ 1. $\int \sin ^ { 5 } \theta d\theta = \int \sin ^ { 4 } \theta \sin \theta d\theta = - \int ( 1 - \cos ^ { 2 } \theta ) ^ { 2 } d( \cos \theta)$

$$ = - \cos \theta + \frac { 2 } { 3 } \cos ^ { 3 } \theta - \frac { \cos ^ { 5 } \theta } { 5 } + C $$

2.  $\int \cos ^ { 3 } \theta \sqrt { \sin \theta } d\theta = \int _ { \pi / 6 } ^ { \pi / 3 } \cos ^ { 2 } \theta \sqrt { \sin \theta } \cos \theta d\theta = \int _ { \pi / 6 } ^ { \pi / 3 } ( 1 - \sin ^ { 2 } \theta ) \sqrt { \sin \theta } d( \sin \theta)$

$$
\begin{align*}
 &= \int _ { \pi / 6 } ^ { \pi / 3 } \left[ \sqrt { \sin \theta } - \sin ^ { 5 } \theta \right] d( \sin \theta ) = \left[ \frac { 2 } { 3 } \sin ^ { 3 } \theta - \frac { 2 } { 7 } \sin ^ { 5 } \theta \right] _ { \pi / 6 } ^ { \pi / 3 } \\[0.5em]
&= \left[ \frac { 2 } { 3 } \left( \frac { \sqrt { 3 } } { 2 } \right) ^ { 3 / 2 } - \frac { 2 } { 7 } \left( \frac { \sqrt { 3 } } { 2 } \right) ^ { 5 / 2 } \right] - \left[ \frac { 2 } { 3 } \left( \frac { \pi } { 6 } \right) ^ { 7 / 2 } - \frac { 2 } { 7 } \left( \frac { \pi } { 6 } \right) ^ { 7 / 2 } \right] \\[0.5em]
&= \left[ \frac { 2 } { 3 } \left( \frac { \sqrt { 3 } } { 2 } \right) ^ { 3 / 2 } - \frac { 2 } { 7 } \left( \frac { \sqrt { 3 } } { 2 } \right) ^ { 5 / 2 } \right] - \left[ \frac { 2 } { 3 } \left( \frac { \pi } { 6 } \right) ^ { 7 / 2 } - \frac { 2 } { 7 } \left( \frac { \pi } { 6 } \right) ^ { 7 / 2 } \right]
\end{align*}
$$

ภาคผนวก คณิตศาสตร์ วิชาวิทยาศาสตร์และเทคโนโลยี สำหรับการศึกษาในระดับมัธยมศึกษาตอนปลาย พุทธศักราช ๒๕๖๓
52


2.3.1.2 ถ้า $m$ และ $n$ ต่างเป็นจำนวนคู่ เราจะแปลงอินทิกรัลโดยใช้เอกลักษณ์ตรีโกณมิติ

ทำให้ได้
$$ \int \cos^{2k} \theta \sin^{2p} \theta d\theta = \int (\cos^2 \theta)^k (\sin^2 \theta)^p d\theta = \int \left(\frac{1+\cos2\theta}{2}\right)^k \left(\frac{1-\cos2\theta}{2}\right)^p d\theta $$

และจะได้อินทิกรัลอยู่ในรูปกำลังต่าง ๆ ของ $\cos2\theta$

ตัวอย่าง 2.3.2 จงหาอินทิกรัลของฟังก์ชันตรีโกณมิติ ต่อไปนี้
1. $\int_0^\pi \sin^2 \theta d\theta$
2. $\int \cos^2 \theta \sin^4 \theta d\theta$
3. $\int \cos^6 \theta d\theta$

วิธีทำ 1.
$$ \int_0^\pi \sin^2 \theta d\theta = \int_0^\pi \left(\frac{1-\cos2\theta}{2}\right) d\theta = \frac{1}{2} \int_0^\pi d\theta - \int_0^\pi \cos2\theta d\theta $$
เพราะว่า $\int \cos2\theta d\theta = \frac{1}{2} \int \cos2\theta d(2\theta) = \frac{\sin2\theta}{2} + C$ ดังนั้น
$$ \int_0^\pi \sin^2 \theta d\theta = \frac{1}{2} \left[ \frac{\sin2\theta}{2} \right]_0^\pi = \left[ \frac{\theta}{2} - \frac{\sin2\theta}{4} \right]_0^\pi = \left[ \frac{\pi}{2} - \frac{\sin2\pi}{4} \right] - \left[ 0 - \frac{\sin0}{4} \right] = \frac{\pi}{2} $$

2. $\int \cos^2 \theta \sin^4 \theta d\theta = \int \left(\frac{1+\cos2\theta}{2}\right)\left(\frac{1-\cos2\theta}{2}\right)^2 d\theta$
$$
\begin{align*}
 &= \int \left(\frac{1+\cos2\theta}{2}\right)\left(\frac{1-\cos2\theta}{2}\right)\left(\frac{1-\cos2\theta}{2}\right) d\theta \\[0.5em]
&= \frac{1}{8} \int (1-\cos2\theta-\cos^22\theta+\cos^32\theta)d\theta \\[0.5em]
&= \frac{1}{8} \left[ \theta - \frac{\sin2\theta}{2} - \int \left(\frac{1+\cos4\theta}{2}\right) d\theta + \frac{1}{2} \int (1-\sin^22\theta)d(\sin2\theta) \right] \\[0.5em]
&= \frac{1}{8} \left[ \theta - \frac{\sin2\theta}{2} - \frac{\sin4\theta}{2} + \frac{\sin2\theta}{2} - \frac{\sin32\theta}{6} \right] + C
\end{align*}
$$

53


$$ \int \cos ^ { 2 } \theta \sin ^ { 4 } \theta d\theta = \frac { 1 } { 8 } \left[ \frac { \theta } { 2 } - \frac { \sin 4\theta } { 8 } - \frac { \sin ^ { 3 } 2\theta } { 6 } \right] + C $$

3. $ \int \cos ^ { 6 } \theta d\theta = \int \left( \frac { 1 + \cos 2\theta } { 2 } \right)^3 d\theta = \frac { 1 } { 8} \int \left( 1 + 3 \cos 2\theta + 3 \cos ^ { 2 } 2\theta + \cos ^ { 3 } 2\theta \right) d\theta $
$$
\begin{align*}
 &= \frac { 1 } { 8} \left[ \theta + \frac { 3 } { 2 } \sin 2\theta + 3 \left( \frac { 1 + \cos 4\theta } { 2 } \right) \theta + \frac { 1 } { 2 } \int \left( 1 - \sin ^ { 2 } 2\theta \right) d ( \sin 2\theta ) \right] + C \\[0.5em]
&= \frac { 1 } { 8} \left[ \theta + \frac { 3 } { 2 } \sin 2\theta + \frac { 3 } { 2 } \theta + \frac { 3 } { 8 } \sin 4\theta + \frac { \sin 2\theta } { 2 } - \frac { \sin ^ { 3 } 2\theta } { 6 } \right] + C \\[0.5em]
&= \frac { 1 } { 8} \left[ \frac { 5 } { 2 } \theta + 2 \sin 2\theta + \frac { 3 } { 8 } \sin 4\theta - \frac { \sin ^ { 3 } 2\theta } { 6 } \right] + C
\end{align*}
$$

2.3.1.3 กรณีที่ $n$ หรือ $n$ จำนวนหนึ่งเป็นศูนย์และอีกจำนวนหนึ่งมีค่ามาก เราจะใช้การอินทิเกรตที่ละส่วนเพื่อสร้างสูตรลดทอนสำหรับ $\int \sin ^ { n } \theta d\theta$ และ $\int \cos ^ { n } \theta d\theta$ ดังนี้ให้ $u = \sin ^ { n - 1 } \theta$ และ $dv = \sin \theta d\theta$ เราจะได้ $du = (n-1) \sin ^ { n - 2 } \theta \cos \theta d\theta$ และ $v = - \cos \theta$ ดังนั้น
$$
\begin{align*}
\int \sin ^ { n } \theta d\theta  &= - \cos \theta \sin ^ { n - 1 } \theta + (n-1) \int \cos ^ { 2 } \theta \sin ^ { n - 2 } \theta d\theta \\[0.5em]
&= - \cos \theta \sin ^ { n - 1 } \theta + (n-1) \int \left( 1 - \sin ^ { 2 } \theta \right) \sin ^ { n - 2 } \theta d\theta \\[0.5em]
&= - \cos \theta \sin ^ { n - 1 } \theta + (n-1) \int \sin ^ { n - 2 } \theta d\theta - (n-1) \int \sin ^ { n } \theta d\theta
\end{align*}
$$
หรือ
$$ n \int \sin ^ { n } \theta d\theta = - \cos \theta \sin ^ { n - 1 } \theta + (n-1) \int \sin ^ { n - 2 } \theta d\theta $$
เพราะฉะนั้น
$$ \int \sin ^ { n } \theta d\theta = \frac { - \cos \theta \sin ^ { n - 1 } \theta } { n } + \frac { n - 1 } { n } \int \sin ^ { n - 2 } \theta d\theta ; n \geq 2 $$
ในทำนองเดียวกันเราก็จะได้
$$ \int \cos ^ { n } \theta d\theta = \frac { \sin \theta \cos ^ { n - 1 } \theta } { n } + \frac { n - 1 } { n } \int \cos ^ { n - 2 } \theta d\theta ; n \geq 2 $$


ตัวอย่าง 2.3.3 จงหาอินทิกรัลของฟังก์ชันตรีโกณมิติ ต่อไปนี้ด้วยการประยุกต์สูตรลดทอน

1. $\int \cos^5 \theta d\theta$
2. $\int \sin^8 \theta d\theta$

วิธีทำ 1. $\int \cos^5 \theta d\theta = \frac{\sin\theta\cos^4\theta}{5} + \frac{4}{5}\int \cos^3 \theta d\theta$
$= \frac{\sin\theta\cos^4\theta}{5} + \frac{4}{5} \left[ \frac{\sin\theta\cos^2\theta}{3} + \frac{2}{3} \int \cos\theta d\theta \right]$
$= \frac{\sin\theta\cos^4\theta}{5} + \frac{4}{5} \left[ \frac{\sin\theta\cos^2\theta}{3} + \frac{2}{3} (\cos\theta) \right] + C$
$= \frac{\sin\theta\cos^4\theta}{5} + \frac{4\sin\theta\cos^2\theta}{15} + \frac{8\sin\theta}{15} + C$

2. $\int \sin^8 \theta d\theta = \frac{-\cos\theta\sin^7\theta}{8} + \frac{7}{8} \int \sin^6 \theta d\theta$
$= -\frac{\cos\theta\sin^7\theta}{8} + \frac{7}{8} \left( -\frac{\cos\theta\sin^5\theta}{6} + \frac{5}{6} \int \sin^4 \theta d\theta \right)$
$= -\frac{\cos\theta\sin^7\theta}{8} + \frac{7}{8} \left( -\frac{\cos\theta\sin^5\theta}{6} + \frac{5}{6} \left( -\frac{\cos\theta\sin^3\theta}{4} + \frac{3}{4} \int \sin^2 \theta d\theta \right) \right)$
$= -\frac{\cos\theta\sin^7\theta}{8} + \frac{7}{8} \left( -\frac{\cos\theta\sin^5\theta}{6} + \frac{5}{6} \left( -\frac{\cos\theta\sin^3\theta}{4} + \frac{3}{4} (\cos\theta) \right) \right) + C$

2.3.2 การหา $\int \tan^n \theta \sec^n \theta d\theta$
จากเอกลักษณ์ตรีโกณมิติและความสัมพันธ์ของสูตรอนุพันธ์ของฟังก์ชัน tan และ sec ดังนี้
$\tan^2 \theta = \sec^2 \theta - 1$, $d(\tan \theta) = \sec^2 \theta d\theta$ และ $d(\sec \theta) = \sec\theta\tan\theta d\theta$
เราจะหา $\int \tan^n \theta \sec^n \theta d\theta$ ได้ 2 กรณีคือ

**กรณีที่ 1:** ให้ $u = \tan \theta$, $du = d(\tan \theta) = \sec^2 \theta d\theta$
และ $dv = \sec^n \theta$, $v = \sec^{n+1} \theta / (n+1)$
ดังนั้น $\int \tan^n \theta \sec^n \theta d\theta = \tan^n \theta \cdot \sec^{n+1} \theta / (n+1) - \int \sec^{n+1} \theta d\theta$
$= \tan^n \theta \cdot \sec^{n+1} \theta / (n+1) - \sec^{n+2} \theta / n$

**กรณีที่ 2:** ให้ $u = \sec \theta$, $du = d(\sec \theta) = \sec\theta\tan\theta d\theta$
และ $dv = \tan^n \theta$, $v = \tan^{n+1} \theta / (n+1)$
ดังนั้น $\int \tan^n \theta \sec^n \theta d\theta = \sec^{n+1} \theta \cdot \tan^{n+1} \theta / (n+1) - \int \tan^{n+1} \theta d\theta$
$= \sec^{n+1} \theta \cdot \tan^{n+1} \theta / (n+1) - \tan^{n+2} \theta / n$


ตัวอย่าง 2.3.4 จงอินทิเกรตฟังก์ชันที่อยู่ในรูปผลคูณของ tan กับ sec ในข้อต่อไปนี้

1. $\int \sec^8 \theta d\theta$
2. $\int \frac{\sec^4 \theta}{\sqrt{\tan \theta}} d\theta$
3. $\int \tan^5 (2\theta)\sec^3 (2\theta) d\theta$

วิธีทำ
1. $\int \sec^8 \theta d\theta = \int \sec^6 \theta \sec^2 \theta d\theta = \int (\sec^2 \theta)^3 d(\tan \theta) = \int (\tan^2 \theta +1)^3 d(\tan \theta)$
$= \int (\tan^6 \theta + 3\tan^4 \theta + 3\tan^2 \theta + 1)d(\tan \theta)$
$\int \sec^8 \theta d\theta = \frac{\tan^7 \theta}{7} + \frac{3}{5}\tan^5 \theta + \tan^3 \theta + \tan \theta + C$

2. $\int \frac{\sec^4 \theta}{\sqrt{\tan \theta}} d\theta = \int \frac{\sec^2 \theta}{\sqrt{\tan \theta}} \sec^2 \theta d\theta = \int \frac{(\tan^2 \theta +1)}{\sqrt{\tan \theta}} d(\tan \theta)$
$= \int (\tan^{3/2} \theta + \tan^{-1/2} \theta)d(\tan \theta) = \frac{2}{5}\tan^{5/2} \theta + 2\sqrt{\tan \theta} + C$

3. $\int \tan^5 (2\theta)\sec^3 (2\theta) d\theta = \frac{1}{2} \int \tan^4 (2\theta)\sec^2 (2\theta) d(2\theta)$
$= \frac{1}{2} \left[ \sec^2 (2\theta) - 1 \right] \sec^2 (2\theta) d(2\theta)$
$= \frac{1}{2} \left[ \sec^4 (2\theta) - 2\sec^2 (2\theta) + 1 \right] \sec^2 (2\theta) d(2\theta)$
$\int \tan^5 (2\theta)\sec^3 (2\theta) d\theta = \frac{1}{2} \left[ \sec^5 (2\theta) - 2\sec^3 (2\theta) + \sec^2 (2\theta) + \sec^2 (2\theta) \right] d(2\theta)$
$= \frac{1}{2} \left[ \frac{5}{23} \sec^5 (2\theta) - \frac{10}{13} \sec^3 (2\theta) + \frac{13}{3} \sec^2 (2\theta) \right] + C$

เราสามารถหาสูตรลดทอนสำหรับ $\int \tan^n \theta d\theta$ ได้ดังนี้
$\int \tan^n \theta d\theta = \int \tan^{n-2} \theta \tan^2 \theta d\theta = \int \tan^{n-2} \theta (\sec^2 \theta -1) d\theta$
$= \int \tan^{n-2} \theta \sec^2 \theta d\theta - \int \tan^{n-2} \theta d\theta = \int \tan^{n-2} \theta d(\tan \theta) - \int \tan^{n-2} \theta d\theta$
เพราะฉะนั้น
$$ \int \tan^n \theta d\theta = \frac{\tan^{n-1} \theta}{n-1} - \int \tan^{n-2} \theta d\theta $$ เมื่อ $n \geq 2$

สำหรับสูตรลดทอนของ $\int \sec^n \theta d\theta$ เราใช้การอินทิเกรตทีละส่วน โดยให้
$u = \sec^{n-2} \theta$ และ $dv = \sec^2 \theta d\theta$
แล้วได้ $du = (n-2)\sec^{n-2} \theta \tan \theta d\theta$ และ $v = \tan \theta$ ดังนั้น

ภาควิชา คณิตศาสตร์
56


$$ \begin{align*}\int \sec^n\theta d\theta & = \sec^{n-2} \theta \tan \theta -(n-2)\int \tan^2 \theta \sec^{n-2} \theta d\theta \\& = \sec^{n-2} \theta \tan \theta -(n-2)\int (\sec^2 \theta - 1) \sec^{n-2} \theta d\theta \\& = \sec^{n-2} \theta \tan \theta +(n-2)\int \sec^{n-2} \theta d\theta-(n-2)\int \sec^n\theta d\theta\end{align*} $$
หรือ
$$ (n-1)\int \sec^n\theta d\theta = \sec^{n-2} \theta \tan \theta +(n-2)\int \sec^{n-2} \theta d\theta $$

เพราะฉะนั้น
$$ \int \sec^n\theta d\theta = \frac{\sec^{n-2} \theta \tan \theta}{n-1} + \frac{n-2}{n-1} \int \sec^{n-2} \theta d\theta \quad \text{เมื่อ } n \geq 2 $$

ตัวอย่าง 2.3.5 จงหา
1. $\int \sec^5 \theta d\theta$
2. $\int \sec^6 \theta d\theta$
3. $\int \tan^3 \theta d\theta$

วิธีทำ
1. $\int \sec^5 \theta d\theta = \frac{\sec^3 \theta \tan \theta}{4} + \frac{3}{4} \int \sec^3 \theta d\theta$
   $= \frac{\sec^3 \theta \tan \theta}{4} + \frac{3}{4} \left( \frac{\sec^4 \theta \tan \theta}{2} + \frac{1}{2} \int \sec^4 \theta d\theta \right)$
   $= \frac{\sec^3 \theta \tan \theta}{4} + \frac{3}{8} \sec^4 \theta \tan \theta + \frac{3}{8} \ln|\sec^4 \theta| + \tan \theta| + C$
2. $\int \sec^6 \theta d\theta = \frac{\sec^4 \theta \tan \theta}{5} + \frac{4}{5} \int \sec^4 \theta d\theta$
   $= \frac{\sec^4 \theta \tan \theta}{5} + \frac{4}{5} \left( \frac{\sec^5 \theta \tan \theta}{3} + \frac{2}{3} \int \sec^5 \theta d\theta \right)$
   $= \frac{\sec^4 \theta \tan \theta}{5} + \frac{4}{15} \sec^5 \theta \tan \theta + \frac{8}{15} \tan \theta + C$
3. $\int \tan^3 \theta d\theta = \frac{\tan^2 \theta}{2} - \tan \theta \int \tan \theta d\theta = \frac{\tan^2 \theta}{2} - \ln|\sec^2 \theta| + C$

2.3.3 การหา $\int \cot^n \theta \csc^n \theta d\theta$
จากการพิจารณาความสัมพันธ์ต่อไปนี้
$\cot^2 \theta = \csc^2 \theta - 1$, $d(\csc \theta) = - \csc \theta \cot \theta d\theta$, $d(\cot \theta) = - \csc^2 \theta d\theta$
ซึ่งเป็นเอกลักษณ์และสูตรการหาอนุพันธ์รูปแบบเดียวกันกับคู่ของ $\tan \theta$ และ $\sec \theta$ เราจึง
พิจารณาการหาอินทิกรัลในแบบเดียวกับเมื่อหา $\int \tan^n \theta \sec^n \theta d\theta$

ตัวอย่าง 2.3.6 จงหา


1. $\int \cot^7 \theta \csc^{7/3} \theta d\theta$
2. $\int \csc^2 \theta d\theta$
3. $\int \cot^4 \theta d\theta$

วิธีทำ 1. เพราะว่า $d(\csc\theta) = -\csc\theta \cot\theta d\theta$ เราจึงจัดอินทิแกรนด์ให้อยู่ในรูปพหุนาม ของ $\csc\theta$ เพื่อการอินทิเกรตได้ดังนี้

$\int \cot^7 \theta \csc^{7/3} \theta d\theta = \int \cot^6 \theta \csc^{4/3} \theta \cot\theta \csc\theta d\theta = -\int (\cot^2 \theta)^3 \csc^3 \theta d(\csc\theta)$
$= -\int (\csc^6 \theta - 3 \csc^4 \theta + 3 \csc^2 \theta - 1) \csc^3 \theta d(\csc\theta)$
$= -\int \left( \frac{22}{\csc^3 \theta} - 3 \csc^2 \theta + 3 \csc^3 \theta - \frac{10}{\csc^3 \theta} \right) d(\csc\theta)$
$= -\int \left( \frac{25}{\csc^3 \theta} - \frac{9}{\csc^3 \theta} + \frac{19}{\csc^3 \theta} - \frac{9}{\csc^3 \theta} \right) d(\csc\theta)$
$= -\frac{3}{25} \csc^3 \theta + \frac{9}{19} \csc^3 \theta - \frac{9}{13} \csc^3 \theta + \frac{3}{7} \csc^3 \theta + C$

2. ให้ $u = \csc\theta$ และ $dv = \csc^2 \theta d\theta$ ซึ่งจะได้ $du = -\csc\theta \cot\theta d\theta$ และ $v = -\cot\theta$ ดังนั้น
$\int \csc^3 \theta d\theta = -\csc\theta \cot\theta - \int \cot^2 \theta \csc\theta d\theta = -\csc\theta \cot\theta - \int (-\csc\theta \cot\theta - \int \csc^3 \theta d\theta)$
หรือ $2 \int \csc^3 \theta d\theta = -\csc\theta \cot\theta + \int \csc^3 \theta d\theta$
เพราะฉะนั้น
$\int \csc^3 \theta d\theta = \frac{-\cot\theta \csc\theta}{2} + \ln|\csc\theta| + \cot\theta| + C$

3. $\int \cot^4 \theta d\theta = \int \cot^2 \theta \csc^2 \theta d\theta = \int \cot^2 \theta d\theta$
$= \int \cot^2 \theta d\theta - \int \cot^2 \theta d\theta$
$= -\int \cot^2 \theta d(\cot\theta) - \int (\csc^2 \theta - 1) d\theta$
$= -\frac{\cot^3 \theta}{3} + \cot\theta + \theta + C$

2.3.4 การหา $\int \sin ax \sin bx dx$, $\int \sin ax \cos bx dx$ และ $\int \cos ax \cos bx dx$

เนื่องจาก $\sin ax \sin bx$, $\sin ax \cos bx$ และ $\cos ax \cos bx$ เป็นผลคูณของฟังก์ชัน ตรีโกณมิติ แต่อยู่ในรูปผลคูณของฟังก์ชันตรีโกณมิติของ $\sin$ และ/หรือ $\cos$ ของมุมหรือจำนวน จริงที่ต่างกัน การ อินทิเกรตฟังก์ชันลักษณะนี้ เราจะใช้เอกลักษณ์ตรีโกณมิติต่อไปนี้
$\sin A \cos B = \frac{1}{2} [\sin(A+B)+\sin(A-B)]$

ภาควิชาคณิตศาสตร์
58


$$ \cos A \cos B = \frac{1}{2} [\cos(A+B)+\cos(A-B)] $$
$$ \sin A \sin B = \frac{1}{2} [\cos(A-B)-\cos(A+B)] $$
เพื่อแปลงอินทิกรัลให้อยู่ในรูปอินทิกรัลของ sin หรือ cos ดังจะแสดงให้เห็นในตัวอย่างต่อไปนี้

**ตัวอย่าง 2.3.7** จงหา $\int \sin ax \cos bx dx$

**วิธีทำ** เนื่องจาก
$\sin ax \cos bx = \frac{1}{2} [\sin(ax+bx)+\sin(ax-bx)] = \frac{1}{2} [\sin(a+b)x+\sin(a-b)x]$
เราจะได้
$$
\begin{align*}
\int \sin ax \cos bx dx  &= \frac{1}{2} \int [\sin(a+b)x+\sin(a-b)x] dx \\[0.5em]
&= \frac{1}{2} \left[ \sin(a+b)x + \frac{1}{2} \sin(a-b)x \right]
\end{align*}
$$

แบบฝึกหัด 2.3

จงหา

1.  $\int \sin x \cos xdx$
2.  $\int \tan^5 xdx$
3.  $\int \cos^8 tdt$
4.  $\int \cos x \sin^5 xdx$
5.  $\int \frac{\cos^2 x}{\sin^4 x} dx$
6.  $\int \frac{\sin^3 x}{\cos^4 x} dx$
7.  $\int \sec^4 2xdx$
8.  $\int (\tan \theta + 2 \cot \theta)^2 d\theta$
9.  $\int \sin^3 t \cos^5 tdt$
10. $\int \frac{\sec^2 x}{\sqrt{1-\tan^2 x}} dx$
11. $\int \csc^6 (2x+1) dx$
12. $\int \frac{\tan \theta}{\sin^2 \theta} d\theta$
13. $\int \sin^5 tdt$
14. $\int \sqrt{1+\cos x} dx$
15. $\int \cos^4 tdt$
16. $\int \sec^5 x \tan xdx$
17. $\int \sqrt{\tan x} \sec^4 xdx$
18. $\int \cot^2 \theta \csc^9 \theta d\theta$
19. $\int \cot^3 3xcsc^3 3x dx$
20. $\int \sec^4 \left( \frac{x}{3} \right) \sqrt{\tan \left( \frac{x}{3} \right)} dx$
21. $\int 3x \cos 2x dx$
22. $\int 4x \sin 2x dx$
23. $\int_0^{\pi/4} \frac{\sin^2 x}{\cos^4 x} dx$
24. $\int_{1/6}^{1/2} \csc \pi x \cdot \cot \pi x dx$

25. $\int_0^{1/4} \tan^4 (\pi x) dx$

59


## 2.4 การอินทิเกรตโดยการแทนด้วยฟังก์ชันตรีโกณมิติ

ในหัวข้อนี้เราจะอินทิเกรตฟังก์ชันซึ่งกำหนดในรูปที่มีนิพจน์ในรูปแบบ $\sqrt{x^2 \pm a^2}$ หรือ $\sqrt{a^2 - x^2}$ เป็นตัวประกอบ ซึ่งหลักสำคัญของเทคนิคที่ใช้คือการทำให้เครื่องหมายรากที่สองหมดไป โดยสังเกตว่าเอกลักษณ์ตรีโกณมิติต่อไปนี้
$$\cos^2 \theta = 1 - \sin^2 \theta, \quad \tan^2 \theta = \sec^2 \theta - 1, \quad \sec^2 \theta = \tan^2 \theta + 1$$
อยู่ในรูปที่อาจแปลความหมายได้ว่า กำลังสองของตัวแปรหนึ่งเป็นผลบวกหรือผลต่างของกำลังสองของอีกตัวแปรหนึ่งกับค่าคงตัว ดังนั้นถ้าให้ $x$ ใน $\sqrt{a^2 - x^2}$ หรือ $\sqrt{x^2 \pm a^2}$ เป็นฟังก์ชัน $\sin$, $\tan$ หรือ $\sec$ ที่เหมาะสมแล้วจะทำให้เครื่องหมายรากที่สองหมดไปได้ เราจึงเรียกเทคนิคนี้ว่า การอินทิเกรตโดยการแทนด้วยฟังก์ชันตรีโกณมิติ (integration by trigonometric substitutions) โดยมีหลักดังนี้

กรณี $\sqrt{a^2 - x^2}$ โดยที่ $a > 0$ : ให้ $x = a \sin \theta$ หรือ $\theta = \sin^{-1} \frac{x}{a}$ เมื่อ $\theta \in [-\frac{\pi}{2}, \frac{\pi}{2}]$
จะได้
$$\sqrt{a^2 - x^2} = \sqrt{a^2 \left(1 - \sin^2 \theta\right)} = \sqrt{a^2} \cos^2 \theta = |a| \cos \theta = a \cos \theta$$
และโดยความสัมพันธ์ของสามเหลี่ยมมุมฉาก เราสามารถแทน
$$\cos \theta = \frac{\sqrt{a^2 - x^2}}{a} \quad \text{และ} \quad \tan \theta = \frac{x}{\sqrt{a^2 - x^2}}$$

กรณี $\sqrt{a^2 + x^2}$ โดยที่ $a > 0$ : ให้ $x = a \tan \theta$ หรือ $\theta = \tan^{-1} \frac{x}{a}$ เมื่อ $\theta \in (-\frac{\pi}{2}, \frac{\pi}{2})$
จะได้
$$\sqrt{a^2 + x^2} = \sqrt{a^2 \left(1 + \tan^2 \theta\right)} = \sqrt{a^2} \sec^2 \theta = |a| \sec \theta = a \sec \theta$$
และโดยความสัมพันธ์ของสามเหลี่ยมมุมฉาก เราสามารถแทน
$$\sin \theta = \frac{x}{\sqrt{a^2 + x^2}} \quad \text{และ} \quad \cos \theta = \frac{a}{\sqrt{a^2 + x^2}}$$

กรณี $\sqrt{x^2 - a^2}$ โดยที่ $a > 0$ : ให้ $x = a \sec \theta$ หรือ $\theta = \sec^{-1} \frac{x}{a}$ เมื่อ $\theta \in [0, \frac{\pi}{2}) \cup (\pi, \frac{3\pi}{2})$
จะได้
$$\sqrt{x^2 - a^2} = \sqrt{a^2 \left(\sec^2 \theta - 1\right)} = \sqrt{a^2} \tan^2 \theta = a \tan \theta$$
และโดยความสัมพันธ์ของสามเหลี่ยมมุมฉาก เราสามารถแทน
$$\sin \theta = \frac{\sqrt{x^2 - a^2}}{x} \quad \text{และ} \quad \tan \theta = \frac{\sqrt{x^2 - a^2}}{a}$$
ภาคผนวก
60


ตัวอย่าง 2.4.1 จงหา
1. $\int x^3 \sqrt{16-x^2} dx$
2. $\int \sqrt{a^2-x^2} dx$
3. $\int \frac{dx}{\sqrt{16+x^2}}$
4. $\int \frac{\sqrt{x^2-9}}{x} dx$

วิธีทำ 1. ให้ $x = 4 \sin \theta$ จะได้ $dx = 4 \cos \theta d\theta$ และ
$\sqrt{16-x^2} = \sqrt{16(1-\sin^2 \theta)} = 4 \cos \theta$ ดังนั้น
$\int x^3 \sqrt{16-x^2} dx = \int (4 \sin \theta)^3 (4 \cos \theta)(4 \cos \theta d\theta)$
$= -4^5 \int \sin^3 \theta \cos^2 \theta d\theta$
$= -4^5 \int (1-\cos^2 \theta)\cos^2 \theta d(\cos \theta)$
$= -4^5 \int (\cos^3 \theta - \cos^4 \theta)d(\cos \theta)$
$= -4^5 \left[ \frac{\cos^3 \theta}{3} - \frac{\cos^4 \theta}{5} \right] + C$
โดยความสัมพันธ์ของสามเหลี่ยมมุมฉากซึ่งในที่นี้ $\cos \theta = \frac{\sqrt{16-x^2}}{4}$ เราจึงได้
$\int x^{13} \sqrt{16-x^2} dx = \frac{4^5}{5} \left[ \frac{\sqrt{16-x^2}}{4} \right]^5 - \frac{4^5}{3} \left[ \frac{\sqrt{16-x^2}}{4} \right]^3 + C = \frac{1}{5}(16-x^2)^{\frac{5}{2}} - \frac{16}{3}(16-x^2)^{\frac{3}{2}} + C$

2. ให้ $x = a \sin \theta$ จะได้ $dx = a \cos \theta d\theta$ และ $\sqrt{a^2-x^2} = a \cos \theta$ ดังนั้น
$\int \sqrt{a^2-x^2} dx = \int a^2 \cos^2 \theta d\theta = a^2 \int \left( \frac{\cos 2\theta+1}{2} \right) d\theta$
$= \frac{a^2}{2} \left[ \frac{\sin 2\theta}{2} + \theta \right] + C$
$= \frac{a^2}{2} (\theta+\sin \theta \cos \theta)+C$
โดยความสัมพันธ์ของสามเหลี่ยมมุมฉากซึ่งในที่นี้ $\cos \theta = \frac{\sqrt{a^2-x^2}}{a}$ และ $\sin \theta = \frac{x}{a}$ ทำให้ได้
$\int \sqrt{a^2-x^2} dx = \frac{a^2}{2} \left[ \sin^{-1} \frac{x}{a} + \frac{x \sqrt{a^2-x^2}}{a^2} \right] + C$

3. ให้ $x = 4 \tan \theta$ จะได้ $dx = 4 \sec^2 \theta d\theta$ และ
$\sqrt{16+x^2} = \sqrt{16(1+\tan^2 \theta)} = 4 \sec \theta$ ดังนั้น
$\int \frac{dx}{\sqrt{16+x^2}} = \int \frac{4 \sec^2 \theta d\theta}{4 \sec \theta} = \int \sec \theta d\theta$
$= \ln |\sec \theta + \tan \theta| + C$


โดยความสัมพันธ์ของสามเหลี่ยมมุมฉากซึ่งในที่นี้ $\sec \theta = \frac{\sqrt{16+x^2}}{4}$ และ $\tan \theta = \frac{x}{4}$ ดังนั้น
$$ \int \frac{dx}{\sqrt{16+x^2}} = \ln \left| \frac{\sqrt{16+x^2}}{4} + \frac{x}{4} \right| + C $$

4. ให้ $x=3 \sec \theta$ จะได้ $dx=3 \sec \theta \tan \theta d\theta$ และ
$$
\begin{align*}
\sqrt{x^2-9}  &= \sqrt{9(\sec^2 \theta -1)} = 3 \tan \theta \quad \text{ดังนั้น} \\[0.5em]
\int \frac{\sqrt{x^2-9}}{x} dx  &= \int \frac{3 \tan \theta}{3 \sec \theta} \tan \theta d\theta = \int \tan^2 \theta d\theta \\[0.5em]
&= 3 \int (\sec^2 \theta -1) d\theta = 3 (\tan \theta - \theta) + C
\end{align*}
$$
โดยความสัมพันธ์ของสามเหลี่ยมมุมฉากซึ่งในที่นี้ $\tan \theta = \frac{\sqrt{x^2-9}}{x}$ และ $\theta = \sec^{-1} \frac{x}{3}$ ดังนั้น
$$ \int \frac{\sqrt{x^2-9}}{x} dx = 3 \left[ \frac{\sqrt{x^2-9}}{x} - \sec^{-1} \frac{x}{3} \right] + C $$

เราสามารถประยุกต์การแทนด้วยฟังก์ชันตรีโกณมิติเหล่านี้กับฟังก์ชันที่อยู่ในรูปผลบวก หรือผลต่างกำลังสอง หรือฟังก์ชันที่มีตัวประกอบหนึ่งในรูปต่อไปนี้
$$ \sqrt{a^2-b^2}[f(x)]^2 , \sqrt{a^2[f(x)]^2-b^2}, \sqrt{a^2+b^2}[f(x)]^2 $$
เมื่อ $a$ และ $b$ เป็นค่าคงตัว โดยการเปลี่ยนตัวแปรตามลำดับดังนี้
$$ bf(x)=asin \theta \quad \text{หรือ} \quad af(x)=bsec \theta \quad \text{หรือ} \quad bf(x)=atan \theta $$

**ตัวอย่าง 2.4.2 จงหา**
1. $ \int \frac{dx}{(1+9x^2)^2} $
2. $ \int \frac{dx}{(4-9x^2)^2} $
3. $ \int \frac{\sec^2 x}{(4-\tan^2 x)^{3/2}} dx $

วิธีทำ 1. ให้ $3x=\tan \theta$ จะได้ $3dx=\sec^2 \theta d\theta$ และ $1+9x^2=\sec^2 \theta$ ดังนั้น
ภาควิชาคณิตศาสตร์
62


$$
\begin{align*}
\int \frac{dx}{(1+9x^2)^2}  &= \frac{1}{3} \int \frac{\sec^2 \theta d\theta}{\sec^4 \theta} = \frac{1}{3} \cos^2 \theta d\theta = \frac{1}{6} \int (1+\cos 2\theta)d\theta \\[0.5em]
&= \frac{\theta}{6} + \frac{\sin 2\theta}{12} + C = \frac{\theta}{6} + \frac{\sin \theta \cos \theta}{6} + C \\[0.5em]
&= \frac{\tan^{-1}(3x)}{6} + \frac{1}{6} \frac{3x}{6+1+9x^2} + C \\[0.5em]
&= \frac{\tan^{-1}(3x)}{6} + \frac{x}{2(1+9x^2)} + C
\end{align*}
$$

2. ถ้าพิจารณา $9x^2 < 4$ และ $9x^2 = 4 \sin^2 \theta$ เราจะเลือกให้ $3x = 2 \sin \theta$ (เพราะฉะนั้น $|\sin \theta| = \frac{|3x|}{2} \leq 1$) จะได้ $3dx = 2 \cos \theta d\theta$ และ $4 - 9x^2 = 4 - 4 \sin^2 \theta = 4 \cos^2 \theta$ ดังนั้น
$$ \int \frac{dx}{(4-9x^2)^2} = \int \frac{2 \cos \theta}{3} d\theta = \frac{1}{24} \int \frac{\cos \theta}{\cos^4 \theta} d\theta = \frac{1}{24} \int \sec^3 \theta d\theta $$
จากสูตรลดทอนในหัวข้อก่อนหน้านี้เราจะได้
$$
\begin{align*}
\int \sec^3 \theta d\theta  &= \frac{\sec^{3-2} \theta \tan \theta}{3-1} + \frac{3-2}{3-1} \int \sec^{3-2} \theta d\theta \\[0.5em]
&= \frac{\sec \theta \tan \theta}{2} + \frac{1}{2} \int \sec \theta d\theta \\[0.5em]
&= \frac{\sec \theta \tan \theta}{2} + \frac{1}{2} \ln |\sec \theta + \tan \theta| + C
\end{align*}
$$
เพราะฉะนั้น
$$
\begin{align*}
\int \frac{dx}{(4-9x^2)^2}  &= \frac{\sec \theta \tan \theta}{48} + \frac{1}{48} \ln |\sec \theta + \tan \theta| + C \\[0.5em]
&= \frac{x}{8(4-9x^2)} + \frac{1}{48} \ln \left| \frac{2}{\sqrt{4-9x^2}} + \frac{3x}{\sqrt{4-9x^2}} \right| + C
\end{align*}
$$

3. ให้ $\tan x = 2 \sin \theta$ จะได้ $\sec^2 x dx = 2 \cos \theta d\theta$ ซึ่งทำให้ได้
$$
\begin{align*}
\int \frac{\sec^2 x}{(4-\tan^2 x)^{3/2}} dx  &= \int \frac{2 \cos \theta}{(4 \cos^2 \theta)^{3/2}} d\theta = \frac{1}{4} \int \sec^2 \theta d\theta = \frac{\tan \theta}{4} + C \\[0.5em]
&= \frac{\tan x}{4 \sqrt{4 - \tan^2 x}} + C
\end{align*}
$$

O
63
