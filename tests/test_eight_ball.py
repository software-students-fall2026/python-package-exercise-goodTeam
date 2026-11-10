import pytest

from pyDeciders.eight_ball import ANSWERS, NEGATIVE, POSITIVE, UNSURE, magic_8_ball


# valid inputs

def test_returns_a_known_answer():
    result = magic_8_ball("Should I order pizza?")
    assert isinstance(result, str)
    assert result in ANSWERS


def test_answer_list_is_balanced():
    assert len(POSITIVE) == len(UNSURE) == len(NEGATIVE)
    assert len(set(ANSWERS)) == len(ANSWERS)


def test_question_without_question_mark_works():
    assert magic_8_ball("will it rain", seed=1) in ANSWERS


def test_same_seed_gives_same_result():
    assert magic_8_ball("Will it rain?", seed=42) == magic_8_ball("Will it rain?", seed=42)
    answers = {magic_8_ball("Will it rain?", seed=s) for s in range(20)}
    assert len(answers) > 1


def test_every_kind_of_answer_can_come_up():
    answers = {magic_8_ball("Is today the day?", seed=s) for s in range(300)}
    assert answers & set(POSITIVE)
    assert answers & set(UNSURE)
    assert answers & set(NEGATIVE)


# invalid inputs

@pytest.mark.parametrize("blank", ["", "   ", "\n\t"])
def test_blank_question_raises_value_error(blank):
    with pytest.raises(ValueError):
        magic_8_ball(blank)


@pytest.mark.parametrize("bad_question", [None, 42, ["Will it rain?"], b"bytes?"])
def test_non_string_question_raises_type_error(bad_question):
    with pytest.raises(TypeError):
        magic_8_ball(bad_question)
