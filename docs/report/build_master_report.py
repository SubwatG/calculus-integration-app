#!/usr/bin/env python3
"""
build_master_report.py
----------------------
สคริปต์ประกอบเอกสารรายงานโครงงาน Calculus Learning Sandbox ฉบับสมบูรณ์ (.docx)
ทำการรวบรวมเนื้อหาทุกบท (บทคัดย่อ, บทที่ 1-5, บรรณานุกรม, ภาคผนวก ก-จ)
และคอมไพล์เป็นไฟล์ Word (.docx) ไฟล์เดียว โดยคงรูปแบบสไตล์ reference.docx (TH SarabunPSK 16pt, ย่อหน้า 1.2 ซม.)
"""

import os
import re
import subprocess
import sys
from pathlib import Path

REPORT_DIR = Path(__file__).resolve().parent

# ลำดับไฟล์ในเล่มรายงานโครงงาน
CHAPTERS = [
    ("บทคัดย่อ (Abstract)", "abstract.qmd"),
    ("บทที่ 1 บทนำ", "chapter-01-introduction.qmd"),
    ("บทที่ 2 ทฤษฎีและเทคโนโลยีที่เกี่ยวข้อง", "chapter-02-background.qmd"),
    ("บทที่ 3 วิธีดำเนินงานและสถาปัตยกรรมระบบ", "chapter-03-methodology.qmd"),
    ("บทที่ 4 ผลการดำเนินงานและการทดสอบระบบ", "chapter-04-results.qmd"),
    ("บทที่ 5 สรุปผล อภิปราย และข้อเสนอแนะ", "chapter-05-conclusion.qmd"),
    ("บรรณานุกรม", "references-bibliography.qmd"),
    ("ภาคผนวก ก เครื่องมือการวิจัยและแบบประเมิน SUS", "appendix-a-survey.qmd"),
    ("ภาคผนวก ข คลังแบบทดสอบมโนทัศน์", "appendix-b-quiz-bank.qmd"),
    ("ภาคผนวก ค เมทริกซ์ขีดความสามารถและขอบเขตข้อจำกัด", "appendix-c-boundary-matrix.qmd"),
    ("ภาคผนวก ง คู่มือการติดตั้งและใช้งานระบบ", "appendix-d-installation-guide.qmd"),
    ("ภาคผนวก จ ประวัติผู้จัดทำโครงงาน", "appendix-e-biography.qmd"),
]

def strip_yaml_frontmatter(content: str) -> str:
    """ตัดแถบ YAML frontmatter ออกจากเนื้อหา"""
    pattern = r"^---\s*\n.*?\n---\s*\n"
    return re.sub(pattern, "", content, flags=re.DOTALL)

def assemble_master_qmd(output_path: Path):
    """ประกอบไฟล์ QMD รวมเล่ม"""
    master_header = """---
title: "รายงานโครงงานการพัฒนาเว็บแอปพลิเคชันช่วยเรียนคณิตศาสตร์สำหรับแคลคูลัสเบื้องต้น"
subtitle: "Calculus Learning Sandbox (Calculus Integration Application)"
author: "ภาควิชาวิทยาการคำนวณและเทคโนโลยีดิจิทัล คณะศิลปศาสตร์และวิทยาศาสตร์ มหาวิทยาลัยเกษตรศาสตร์"
format:
  docx:
    reference-doc: reference.docx
    toc: false
---

"""
    sections = [master_header]

    for title, filename in CHAPTERS:
        filepath = REPORT_DIR / filename
        if not filepath.exists():
            print(f"Warning: File {filename} not found, skipping...")
            continue
        
        with open(filepath, "r", encoding="utf-8") as f:
            raw_text = f.read()
        
        body_text = strip_yaml_frontmatter(raw_text).strip()
        
        # เพิ่ม Page Break ใน docx ก่อนขึ้นบทใหม่
        sections.append(f"\n\n{{{{< pagebreak >}}}}\n\n{body_text}")

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(sections))
    
    print(f"[OK] ประกอบไฟล์แม่แบบรวมเล่มสำเร็จ: {output_path.name}")

def render_to_docx(master_qmd: Path, output_docx: Path):
    """คอมไพล์ master qmd เป็น docx ผ่าน Quarto"""
    print(f"[*] กำลังเรนเดอร์เอกสาร Word: {output_docx.name} ผ่าน Quarto...")
    cmd = [
        "quarto",
        "render",
        str(master_qmd),
        "--to",
        "docx",
        "--output",
        output_docx.name,
    ]
    res = subprocess.run(cmd, cwd=str(REPORT_DIR), capture_output=True, text=True)
    if res.returncode != 0:
        print("[Error] การเรนเดอร์ล้มเหลว:")
        print(res.stderr)
        sys.exit(res.returncode)
    print(f"[SUCCESS] สร้างไฟล์เล่มรายงาน Word สำเร็จ: {output_docx}")

def render_individual_chapters():
    """เรนเดอร์ไฟล์แยกรายบทด้วย"""
    print("[*] กำลังเรนเดอร์ไฟล์แยกรายบท...")
    for title, filename in CHAPTERS:
        filepath = REPORT_DIR / filename
        if not filepath.exists():
            continue
        cmd = ["quarto", "render", str(filepath), "--to", "docx"]
        subprocess.run(cmd, cwd=str(REPORT_DIR), capture_output=True)
    print("[SUCCESS] เรนเดอร์ไฟล์แยกรายบทครบถ้วน")

def apply_cambria_math_fix(target_files: list[Path]):
    """เรียกสคริปต์ fix_math_cambria.py เพื่อกำหนด Cambria Math 12pt ให้สมการ"""
    fixer = REPORT_DIR / "fix_math_cambria.py"
    if not fixer.exists():
        print("[WARN] ไม่พบ fix_math_cambria.py — ข้ามการปรับ Cambria Math")
        return
    existing = [str(p) for p in target_files if p.exists()]
    if not existing:
        return
    cmd = [sys.executable, str(fixer)] + existing
    res = subprocess.run(cmd, cwd=str(REPORT_DIR), capture_output=True, text=True)
    if res.returncode != 0:
        print(f"[WARN] Cambria Math post-processing ล้มเหลว:\n{res.stderr}")
    else:
        print(res.stdout.strip())

def main():
    master_qmd = REPORT_DIR / "full-project-report-master.qmd"
    master_docx = REPORT_DIR / "full-project-report-master.docx"

    assemble_master_qmd(master_qmd)
    render_to_docx(master_qmd, master_docx)
    render_individual_chapters()

    # Post-process ทุกไฟล์ docx ให้สมการเป็น Cambria Math 12pt
    docx_targets = [master_docx] + [
        REPORT_DIR / filename for _, filename in CHAPTERS
    ]
    docx_targets = [p.with_suffix(".docx") for p in docx_targets if p.with_suffix(".docx").exists()]
    apply_cambria_math_fix(docx_targets)

if __name__ == "__main__":
    main()
