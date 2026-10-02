"""Tests for conceptual quiz data banks in data/quizzes/*.json."""

import glob
import json
import os
import pytest

QUIZ_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data", "quizzes"))


def get_quiz_files():
    files = glob.glob(os.path.join(QUIZ_DIR, "*.json"))
    return files


class TestQuizData:
    def test_quiz_files_exist(self):
        files = get_quiz_files()
        assert len(files) >= 3, f"Expected at least 3 quiz files in {QUIZ_DIR}, found {len(files)}"

    @pytest.mark.parametrize("filepath", get_quiz_files())
    def test_quiz_file_valid_structure(self, filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)

        assert isinstance(data, list), f"{filepath} root must be a list of questions"
        assert len(data) >= 1, f"{filepath} must contain at least 1 question"

        for i, q in enumerate(data):
            for field in ["topic", "question", "choices", "answer", "hint", "explanation"]:
                assert field in q, f"Question {i+1} in {filepath} missing '{field}'"
                assert q[field], f"Field '{field}' in question {i+1} in {filepath} must not be empty"

            assert isinstance(q["choices"], list), f"'choices' in question {i+1} must be a list"
            assert len(q["choices"]) >= 2, f"Question {i+1} must have at least 2 choices"
            assert q["answer"] in q["choices"], (
                f"Question {i+1} in {filepath}: answer '{q['answer']}' not found in choices {q['choices']}"
            )
