---
type: handoff
title: "ชุดส่งงานแก้ PR #3 สำหรับทั้งสองคน"
date: 2026-11-22
head: 11b10d4b485682455f5536d386f1e955aa1337bb
status: ready
---

# ชุดส่งงานแก้ PR #3

ทั้งสองคนใช้ชุดนี้ร่วมกัน ไม่แบ่ง role ล่วงหน้า

## ไฟล์

```text
FIX-TASKS.md                  รายการ 25 เคสที่ต้องแก้ (อ่านไฟล์นี้ก่อน)
TASKS.csv                     ตารางติดตาม เติม assignee/status เอง
PR3-BATTERY-400-2026-11-22.py สคริปต์รัน 400 เคส
battery400_lib.py             ตัวช่วยของสคริปต์
PR3-BATTERY-400-2026-11-22.csv ผลรัน 400 เคส
PR3-BATTERY-400-2026-11-22.md  ตารางอ่านง่าย 400 แถว
PR3-REVIEW-2026-11-22.md       รายงานเต็ม ใช้เป็นภาคผนวก
```

## วิธีทำ

1. อ่าน `FIX-TASKS.md` ด้วยกัน แล้วตกลงกันเองว่าใครทำข้อไหน
2. เติมชื่อใน `TASKS.csv` คอลัมน์ `assignee`
3. แตก branch เดียวจาก `11b10d4` ชื่อ `fix/pr3-findings`
4. แก้และรัน `pytest` กับ battery ของกลุ่มที่แก้
5. เปิด PR เดียวกลับไปที่ `feat/area-between-and-interactive-graph` โดยใส่ชื่อทั้งคู่

## คำสั่ง

```bash
python -m pytest tests/ -q
CALC_REPO=$PWD python PR3-BATTERY-400-2026-11-22.py area
CALC_REPO=$PWD python PR3-BATTERY-400-2026-11-22.py improper
CALC_REPO=$PWD python PR3-BATTERY-400-2026-11-22.py tangent
CALC_REPO=$PWD python PR3-BATTERY-400-2026-11-22.py substitution
CALC_REPO=$PWD python PR3-BATTERY-400-2026-11-22.py by_parts
```

## กติกา

- หารงานกันเอง ไม่มี role ตายตัว
- ก่อนแก้ไฟล์เดียวกันพร้อมกัน ให้ตกลงกันก่อน
- ห้ามแก้ค่าคาดหมายหรือสคริปต์ battery
- ห้าม force push
- PR body ต้องมีผลรัน `pytest` และ battery

