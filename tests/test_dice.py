import pytest

from pyDeciders.dice import roll_dice


# valid inputs

def test_default_is_one_six_sided_die():
    result = roll_dice()
    assert isinstance(result, list)
    assert len(result) == 1
    assert 1 <= result[0] <= 6


def test_n_controls_number_of_dice():
    result = roll_dice(n=5)
    assert len(result) == 5
    assert all(isinstance(roll, int) for roll in result)


def test_sides_controls_the_range():
    rolls = roll_dice(n=500, sides=20, seed=1)
    assert min(rolls) >= 1
    assert max(rolls) <= 20


def test_every_face_can_come_up():
    rolls = roll_dice(n=600, sides=6, seed=0)
    assert set(rolls) == {1, 2, 3, 4, 5, 6}


def test_two_sided_die_only_gives_1_or_2():
    rolls = roll_dice(n=100, sides=2, seed=3)
    assert set(rolls) == {1, 2}


def test_same_seed_gives_same_result():
    assert roll_dice(n=10, seed=42) == roll_dice(n=10, seed=42)
    assert roll_dice(n=10, seed=1) != roll_dice(n=10, seed=2)


# invalid inputs

@pytest.mark.parametrize("bad_n", [0, -1, -50])
def test_n_below_one_raises_value_error(bad_n):
    with pytest.raises(ValueError):
        roll_dice(n=bad_n)


@pytest.mark.parametrize("bad_n", [2.5, "3", None, True])
def test_n_wrong_type_raises_type_error(bad_n):
    with pytest.raises(TypeError):
        roll_dice(n=bad_n)


@pytest.mark.parametrize("bad_sides", [1, 0, -6])
def test_sides_below_two_raises_value_error(bad_sides):
    with pytest.raises(ValueError):
        roll_dice(sides=bad_sides)


@pytest.mark.parametrize("bad_sides", [6.0, "6", None, True])
def test_sides_wrong_type_raises_type_error(bad_sides):
    with pytest.raises(TypeError):
        roll_dice(sides=bad_sides)