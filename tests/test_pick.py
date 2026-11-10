import pytest

from pyDeciders.pick import pick_one


# valid inputs

def test_returns_one_of_the_options():
    options = ["pizza", "tacos", "sushi"]
    result = pick_one(options)
    assert result in options
    assert isinstance(result, str)


def test_single_option_is_always_picked():
    assert pick_one(["only"]) == "only"
    assert pick_one(("only",), seed=5) == "only"


def test_tuple_is_accepted():
    options = ("red", "green", "blue")
    assert pick_one(options, seed=1) in options


def test_non_string_options_work():
    assert pick_one([1, 2, 3], seed=0) in (1, 2, 3)


def test_same_seed_gives_same_result():
    options = list(range(100))
    assert pick_one(options, seed=42) == pick_one(options, seed=42)
    picks = {pick_one(options, seed=s) for s in range(20)}
    assert len(picks) > 1


def test_every_option_can_come_up():
    options = ["a", "b", "c", "d"]
    picks = {pick_one(options, seed=s) for s in range(200)}
    assert picks == set(options)


def test_does_not_change_the_options():
    options = ["a", "b", "c"]
    pick_one(options, seed=3)
    assert options == ["a", "b", "c"]


# invalid inputs

@pytest.mark.parametrize("empty", [[], ()])
def test_empty_options_raises_value_error(empty):
    with pytest.raises(ValueError):
        pick_one(empty)


@pytest.mark.parametrize("bad_options", ["abc", None, 5, {"a", "b"}, {"a": 1}])
def test_wrong_type_raises_type_error(bad_options):
    with pytest.raises(TypeError):
        pick_one(bad_options)
