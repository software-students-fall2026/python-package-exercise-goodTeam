import pytest

from pyDeciders.wheel import spin_wheel

OPTIONS = ["pizza", "tacos", "sushi"]


def test_result_is_one_of_the_options():
    for seed in range(50):
        assert spin_wheel(OPTIONS, seed=seed) in OPTIONS


def test_single_option_always_wins():
    assert spin_wheel(["pizza"]) == "pizza"
    assert spin_wheel(["pizza"], weights=[5]) == "pizza"


def test_tuple_inputs_are_accepted():
    assert spin_wheel(("pizza", "tacos"), seed=1) in ("pizza", "tacos")
    assert spin_wheel(("pizza", "tacos"), weights=(0, 1)) == "tacos"


def test_same_seed_gives_same_result():
    for seed in range(50):
        assert spin_wheel(OPTIONS, seed=seed) == spin_wheel(OPTIONS, seed=seed)


def test_different_seeds_give_different_winners():
    winners = {spin_wheel(OPTIONS, seed=seed) for seed in range(50)}
    assert len(winners) > 1


def test_every_option_can_win():
    winners = {spin_wheel(OPTIONS, seed=seed) for seed in range(200)}
    assert winners == set(OPTIONS)


def test_zero_weight_option_never_wins():
    winners = {spin_wheel(OPTIONS, weights=[0, 1, 1], seed=seed) for seed in range(500)}
    assert "pizza" not in winners
    assert winners == {"tacos", "sushi"}


def test_weights_shift_the_odds():
    winners = [spin_wheel(["a", "b"], weights=[9, 1], seed=seed) for seed in range(1000)]
    assert winners.count("a") > 800
    assert winners.count("b") > 0


def test_float_weights_are_accepted():
    assert spin_wheel(["a", "b"], weights=[0.0, 0.5]) == "b"
    assert spin_wheel(["a", "b"], weights=[0.5, 0.0]) == "a"


@pytest.mark.parametrize("bad_options", ["pizza", None, 5, {"pizza"}, {"a": 1}])
def test_options_wrong_type_raises_type_error(bad_options):
    with pytest.raises(TypeError):
        spin_wheel(bad_options)


@pytest.mark.parametrize("empty_options", [[], ()])
def test_empty_options_raises_value_error(empty_options):
    with pytest.raises(ValueError):
        spin_wheel(empty_options)


@pytest.mark.parametrize("bad_weights", ["123", 5, {1, 2, 3}, {"a": 1}])
def test_weights_wrong_type_raises_type_error(bad_weights):
    with pytest.raises(TypeError):
        spin_wheel(OPTIONS, weights=bad_weights)


@pytest.mark.parametrize("bad_weights", [[], [1], [1, 2], [1, 2, 3, 4]])
def test_weights_wrong_length_raises_value_error(bad_weights):
    with pytest.raises(ValueError):
        spin_wheel(OPTIONS, weights=bad_weights)


@pytest.mark.parametrize("bad_weight", ["1", None, True, False, [1]])
def test_weight_wrong_type_raises_type_error(bad_weight):
    with pytest.raises(TypeError):
        spin_wheel(OPTIONS, weights=[1, 1, bad_weight])


@pytest.mark.parametrize("bad_weight", [-1, -0.5, float("nan"), float("inf"), float("-inf")])
def test_weight_invalid_value_raises_value_error(bad_weight):
    with pytest.raises(ValueError):
        spin_wheel(OPTIONS, weights=[1, 1, bad_weight])


@pytest.mark.parametrize("zero_weights", [[0, 0, 0], [0.0, 0.0, 0.0]])
def test_all_zero_weights_raises_value_error(zero_weights):
    with pytest.raises(ValueError):
        spin_wheel(OPTIONS, weights=zero_weights)
