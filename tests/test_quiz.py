from app.content import Question
from app.quiz import grade

QUESTIONS = [Question(text=f"q{i}", options=["a", "b"], correct=1) for i in range(5)]


def test_all_correct():
    r = grade(QUESTIONS, {i: 1 for i in range(5)})
    assert r.correct == 5 and r.passed


def test_80_percent_threshold():
    four_of_five = grade(QUESTIONS, {0: 1, 1: 1, 2: 1, 3: 1, 4: 0})
    assert four_of_five.passed
    three_of_five = grade(QUESTIONS, {0: 1, 1: 1, 2: 1, 3: 0, 4: 0})
    assert not three_of_five.passed


def test_unanswered_counts_as_wrong():
    r = grade(QUESTIONS, {0: 1})
    assert r.correct == 1
    assert r.answers[1].chosen is None and not r.answers[1].ok


def test_no_questions_does_not_pass():
    assert not grade([], {}).passed
