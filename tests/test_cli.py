import pytest

from pyDeciders import cli, flip_coin, magic_8_ball, pick_one, roll_dice
from pyDeciders.cli import build_parser, main, print_result


def run(capsys, *argv):
    """Run the CLI and return (exit code, stdout, stderr)."""
    code = main(list(argv))
    out, err = capsys.readouterr()
    return code, out, err


# dice

def test_dice_prints_requested_number_of_rolls(capsys):
    code, out, err = run(capsys, "dice", "-n", "4", "--sides", "20")
    rolls = [int(x) for x in out.split()]
    assert code == 0
    assert len(rolls) == 4
    assert all(1 <= roll <= 20 for roll in rolls)
    assert err == ""


def test_dice_defaults_to_one_six_sided_die(capsys):
    code, out, _ = run(capsys, "dice")
    assert code == 0
    assert len(out.split()) == 1
    assert 1 <= int(out) <= 6


def test_dice_seed_matches_library(capsys):
    _, out, _ = run(capsys, "dice", "-n", "5", "--seed", "42")
    expected = " ".join(str(r) for r in roll_dice(5, 6, 42))
    assert out.strip() == expected


def test_dice_bad_count_exits_with_error(capsys):
    code, out, err = run(capsys, "dice", "-n", "0")
    assert code == 1
    assert out == ""
    assert err.strip() == "decisions: n must be at least 1"


def test_dice_bad_sides_exits_with_error(capsys):
    code, _, err = run(capsys, "dice", "--sides", "1")
    assert code == 1
    assert "at least 2 sides" in err


# coin

def test_coin_bias_one_is_all_heads(capsys):
    code, out, _ = run(capsys, "coin", "--times", "3", "--bias", "1")
    assert code == 0
    assert out.strip() == "heads heads heads"


def test_coin_seed_matches_library(capsys):
    _, out, _ = run(capsys, "coin", "--times", "10", "--seed", "7")
    assert out.split() == flip_coin(10, 0.5, 7)


def test_coin_bad_bias_exits_with_error(capsys):
    code, out, err = run(capsys, "coin", "--bias", "2")
    assert code == 1
    assert out == ""
    assert "bias must be between 0 and 1" in err


# pick

def test_pick_prints_one_of_the_options(capsys):
    code, out, _ = run(capsys, "pick", "pizza", "tacos", "sushi")
    assert code == 0
    assert out.strip() in ("pizza", "tacos", "sushi")


def test_pick_seed_matches_library(capsys):
    options = ["a", "b", "c", "d", "e"]
    _, out, _ = run(capsys, "pick", *options, "--seed", "3")
    assert out.strip() == pick_one(options, 3)


def test_pick_needs_at_least_one_option(capsys):
    with pytest.raises(SystemExit) as exit_info:
        main(["pick"])
    assert exit_info.value.code == 2
    assert "options" in capsys.readouterr().err


# 8ball

def test_8ball_seed_matches_library(capsys):
    code, out, _ = run(capsys, "8ball", "Will it rain?", "--seed", "5")
    assert code == 0
    assert out.strip() == magic_8_ball("Will it rain?", 5)


def test_8ball_blank_question_exits_with_error(capsys):
    code, out, err = run(capsys, "8ball", "   ")
    assert code == 1
    assert out == ""
    assert err.strip() == "decisions: question must not be empty"


# wheel arguments (only parsing, so these keep passing once spin_wheel exists)

def test_wheel_arguments_are_parsed():
    args = build_parser().parse_args(["wheel", "a", "b", "c", "--weights", "1", "2", "3"])
    assert args.options == ["a", "b", "c"]
    assert args.weights == [1.0, 2.0, 3.0]
    assert args.seed is None


def test_wheel_weights_default_to_none():
    args = build_parser().parse_args(["wheel", "a", "b"])
    assert args.weights is None


# shared behaviour

@pytest.mark.parametrize(
    "argv",
    [
        ["dice", "-n", "3", "--seed", "1"],
        ["coin", "--times", "3", "--seed", "1"],
        ["pick", "x", "y", "z", "--seed", "1"],
        ["8ball", "Is it Friday?", "--seed", "1"],
    ],
)
def test_same_seed_gives_same_output(capsys, argv):
    _, first, _ = run(capsys, *argv)
    _, second, _ = run(capsys, *argv)
    assert first == second


def test_not_implemented_command_exits_with_message(capsys, monkeypatch):
    def not_ready(*args):
        raise NotImplementedError

    monkeypatch.setattr(cli, "roll_dice", not_ready)
    code, out, err = run(capsys, "dice")
    assert code == 1
    assert out == ""
    assert err.strip() == "decisions: dice is not implemented yet"


def test_missing_command_is_a_usage_error(capsys):
    with pytest.raises(SystemExit) as exit_info:
        main([])
    assert exit_info.value.code == 2
    assert "usage" in capsys.readouterr().err


def test_unknown_command_is_a_usage_error(capsys):
    with pytest.raises(SystemExit) as exit_info:
        main(["lottery"])
    assert exit_info.value.code == 2
    assert "invalid choice" in capsys.readouterr().err


def test_non_number_argument_is_a_usage_error(capsys):
    with pytest.raises(SystemExit) as exit_info:
        main(["dice", "-n", "three"])
    assert exit_info.value.code == 2
    assert "invalid int value" in capsys.readouterr().err


def test_help_exits_cleanly(capsys):
    with pytest.raises(SystemExit) as exit_info:
        main(["--help"])
    assert exit_info.value.code == 0
    out = capsys.readouterr().out
    for command in ("dice", "coin", "wheel", "pick", "8ball"):
        assert command in out


# print_result

def test_print_result_joins_lists_with_spaces(capsys):
    print_result([1, 2, 3])
    print_result(("heads", "tails"))
    assert capsys.readouterr().out == "1 2 3\nheads tails\n"


def test_print_result_prints_single_values(capsys):
    print_result("tacos")
    print_result(4)
    assert capsys.readouterr().out == "tacos\n4\n"
