"""Inventory displayed lesson files and exercise quiz scoring, without UI/network I/O."""
from collections import Counter
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from utils.content_loader import list_lessons, load_lesson, NON_LESSONS, ARCHIVE_DIR
from utils.math_render import format_math_spacing
from utils.quiz_engine import grade_quiz

lesson_root = ROOT/'data/lessons'
expected = {p.relative_to(lesson_root).as_posix() for p in lesson_root.rglob('*.md')
            if ARCHIVE_DIR not in p.parents and p.name not in NON_LESSONS}
lessons = list_lessons()
checks = []
checks.append(dict(id='LIB-INVENTORY', passed=expected=={item['filename'] for item in lessons}))
for index, item in enumerate(lessons, 1):
    checks.append(dict(id=f'LIB-{index:03d}', filename=item['filename'],
                       passed=bool(item['title'].strip()) and bool(item['text'].strip())
                       and load_lesson(item['filename'])==format_math_spacing(item['text'])))
quiz_inventory = []
for index, path in enumerate(sorted((ROOT/'data/quizzes').glob('*.json')), 1):
    questions = json.loads(path.read_text(encoding='utf-8'))
    quiz_inventory.append(dict(file=path.relative_to(ROOT).as_posix(), questions=len(questions)))
    valid = isinstance(questions, list) and bool(questions) and all(
        isinstance(q, dict) and isinstance(q.get('answer'), str) and bool(q['answer']) for q in questions)
    checks.append(dict(id=f'QUIZ-{index:03d}-schema', passed=valid))
    if not valid:
        continue
    for scenario, answers, expected_score in [
        ('all-correct', {i:q['answer'] for i,q in enumerate(questions)}, len(questions)),
        ('all-wrong', {i:'__fixture_wrong__' for i in range(len(questions))}, 0),
        ('blank', {}, 0),
        ('partial', {0:questions[0]['answer']}, 1),
    ]:
        checks.append(dict(id=f'QUIZ-{index:03d}-{scenario}',
                           passed=grade_quiz(questions, answers)=={'score':expected_score, 'total':len(questions)}))
counts = Counter('PASS' if item['passed'] else 'FAIL' for item in checks)
report = dict(scope='Loading and configured-key scoring only; not rendered UI or answer-key mathematical audit',
              lessons=len(lessons), quiz_files=len(quiz_inventory),
              questions=sum(item['questions'] for item in quiz_inventory),
              total=len(checks), passed=counts['PASS'], failed=counts['FAIL'],
              lesson_files=[item['filename'] for item in lessons], quizzes=quiz_inventory, checks=checks)
output = Path(__file__).with_name('content-results.json')
output.write_text(json.dumps(report, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
print(json.dumps({k:v for k,v in report.items() if k not in ['lesson_files','quizzes','checks']}, ensure_ascii=False))
raise SystemExit(1 if counts['FAIL'] else 0)
