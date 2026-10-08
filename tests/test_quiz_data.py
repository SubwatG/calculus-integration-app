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
    def test_quiz_file_valid_structure_and_length(self, filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)

        assert isinstance(data, list), f"{filepath} root must be a list of questions"
        assert len(data) >= 10, f"{filepath} must contain at least 10 questions, found {len(data)}"

        for i, q in enumerate(data):
            for field in ["topic", "question", "choices", "answer", "hint", "explanation"]:
                assert field in q, f"Question {i+1} in {filepath} missing '{field}'"
                assert q[field], f"Field '{field}' in question {i+1} in {filepath} must not be empty"

            assert isinstance(q["choices"], list), f"'choices' in question {i+1} must be a list"
            assert len(q["choices"]) == 4, f"Question {i+1} in {filepath} must have exactly 4 choices (A, B, C, D)"
            assert q["answer"] in q["choices"], (
                f"Question {i+1} in {filepath}: answer '{q['answer']}' not found in choices {q['choices']}"
            )

    @pytest.mark.parametrize("filepath", get_quiz_files())
    def test_answer_distribution_not_skewed(self, filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)

        positions = [q["choices"].index(q["answer"]) for q in data]
        index_0_count = positions.count(0)
        max_allowed_0 = max(1, int(len(data) * 0.4))

        assert index_0_count <= max_allowed_0, (
            f"{filepath} has {index_0_count}/{len(data)} answers at choice A. "
            f"Answers must be balanced across choices A, B, C, D."
        )
        assert len(set(positions)) >= 3, (
            f"{filepath} answers should be spread across at least 3 choice positions (found {set(positions)})"
        )
